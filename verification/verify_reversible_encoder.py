#!/usr/bin/env python3
"""Exact-bit band compiler and X/CNOT/Toffoli circuit verification.

The quantum prototype compiles the dynamic-program lookup, comparison and
arithmetic into primitive reversible gates.  It does not replace either
rank/unrank oracle with a black-box permutation or a unit-cost QRAM call.

Sparse basis propagation avoids allocating 2**(temporary workspace) amplitudes.
This is exact for this reversible circuit; Gaussian noise is then applied to
the physical-register matrix elements, including entangled reference inputs.
Only Python's standard library and NumPy are required.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import json
from math import isqrt
from pathlib import Path
import random
from typing import Callable

import numpy as np

from band_code import (
    compile_band as primary_compile_band,
    dyadic_grid as primary_dyadic_grid,
    nearest_integer as primary_nearest_integer,
)


def pow2(k: int) -> Fraction:
    return Fraction(1 << k, 1) if k >= 0 else Fraction(1, 1 << (-k))


def floor_log2_fraction(x: Fraction) -> int:
    assert x > 0
    p, q = x.numerator, x.denominator
    k = p.bit_length() - q.bit_length()
    too_large = p < (q << k) if k >= 0 else (p << (-k)) < q
    return k - int(too_large)


def select_grid(n: int, t: Fraction, epsilon: Fraction) -> tuple[int, Fraction]:
    if n < 1 or t <= 0 or not (0 < epsilon < Fraction(1, 4)):
        raise ValueError("Need n >= 1, t > 0 and 0 < epsilon < 1/4.")
    square = epsilon / (16 * n * n * t)
    k = floor_log2_fraction(square) // 2
    delta = pow2(k)
    assert delta * delta <= square < 4 * delta * delta
    return k, delta


def nearest_integer_ties_up(x: Fraction) -> int:
    y = x + Fraction(1, 2)
    return y.numerator // y.denominator


def exact_subdivision_factor(epsilon: Fraction) -> int:
    # Smallest k with k^2 epsilon >= 16; exactly ceil(4/sqrt(epsilon)).
    numerator = 16 * epsilon.denominator
    denominator = epsilon.numerator
    ceiling_ratio = (numerator + denominator - 1) // denominator
    return isqrt(ceiling_ratio - 1) + 1


@dataclass
class Band:
    q: list[int]
    h: list[int]
    sign_flip: list[bool]
    total_weight: int
    width: int
    start: int
    population: int
    logical_qubits: int
    suffix: list[list[int]]
    completions: list[list[int]]

    @property
    def dimension(self) -> int:
        return 1 << self.logical_qubits

    def classical_unrank(self, rank: int) -> list[int]:
        if not (0 <= rank < self.population):
            raise ValueError("rank outside accepted band")
        p = 0
        out = []
        for j, h in enumerate(self.h):
            c = self.completions[j][p]
            bit = int(rank >= c)
            out.append(bit)
            if bit:
                rank -= c
                p += h
        assert rank == 0
        assert self.start <= p <= self.start + self.width
        return out

    def classical_rank(self, y: list[int]) -> int:
        p = 0
        rank = 0
        for j, bit in enumerate(y):
            if bit:
                rank += self.completions[j][p]
                p += self.h[j]
        return rank

    def physical_bits(self, rank: int) -> list[int]:
        return [b ^ int(f) for b, f in zip(self.classical_unrank(rank), self.sign_flip)]


def construct_band(q: list[int], width: int | None = None) -> Band:
    n = len(q)
    h = [abs(v) for v in q]
    smax = sum(h)
    width = 4 * n if width is None else width
    suffix = [[0] * (smax + 1) for _ in range(n + 1)]
    suffix[n][0] = 1
    for j in range(n - 1, -1, -1):
        for s in range(smax + 1):
            suffix[j][s] = suffix[j + 1][s]
            if s >= h[j]:
                suffix[j][s] += suffix[j + 1][s - h[j]]

    # Closed integer interval: width+1 integer points, diameter width.
    window = sum(suffix[0][: min(width, smax) + 1])
    best_start, best_population = 0, window
    for a in range(1, smax + 1):
        window -= suffix[0][a - 1]
        if a + width <= smax:
            window += suffix[0][a + width]
        if window > best_population:
            best_start, best_population = a, window

    completions = []
    for j in range(n):
        prefix = [0]
        for count in suffix[j + 1]:
            prefix.append(prefix[-1] + count)

        def cumulative(z: int) -> int:
            if z < 0:
                return 0
            if z >= smax:
                return prefix[-1]
            return prefix[z + 1]

        completions.append([
            cumulative(best_start + width - p) - cumulative(best_start - 1 - p)
            for p in range(smax + 1)
        ])

    return Band(
        q=q, h=h, sign_flip=[v < 0 for v in q], total_weight=smax,
        width=width, start=best_start, population=best_population,
        logical_qubits=best_population.bit_length() - 1,
        suffix=suffix, completions=completions,
    )


# Signals are wire numbers >= 0 or the two constant sentinels below.
ZERO = -1
ONE = -2


def constant(bit: int | bool) -> int:
    return ONE if bit else ZERO


@dataclass(frozen=True)
class Gate:
    controls: tuple[int, ...]
    target: int

    def apply(self, basis: int) -> int:
        if all((basis >> c) & 1 for c in self.controls):
            return basis ^ (1 << self.target)
        return basis

    @property
    def name(self) -> str:
        return ("X", "CX", "CCX")[len(self.controls)]


class ReversibleBuilder:
    """Fresh-wire Boolean computation, made clean by compute-copy-uncompute."""

    def __init__(self) -> None:
        self.next_wire = 0
        self.peak_wires = 0
        self.gates: list[Gate] = []

    def allocate(self, number: int = 1) -> list[int]:
        out = list(range(self.next_wire, self.next_wire + number))
        self.next_wire += number
        self.peak_wires = max(self.peak_wires, self.next_wire)
        return out

    def fresh(self) -> int:
        return self.allocate()[0]

    def gate(self, controls: tuple[int, ...], target: int) -> None:
        assert 0 <= len(controls) <= 2
        assert min((target,) + controls) >= 0
        assert len(set((target,) + controls)) == len(controls) + 1
        self.gates.append(Gate(controls, target))

    def copy_signal(self, signal: int, target: int) -> None:
        if signal == ONE:
            self.gate((), target)
        elif signal >= 0:
            self.gate((signal,), target)

    def bnot(self, a: int) -> int:
        if a < 0:
            return ONE if a == ZERO else ZERO
        out = self.fresh()
        self.gate((), out)
        self.gate((a,), out)
        return out

    def bxor(self, a: int, b: int) -> int:
        if a == b:
            return ZERO
        if a == ZERO:
            return b
        if b == ZERO:
            return a
        if a == ONE:
            return self.bnot(b)
        if b == ONE:
            return self.bnot(a)
        out = self.fresh()
        self.gate((a,), out)
        self.gate((b,), out)
        return out

    def band(self, a: int, b: int) -> int:
        if a == ZERO or b == ZERO:
            return ZERO
        if a == b:
            return a
        if a == ONE:
            return b
        if b == ONE:
            return a
        out = self.fresh()
        self.gate((a, b), out)
        return out

    def mux(self, control: int, when_one: int, when_zero: int) -> int:
        return self.bxor(when_zero, self.band(control, self.bxor(when_one, when_zero)))

    def add(self, a: list[int], b: list[int], carry: int = ZERO) -> tuple[list[int], int]:
        assert len(a) == len(b)
        out = []
        for x, y in zip(a, b):
            xy = self.bxor(x, y)
            out.append(self.bxor(xy, carry))
            # x&y and carry&(x xor y) are disjoint Boolean events.
            carry = self.bxor(self.band(x, y), self.band(carry, xy))
        return out, carry

    def subtract(self, a: list[int], b: list[int]) -> tuple[list[int], int]:
        # Carry out is exactly the unsigned a >= b comparison.
        return self.add(a, [self.bnot(x) for x in b], ONE)

    def lookup(self, address: list[int], table: list[int], output_bits: int) -> list[int]:
        """Explicit equality-controlled XOR scan of all classical addresses."""
        out = self.allocate(output_bits)
        for addr, value in enumerate(table):
            if value == 0:
                continue
            eq = ONE
            for j, bit in enumerate(address):
                literal = bit if ((addr >> j) & 1) else self.bnot(bit)
                eq = self.band(eq, literal)
            for j in range(output_bits):
                if (value >> j) & 1:
                    self.copy_signal(eq, out[j])
        return out

    def xor_oracle(self, function: Callable[[], list[int]], targets: list[int]) -> None:
        if not targets:
            return
        saved_cursor = self.next_wire
        start = len(self.gates)
        outputs = function()
        assert len(outputs) == len(targets)
        end = len(self.gates)
        for source, target in zip(outputs, targets):
            self.copy_signal(source, target)
        # Every primitive is self-inverse.  Copy gates are intentionally omitted.
        self.gates.extend(reversed(self.gates[start:end]))
        # Ancillas are clean again, so the next oracle may reuse their wires.
        self.next_wire = saved_cursor


def integer_signals(value: int, length: int) -> list[int]:
    return [constant((value >> i) & 1) for i in range(length)]


def unrank_function(builder: ReversibleBuilder, band: Band, rank: list[int]) -> list[int]:
    n = len(band.q)
    count_bits = n + 1
    sum_bits = max(1, band.total_weight.bit_length())
    residual = rank + [ZERO] * (count_bits - len(rank))
    prefix = [ZERO] * sum_bits
    y = []
    for j, h in enumerate(band.h):
        count = builder.lookup(prefix, band.completions[j], count_bits)
        difference, choose_one = builder.subtract(residual, count)
        y.append(choose_one)
        residual = [builder.mux(choose_one, a, b) for a, b in zip(difference, residual)]
        increment = [choose_one if (h >> k) & 1 else ZERO for k in range(sum_bits)]
        prefix, _ = builder.add(prefix, increment)
    return y


def rank_function(builder: ReversibleBuilder, band: Band, y: list[int], output_bits: int) -> list[int]:
    count_bits = len(band.q) + 1
    sum_bits = max(1, band.total_weight.bit_length())
    rank = [ZERO] * count_bits
    prefix = [ZERO] * sum_bits
    for j, bit in enumerate(y):
        count = builder.lookup(prefix, band.completions[j], count_bits)
        increment = [builder.band(bit, x) for x in count]
        rank, _ = builder.add(rank, increment)
        sum_increment = [bit if (band.h[j] >> k) & 1 else ZERO for k in range(sum_bits)]
        prefix, _ = builder.add(prefix, sum_increment)
    return rank[:output_bits]


@dataclass
class CompiledEncoder:
    builder: ReversibleBuilder
    logical: list[int]
    physical: list[int]

    def apply_basis(self, basis: int, inverse: bool = False) -> int:
        gates = reversed(self.builder.gates) if inverse else self.builder.gates
        for gate in gates:
            basis = gate.apply(basis)
        return basis

    def write_register(self, register: list[int], value: int) -> int:
        return sum(((value >> j) & 1) << wire for j, wire in enumerate(register))

    def read_register(self, register: list[int], basis: int) -> int:
        return sum(((basis >> wire) & 1) << j for j, wire in enumerate(register))


def compile_encoder(band: Band) -> CompiledEncoder:
    builder = ReversibleBuilder()
    logical = builder.allocate(band.logical_qubits)
    physical = builder.allocate(len(band.q))
    builder.xor_oracle(lambda: unrank_function(builder, band, logical), physical)
    builder.xor_oracle(
        lambda: rank_function(builder, band, physical, band.logical_qubits), logical
    )
    for j, flip in enumerate(band.sign_flip):
        if flip:
            builder.gate((), physical[j])
    return CompiledEncoder(builder, logical, physical)


def physical_energy(bits: list[int], coefficients: list[Fraction]) -> Fraction:
    return sum((g * x for x, g in zip(bits, coefficients)), Fraction(0))


def exact_resolution_population(energies: list[Fraction], t: Fraction) -> int:
    ordered = sorted(energies)
    left, best = 0, 0
    for right, value in enumerate(ordered):
        while t * (value - ordered[left]) ** 2 > 1:
            left += 1
        best = max(best, right - left + 1)
    return best


def partial_trace_error(output: np.ndarray, target: np.ndarray) -> float:
    return float(np.linalg.svd(output - target, compute_uv=False).sum() / 2)


def test_reference_input(
    compiled: CompiledEncoder,
    band: Band,
    energies: list[Fraction],
    t: Fraction,
    coefficients: np.ndarray,
) -> dict:
    """Propagate an entangled pure state through gates, physical noise, inverse gates."""
    dimension, reference_dimension = coefficients.shape
    assert dimension == band.dimension
    coefficients = coefficients / np.linalg.norm(coefficients)
    support = []
    for r in range(dimension):
        for ref in range(reference_dimension):
            amplitude = coefficients[r, ref]
            if amplitude != 0:
                before = compiled.write_register(compiled.logical, r)
                encoded = compiled.apply_basis(before)
                support.append((r, ref, amplitude, encoded))

    allowed_mask = sum(1 << q for q in compiled.physical)
    assert all(encoded & ~allowed_mask == 0 for _, _, _, encoded in support)
    amps = np.asarray([row[2] for row in support], dtype=complex)
    encoded_rho = np.outer(amps, amps.conj())
    energy_array = np.asarray([float(energies[r]) for r, _, _, _ in support])
    physical_noise = np.exp(-float(t) * (energy_array[:, None] - energy_array[None, :]) ** 2 / 2)
    noisy_rho = encoded_rho * physical_noise

    decoded_indices = []
    logical_mask = sum(1 << q for q in compiled.logical)
    for r, ref, _, encoded in support:
        decoded = compiled.apply_basis(encoded, inverse=True)
        assert decoded & ~logical_mask == 0
        decoded_rank = compiled.read_register(compiled.logical, decoded)
        assert decoded_rank == r
        decoded_indices.append(decoded_rank * reference_dimension + ref)

    size = dimension * reference_dimension
    actual = np.zeros((size, size), dtype=complex)
    actual[np.ix_(decoded_indices, decoded_indices)] = noisy_rho
    initial = np.outer(coefficients.reshape(-1), coefficients.reshape(-1).conj())
    code_energies = np.asarray([float(x) for x in energies])
    schur = np.exp(-float(t) * (code_energies[:, None] - code_energies[None, :]) ** 2 / 2)
    expected = initial * np.kron(schur, np.ones((reference_dimension, reference_dimension)))
    residual = float(np.max(np.abs(actual - expected)))
    assert residual < 1e-13
    assert abs(np.trace(actual) - 1) < 1e-12
    assert np.linalg.eigvalsh(actual).min() > -1e-12
    return {
        "reference_dimension": reference_dimension,
        "nonzero_input_amplitudes": len(support),
        "decoded_schur_max_entry_error": residual,
        "trace_distance_from_ideal_storage": partial_trace_error(actual, initial),
        "all_encoder_and_decoder_workspaces_clean": True,
    }


def verify_case(n: int, intended_q: list[int], label: str, outdir: Path, export: bool) -> dict:
    epsilon, t = Fraction(1, 16), Fraction(4)
    exponent, delta = select_grid(n, t, epsilon)
    # Rational estimates with uncertainty at its allowed boundary.  The
    # calibration displacements alternate signs and include nonzero true
    # couplings even when an intended rounded weight is zero.
    estimate = [delta * (q + (Fraction(1, 4) if j % 2 == 0 else -Fraction(1, 4)))
                for j, q in enumerate(intended_q)]
    true_g = [g + (delta / 2 if j % 3 == 0 else -delta / 2)
              for j, g in enumerate(estimate)]
    uncertainty = [delta / 2] * n
    assert all(abs(g - gh) <= u for g, gh, u in zip(true_g, estimate, uncertainty))
    assert all(u <= delta / 2 for u in uncertainty)
    q = [nearest_integer_ties_up(g / delta) for g in estimate]
    assert q == intended_q
    assert all(abs(g - delta * w) <= delta for g, w in zip(true_g, q))
    band = construct_band(q)

    # Independent implementation comparison: the primitive circuit is still
    # compiled entirely from this module's own suffix/completion tables.
    primary = primary_compile_band(estimate, t, epsilon, uncertainty)
    assert primary.delta == delta
    assert tuple(q) == primary.signed_weights
    assert tuple(band.h) == primary.weights
    assert (band.start, band.start + band.width) == (primary.lower, primary.upper)
    assert band.population == primary.population
    assert band.logical_qubits == primary.logical_qubits
    compared_addresses = 0
    for j in range(n):
        for p in range(band.total_weight + 1):
            assert band.completions[j][p] == primary.count(
                j + 1, band.start - p, band.start + band.width - p
            )
            compared_addresses += 1

    accepted = []
    # Integer r below uses a conventional big-endian lexicographic y-string.
    for r in range(1 << n):
        y = [(r >> (n - 1 - j)) & 1 for j in range(n)]
        total = sum(h * b for h, b in zip(band.h, y))
        if band.start <= total <= band.start + band.width:
            accepted.append(y)
    assert len(accepted) == band.population
    for rank, y in enumerate(accepted):
        assert band.classical_unrank(rank) == y
        assert band.classical_rank(y) == rank
        x = [b ^ int(f) for b, f in zip(y, band.sign_flip)]
        assert sum(w * b for w, b in zip(q, x)) == sum(h * b for h, b in zip(band.h, y)) - sum(-w for w in q if w < 0)
        assert tuple(x) == primary.unrank(rank)
        assert primary.rank(x) == rank

    compiled = compile_encoder(band)
    code_energies = []
    physical_mask = sum(1 << wire for wire in compiled.physical)
    compiled_strings = []
    for rank in range(band.dimension):
        before = compiled.write_register(compiled.logical, rank)
        encoded = compiled.apply_basis(before)
        assert encoded & ~physical_mask == 0
        x = [(encoded >> wire) & 1 for wire in compiled.physical]
        assert x == band.physical_bits(rank)
        assert compiled.apply_basis(encoded, inverse=True) == before
        compiled_strings.append("".join(map(str, x)))
        code_energies.append(physical_energy(x, true_g))

    rng = random.Random(20261103 + n)
    for _ in range(3):
        arbitrary = rng.getrandbits(compiled.builder.peak_wires)
        assert compiled.apply_basis(compiled.apply_basis(arbitrary), inverse=True) == arbitrary

    all_energies = [physical_energy([(r >> j) & 1 for j in range(n)], true_g)
                    for r in range(1 << n)]
    mt = exact_resolution_population(all_energies, t)
    k = exact_subdivision_factor(epsilon)
    assert band.population * k >= mt
    diameter = max(code_energies) - min(code_energies)
    assert diameter <= 6 * n * delta
    assert diameter <= primary.true_width_bound
    storage_bound = t * diameter * diameter / 4
    assert storage_bound <= 9 * epsilon / 16

    bell = np.eye(band.dimension, dtype=complex) / np.sqrt(band.dimension)
    bell_result = test_reference_input(compiled, band, code_energies, t, bell)
    numpy_rng = np.random.default_rng(20261103 + n)
    generic = (numpy_rng.normal(size=(band.dimension, 3))
               + 1j * numpy_rng.normal(size=(band.dimension, 3)))
    generic_result = test_reference_input(compiled, band, code_energies, t, generic)
    assert bell_result["trace_distance_from_ideal_storage"] <= float(storage_bound) + 1e-12
    assert generic_result["trace_distance_from_ideal_storage"] <= float(storage_bound) + 1e-12

    counts = Counter(g.name for g in compiled.builder.gates)
    if export:
        gate_path = outdir / f"{label}_primitive_gates.json"
        gate_path.write_text(json.dumps({
            "format": "Reversible primitive circuit; all wires initialized to zero except logical input",
            "logical_wires_little_endian": compiled.logical,
            "physical_wires_site_order": compiled.physical,
            "total_wires": compiled.builder.peak_wires,
            "gates": [[gate.name, *gate.controls, gate.target] for gate in compiled.builder.gates],
        }, separators=(",", ":")) + "\n")

    return {
        "case": label, "n": n, "epsilon": str(epsilon), "t": str(t),
        "grid_exponent": exponent, "delta": str(delta),
        "estimates": list(map(str, estimate)), "true_coefficients": list(map(str, true_g)),
        "uncertainty": list(map(str, uncertainty)), "rounded_weights": q,
        "nonnegative_weights": band.h, "S": band.total_weight,
        "closed_band": [band.start, band.start + band.width],
        "band_population": band.population, "logical_qubits": band.logical_qubits,
        "dimension": band.dimension, "resolution_population": mt,
        "subdivision_factor": k, "physical_codewords": compiled_strings,
        "true_code_diameter": str(diameter),
        "analytic_half_diamond_storage_bound": str(storage_bound),
        "uniform_budget_9epsilon_over16": str(9 * epsilon / 16),
        "encoder_primitive_gate_count": len(compiled.builder.gates),
        "encoder_gate_counts": dict(counts),
        "decoder_primitive_gate_count": len(compiled.builder.gates),
        "total_circuit_wires": compiled.builder.peak_wires,
        "temporary_work_qubits": compiled.builder.peak_wires - n - band.logical_qubits,
        "storage_qubits_only": n,
        "bell_reference_test": bell_result, "generic_reference_test": generic_result,
        "arbitrary_basis_inverse_tests": 3,
        "classical_band_exhaustively_checked": True,
        "compiled_all_logical_basis_inputs_checked": True,
        "primary_module_comparison": {
            "module": "band_code.py",
            "same_grid_weights_band_and_population": True,
            "accepted_words_ranked_and_unranked": len(accepted),
            "completion_table_addresses_compared": compared_addresses,
            "all_passed": True,
        },
    }


def exact_arithmetic_checks() -> dict:
    # The selection rule includes exact powers and values on either side of a
    # power.  No floating square root or logarithm enters the compiler.
    checks = 0
    for e in range(-60, 61):
        for factor in (Fraction(1), Fraction(3, 2), Fraction(999, 1000)):
            value = pow2(e) * factor
            k = floor_log2_fraction(value)
            assert pow2(k) <= value < pow2(k + 1)
            checks += 1
    for n in range(1, 11):
        for t in (Fraction(1, 10**8), Fraction(1), Fraction(4), Fraction(10**9)):
            for epsilon in (Fraction(1, 16), Fraction(1, 100), Fraction(1, 10**6)):
                _, delta = select_grid(n, t, epsilon)
                assert delta == primary_dyadic_grid(n, t, epsilon)
                v = epsilon / (16 * n * n * t)
                assert delta * delta <= v < 4 * delta * delta
                k = exact_subdivision_factor(epsilon)
                assert k * k * epsilon >= 16
                assert (k - 1) ** 2 * epsilon < 16
                checks += 1
    for integer in range(-10, 11):
        assert nearest_integer_ties_up(Fraction(integer) + Fraction(1, 2)) == integer + 1
        assert primary_nearest_integer(Fraction(integer) + Fraction(1, 2)) == integer + 1
        checks += 1
    return {
        "exact_rational_checks": checks,
        "independent_grid_comparisons": 120,
        "independent_rounding_tie_comparisons": 21,
        "all_passed": True,
    }


def verify_boundaries(output: Path | None = None) -> dict:
    """Exercise the zero-logical-qubit and one-negative-physical-qubit edges.

    These cases are separate from the five performance-table instances.  The
    m=0 case still prepares a nonzero physical word and checks clean inverse
    decoding; its logical/reference tests are necessarily product-state tests.
    """
    output = Path(output) if output is not None else Path(__file__).resolve().parent / "results"
    specifications = [
        (2, [-9, 18], "zero_logical_qubits"),
        (1, [-3], "one_negative_physical_qubit"),
    ]
    summaries = []
    for n, q, label in specifications:
        case = verify_case(n, q, label, output, export=False)
        if label == "zero_logical_qubits":
            assert case["logical_qubits"] == 0 and case["dimension"] == 1
            assert case["physical_codewords"] == ["10"]
        else:
            assert case["n"] == 1 and case["rounded_weights"][0] < 0
            assert case["logical_qubits"] == 1 and case["dimension"] == 2
            assert case["physical_codewords"] == ["1", "0"]
        summaries.append({
            key: case[key] for key in (
                "case", "n", "rounded_weights", "band_population",
                "logical_qubits", "dimension", "physical_codewords",
                "encoder_primitive_gate_count", "temporary_work_qubits",
                "analytic_half_diamond_storage_bound", "primary_module_comparison",
            )
        } | {
            "all_encoder_and_decoder_workspaces_clean": all(
                case[test]["all_encoder_and_decoder_workspaces_clean"]
                for test in ("bell_reference_test", "generic_reference_test")
            ),
            "max_decoded_schur_entry_error": max(
                case[test]["decoded_schur_max_entry_error"]
                for test in ("bell_reference_test", "generic_reference_test")
            ),
            "all_passed": True,
        })
    return {
        "cases": summaries,
        "logical_basis_inputs_checked": sum(x["dimension"] for x in summaries),
        "all_passed": True,
    }


def run_verification(output: Path | None = None, verbose: bool = False) -> dict:
    """Run every primitive-gate test, save deterministic artifacts, return data.

    Assertion or import failures propagate to the caller.  The unified runner
    invokes this function unconditionally; gate verification is not optional.
    """
    output = Path(output) if output is not None else Path(__file__).resolve().parent / "results"
    output.mkdir(parents=True, exist_ok=True)
    cases = [
        (3, [0, -5, 12], "signed_zero_n3"),
        (4, [-17, 0, 11, 25], "signed_zero_n4"),
        (5, [0, -9, 14, 21, -31], "signed_zero_n5"),
        (6, [-7, 0, 11, 16, -23, 29], "signed_zero_n6"),
        (4, [0, 0, 0, 0], "all_rounded_zero_n4"),
    ]
    result = {"arithmetic": exact_arithmetic_checks(), "cases": []}
    for n, q, label in cases:
        case = verify_case(n, q, label, output, export=(n == 4 and sum(map(abs, q)) > 0))
        result["cases"].append(case)
        if verbose:
            print(json.dumps({k: case[k] for k in (
                "case", "dimension", "band_population", "encoder_primitive_gate_count",
                "temporary_work_qubits", "analytic_half_diamond_storage_bound"
            )}), flush=True)
    result["boundary_checks"] = verify_boundaries(output)
    result["all_passed"] = True
    (output / "reversible_encoder.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if verbose:
        print("All exact-bit, primitive-circuit, cleanup and entangled-channel checks passed.", flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "results")
    args = parser.parse_args()
    run_verification(args.output, verbose=True)


if __name__ == "__main__":
    main()
