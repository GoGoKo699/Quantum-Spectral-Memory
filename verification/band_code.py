"""Exact classical compilation for calibrated spectral-band memory codes.

The noise generator is A=sum_j g_j |1><1|_j.  This module implements the
finite-rational preprocessing and classical rank/unrank maps used by the
coherent circuit construction in science/encoder.md.  It does not simulate
coupling calibration or noisy physical gates.  Python's arbitrary-size
integers are used; table entries have at most n+1 bits.
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import accumulate
from typing import Sequence


def dyadic_grid(n: int, time: Fraction, error: Fraction) -> Fraction:
    """Largest dyadic delta with 16*n*n*time*delta**2 <= error.

    All decisions use exact rational comparisons, including at powers of two.
    Thus delta_star/2 < delta <= delta_star, with no square-root oracle.
    """
    time, error = Fraction(time), Fraction(error)
    if n < 1 or time <= 0 or not 0 < error < Fraction(1, 4):
        raise ValueError("Require n>=1, time>0 and 0<error<1/4")
    target = error / (16*n*n*time)
    delta = Fraction(1)
    while delta*delta > target:
        delta /= 2
    while 4*delta*delta <= target:
        delta *= 2
    return delta


def nearest_integer(value: Fraction) -> int:
    """Round to nearest integer; exact half ties go toward positive infinity."""
    value = Fraction(value)
    return (2*value.numerator+value.denominator)//(2*value.denominator)


@dataclass
class BandCode:
    estimates: tuple[Fraction, ...]
    uncertainty: tuple[Fraction, ...]
    time: Fraction
    error_target: Fraction
    delta: Fraction
    signed_weights: tuple[int, ...]
    weights: tuple[int, ...]
    origin: int
    lower: int
    upper: int
    population: int
    prefix_counts: list[list[int]]

    @property
    def n(self) -> int:
        return len(self.weights)

    @property
    def logical_qubits(self) -> int:
        return self.population.bit_length()-1

    @property
    def logical_dimension(self) -> int:
        return 1 << self.logical_qubits

    @property
    def true_width_bound(self) -> Fraction:
        # Each true basis energy is within sum(delta/2+u_j) of its
        # rounded counterpart; taking both endpoints is conservative.
        return ((self.upper-self.lower)*self.delta
                + self.n*self.delta + 2*sum(self.uncertainty))

    @property
    def storage_error_bound(self) -> Fraction:
        return self.time*self.true_width_bound**2/4

    @property
    def table_cells(self) -> int:
        return sum(map(len, self.prefix_counts))

    def count(self, suffix: int, lower: int, upper: int) -> int:
        """Number of accepted suffix strings; bounds may be out of range."""
        prefix = self.prefix_counts[suffix]
        lower = max(0, lower)
        upper = min(upper, len(prefix)-2)
        return 0 if upper < lower else prefix[upper+1]-prefix[lower]

    def unrank(self, index: int) -> tuple[int, ...]:
        """Return the index-th band word in lexicographic sign-flipped order.

        All population labels are supported for diagnostics. The quantum
        code uses only 0 <= index < logical_dimension.
        """
        if not isinstance(index, int) or not 0 <= index < self.population:
            raise ValueError("Band index out of range")
        residual = index
        lower, upper = self.lower, self.upper
        result = []
        for j, weight in enumerate(self.weights):
            zeros = self.count(j+1, lower, upper)
            if residual < zeros:
                bit = 0
            else:
                bit = 1
                residual -= zeros
                lower -= weight
                upper -= weight
            result.append(1-bit if self.signed_weights[j] < 0 else bit)
        if residual != 0 or not lower <= 0 <= upper:
            raise ArithmeticError("Invalid unranking terminal state")
        return tuple(result)

    def rank(self, word: Sequence[int]) -> int:
        """Inverse of unrank on the complete chosen band."""
        if len(word) != self.n or any(x not in (0, 1) for x in word):
            raise ValueError("Expected one binary entry per physical qubit")
        index = 0
        lower, upper = self.lower, self.upper
        for j, (x, weight) in enumerate(zip(word, self.weights)):
            bit = 1-x if self.signed_weights[j] < 0 else x
            if bit:
                index += self.count(j+1, lower, upper)
                lower -= weight
                upper -= weight
        if not lower <= 0 <= upper or not index < self.population:
            raise ValueError("Word is outside the chosen band")
        return index

    def report(self) -> dict:
        """Finite compilation facts; an uncertainty certificate is an input."""
        return {
            "physical_qubits": self.n,
            "time": str(self.time),
            "error_target": str(self.error_target),
            "dyadic_grid": str(self.delta),
            "calibration_error_bounds": [str(x) for x in self.uncertainty],
            "integer_band": [self.lower+self.origin,self.upper+self.origin],
            "sum_range": sum(self.weights),
            "band_population": self.population,
            "logical_qubits": self.logical_qubits,
            "table_cells": self.table_cells,
            "true_spectral_width_bound": str(self.true_width_bound),
            "half_diamond_storage_bound": str(self.storage_error_bound),
        }


def compile_band(estimates: Sequence[Fraction], time: Fraction, error: Fraction,
                 uncertainty: Sequence[Fraction] | None = None) -> BandCode:
    """Compile a maximum-population rounded band using exact integer DP.

    Caller-supplied uncertainty[j] certifies |g_j-estimates[j]| at the
    storage interval. It must lie in [0,delta/2]. Omitting it treats the
    rational estimates as exact supplied coefficients, not measured data.
    Negative q_j are handled by a known bit complement and energy shift.
    """
    estimates = tuple(Fraction(x) for x in estimates)
    n = len(estimates)
    time, error = Fraction(time), Fraction(error)
    delta = dyadic_grid(n,time,error)
    uncertainty = (tuple(Fraction(x) for x in uncertainty) if uncertainty is not None
                   else (Fraction(0),)*n)
    if len(uncertainty) != n or any(u < 0 or u > delta/2 for u in uncertainty):
        raise ValueError("Each certified coupling error must be at most delta/2")
    signed = tuple(nearest_integer(x/delta) for x in estimates)
    weights = tuple(abs(x) for x in signed)
    origin = sum(x for x in signed if x < 0)
    suffix = [[1]]
    for weight in reversed(weights):
        old = suffix[-1]
        new = old+[0]*weight
        for s,value in enumerate(old):
            new[s+weight] += value
        suffix.append(new)
    suffix.reverse()
    prefixes = [[0]+list(accumulate(row)) for row in suffix]
    full = prefixes[0]
    width = 4*n

    def population(lower):
        return full[min(lower+width+1,len(full)-1)]-full[lower]

    lower = max(range(len(full)-1),key=population)
    code = BandCode(estimates,uncertainty,time,error,delta,signed,weights,origin,
                    lower,lower+width,population(lower),prefixes)
    if code.storage_error_bound > 9*error/16:
        raise ArithmeticError("Construction exceeds certified storage budget")
    return code


def exact_occupancy(values: Sequence[Fraction], width: Fraction) -> int:
    """Closed-window population for small exactly enumerable spectra."""
    width=Fraction(width)
    if width < 0:
        raise ValueError("Window width must be nonnegative")
    ordered=sorted(Fraction(x) for x in values)
    end=best=0
    for begin,value in enumerate(ordered):
        while end < len(ordered) and ordered[end] <= value+width:
            end += 1
        best=max(best,end-begin)
    return best


def exact_spectrum(coefficients: Sequence[Fraction]) -> list[Fraction]:
    """Exponential enumeration for small verification cases only."""
    values=[Fraction(0)]
    for coefficient in coefficients:
        coefficient=Fraction(coefficient)
        values += [x+coefficient for x in values]
    return values
