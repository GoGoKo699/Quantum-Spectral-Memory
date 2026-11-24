"""Check finite examples for the Gaussian noise-rank theorem."""

from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import product
from math import ceil, comb, e, exp, factorial, fsum, isclose, log, sqrt


def majority_failure_numerator(qubits, flip_weight, no_flip_weight):
    """Count majority events with integer probability weights."""
    return sum(
        comb(qubits, weight)
        * flip_weight**weight
        * no_flip_weight**(qubits - weight)
        for weight in range(qubits // 2 + 1, qubits + 1)
    )


def majority_failure_recurrence(qubits, flip_probability):
    """Obtain the same probability by propagating rational masses."""
    masses = [Fraction(1)]
    for _ in range(qubits):
        updated = [Fraction(0)] * (len(masses) + 1)
        for weight, mass in enumerate(masses):
            updated[weight] += mass * (1 - flip_probability)
            updated[weight + 1] += mass * flip_probability
        masses = updated
    assert sum(masses) == 1
    return sum(masses[qubits // 2 + 1 :])


def check_phase_repetition():
    # The squared separation of distinct hypercube signatures is at least
    # 2 ln(8) = 6 ln(2) > 4, as certified by two positive terms of
    # ln(2) = 2 atanh(1/3).
    series_argument = Fraction(1, 3)
    separation_squared_lower_bound = 12 * (
        series_argument + series_argument**3 / 3
    )
    assert separation_squared_lower_bound > 4
    # Gaussian coherence exp(-ln(8)) equals 1/8. A Z flip attenuates
    # coherence by 1 - 2p, because it negates every one-bit off-diagonal.
    coherence = Fraction(1, 8)
    flip_probability = (1 - coherence) / 2
    assert flip_probability == Fraction(7, 16)
    flip_weight, denominator = flip_probability.as_integer_ratio()
    no_flip_weight = denominator - flip_weight

    pattern_count = 0
    for qubits in range(1, 10, 2):
        all_qubits = (1 << qubits) - 1
        syndrome_representatives = {}
        failure_numerator = 0
        for error in range(1 << qubits):
            # Adjacent X-parity measurements identify a phase-error mask up
            # to flipping every bit. The two masks have distinct weights.
            syndrome = (error ^ (error >> 1)) & (all_qubits >> 1)
            complement = all_qubits ^ error
            weight = error.bit_count()
            correction = error if weight <= qubits // 2 else complement
            representative = syndrome_representatives.setdefault(syndrome, correction)
            assert representative == correction
            residual = correction ^ error
            assert residual == (all_qubits if weight > qubits // 2 else 0)
            if residual:
                failure_numerator += flip_weight**weight * no_flip_weight**(
                    qubits - weight
                )
            pattern_count += 1
        assert len(syndrome_representatives) == 1 << (qubits - 1)
        assert failure_numerator == majority_failure_numerator(
            qubits, flip_weight, no_flip_weight
        )

    qubits = 151
    risk = Fraction(
        majority_failure_numerator(qubits, flip_weight, no_flip_weight),
        denominator**qubits,
    )
    assert risk == majority_failure_recurrence(qubits, flip_probability)
    assert risk < Fraction(1, 16)
    # A much smaller point supplies an independent check against using an
    # off-by-one majority threshold.
    assert majority_failure_recurrence(3, flip_probability) == Fraction(833, 2048)
    with localcontext() as context:
        context.prec = 40
        rounded_risk = f"{Decimal(risk.numerator) / Decimal(risk.denominator):.12f}"
    assert rounded_risk == "0.061217204448"
    print(f"Phase repetition: {pattern_count} small error patterns checked.")
    print(f"151-qubit half-diamond error: {rounded_risk} < 1/16 (exact comparison).")


def dot(left, right):
    return fsum(x * y for x, y in zip(left, right, strict=True))


def polynomial_exponential(argument, cutoff):
    return fsum(argument**degree / factorial(degree) for degree in range(cutoff + 1))


def poisson_tail(mean, cutoff):
    # Evaluate the omitted positive series directly instead of subtracting
    # a cumulative probability close to one.
    degree = cutoff + 1
    term = exp(-mean) * mean**degree / factorial(degree)
    tail = term
    while term:
        degree += 1
        term *= mean / degree
        updated = tail + term
        if updated == tail:
            break
        tail = updated
    return tail


def normalized_features(signature, indices):
    features = []
    for index in indices:
        feature = 1.0
        for coordinate, power in zip(signature, index, strict=True):
            feature *= coordinate**power / sqrt(factorial(power))
        features.append(feature)
    norm = sqrt(dot(features, features))
    return [value / norm for value in features], norm


def check_gaussian_features():
    fixtures = (
        ((0.0,), (1.0,), (-0.75,), (0.3,)),
        ((0.0, 0.0), (1.0, 1.0), (-0.8, 0.4), (0.2, -1.2)),
        ((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), (-1.0, 0.2, 0.7), (0.4, -0.8, 1.2)),
    )
    epsilon = 1 / 16
    max_gram_residual = 0.0
    max_dilation_displacement = 0.0
    for rank, signatures in enumerate(fixtures, start=1):
        cutoff = ceil(2 * rank + log(2 / epsilon**2))
        indices = [
            index
            for index in product(range(cutoff + 1), repeat=rank)
            if sum(index) <= cutoff
        ]
        assert len(indices) == comb(rank + cutoff, cutoff)
        projected = []
        for signature in signatures:
            mean = dot(signature, signature)
            assert mean <= rank
            features, norm = normalized_features(signature, indices)
            assert isclose(dot(features, features), 1, abs_tol=2e-14, rel_tol=0)
            tail = poisson_tail(mean, cutoff)
            mass = exp(-mean) * norm**2
            assert isclose(mass, 1 - tail, abs_tol=2e-14, rel_tol=0)
            assert tail <= exp((e - 1) * mean - cutoff) <= epsilon**2 / 2
            # Stable form of sqrt(2 - 2 sqrt(1 - tail)).
            displacement = sqrt(2 * tail / (1 + sqrt(1 - tail)))
            assert displacement <= epsilon
            max_dilation_displacement = max(displacement, max_dilation_displacement)
            projected.append((signature, features, norm, displacement))

        for left, left_features, left_norm, left_shift in projected:
            for right, right_features, right_norm, right_shift in projected:
                actual_gram = dot(left_features, right_features)
                expected_norm = sqrt(
                    polynomial_exponential(dot(left, left), cutoff)
                    * polynomial_exponential(dot(right, right), cutoff)
                )
                assert isclose(left_norm * right_norm, expected_norm, rel_tol=2e-14)
                expected_gram = polynomial_exponential(dot(left, right), cutoff) / (
                    expected_norm
                )
                residual = abs(actual_gram - expected_gram)
                assert residual < 2e-14
                max_gram_residual = max(residual, max_gram_residual)
                squared_distance = fsum(
                    (x - y) ** 2 for x, y in zip(left, right, strict=True)
                )
                true_gram = exp(-squared_distance / 2)
                assert abs(actual_gram - true_gram) <= left_shift + right_shift + 2e-14
    print(
        f"Gaussian features: 48 Gram entries checked "
        f"(max residual {max_gram_residual:.3g})."
    )
    print(
        f"Largest dilation displacement among 12 signatures: "
        f"{max_dilation_displacement:.6g}."
    )


def check_disjoint_feature_mixtures():
    # With degree one, the normalized feature projector for signature z is
    # the matrix [[1, z], [z, z^2]] / (1 + z^2).
    groups = (
        {-1: Fraction(1, 2), 1: Fraction(1, 2)},
        {-2: Fraction(5, 16), 0: Fraction(3, 8), 2: Fraction(5, 16)},
    )
    first, second = groups
    assert first.keys().isdisjoint(second)
    expected = (Fraction(1, 2), Fraction(0), Fraction(0), Fraction(1, 2))
    for weights in groups:
        assert all(weight > 0 for weight in weights.values())
        assert sum(weights.values()) == 1
        mixture = tuple(
            sum(weight * Fraction(z**power, 1 + z**2) for z, weight in weights.items())
            for power in (0, 1, 1, 2)
        )
        assert mixture == expected
    print("Truncated code: two disjoint groups give identical feature mixtures I/2.")


if __name__ == "__main__":
    check_phase_repetition()
    check_gaussian_features()
    check_disjoint_feature_mixtures()
