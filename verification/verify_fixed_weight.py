"""Check the signed fixed-weight counting and certificate with exact arithmetic."""

from collections import Counter
from fractions import Fraction
from itertools import product
from random import Random


def signed_energy(bits, weights):
    return sum(weight * (1 - 2 * bit) for bit, weight in zip(bits, weights))


def suffix_counts(weights, target_weight):
    """Return signed energy counts indexed by suffix start and residual weight."""
    size = len(weights)
    counts = [
        [Counter() for _ in range(target_weight + 1)] for _ in range(size + 1)
    ]
    counts[size][0][0] = 1
    for site in range(size - 1, -1, -1):
        weight = weights[site]
        for left in range(target_weight + 1):
            for energy, multiplicity in counts[site + 1][left].items():
                counts[site][left][energy + weight] += multiplicity
            if left:
                for energy, multiplicity in counts[site + 1][left - 1].items():
                    counts[site][left][energy - weight] += multiplicity
    return counts


def population(counts, lower, upper):
    return sum(value for energy, value in counts.items() if lower <= energy <= upper)


def zero_branch(weights, counts, site, left, partial, lower, upper):
    after_zero = partial + weights[site]
    return population(counts[site + 1][left], lower - after_zero, upper - after_zero)


def unrank(weights, counts, target_weight, lower, upper, index):
    bits = []
    left = target_weight
    partial = 0
    for site, weight in enumerate(weights):
        count = zero_branch(weights, counts, site, left, partial, lower, upper)
        bit = int(index >= count)
        if bit:
            index -= count
        bits.append(bit)
        left -= bit
        partial += weight * (1 - 2 * bit)
    assert index == left == 0
    assert lower <= partial <= upper
    return tuple(bits)


def rank(bits, weights, counts, target_weight, lower, upper):
    index = 0
    left = target_weight
    partial = 0
    for site, (bit, weight) in enumerate(zip(bits, weights)):
        if bit:
            index += zero_branch(weights, counts, site, left, partial, lower, upper)
        left -= bit
        partial += weight * (1 - 2 * bit)
    return index


def verify_case(weights, target_weight, diameter):
    size = len(weights)
    counts = suffix_counts(weights, target_weight)
    exhaustive = {
        bits: signed_energy(bits, weights)
        for bits in product((0, 1), repeat=size)
        if sum(bits) == target_weight
    }
    assert counts[0][target_weight] == Counter(exhaustive.values())

    total_range = sum(map(abs, weights))
    closed_bands = {}
    for lower in range(-total_range, total_range + 1):
        upper = lower + diameter
        accepted = [
            bits for bits, energy in exhaustive.items() if lower <= energy <= upper
        ]
        assert population(counts[0][target_weight], lower, upper) == len(accepted)
        closed_bands[lower] = accepted
    lower = max(closed_bands, key=lambda start: len(closed_bands[start]))
    upper = lower + diameter
    accepted = closed_bands[lower]
    for index, bits in enumerate(accepted):
        assert unrank(weights, counts, target_weight, lower, upper, index) == bits
        assert rank(bits, weights, counts, target_weight, lower, upper) == index

    scale = Fraction(1, 8)
    errors = [Fraction((-1) ** site, 16) for site in range(size)]
    centered = [scale * weight + error for weight, error in zip(weights, errors)]
    shift = Fraction(59, 7)
    shifted = [coefficient + shift for coefficient in centered]
    actual = []
    for bits in accepted:
        energy = signed_energy(bits, shifted)
        assert energy - signed_energy(bits, centered) == shift * (
            size - 2 * target_weight
        )
        predicted = shift * (size - 2 * target_weight) + scale * exhaustive[bits]
        assert abs(energy - predicted) <= sum(map(abs, errors))
        actual.append(energy)
    actual_diameter = max(actual) - min(actual)
    assert actual_diameter <= scale * diameter + 2 * sum(map(abs, errors))
    return len(closed_bands), len(accepted)


def main():
    cases = [
        ((-3, 0, 2), 1, 4),
        ((0, 0, 0, 0), 2, 0),
        ((-5, -2, -2, 0), 2, 0),
        ((-5, 0, 8), 0, 0),
        ((-5, 0, 8), 3, 0),
    ]
    random = Random(20261124)
    for trial in range(195):
        size = 1 + trial % 9
        weights = tuple(random.randint(-13, 13) for _ in range(size))
        cases.append((weights, random.randint(0, size), random.randint(0, 11)))

    band_count = rank_count = 0
    for weights, target_weight, width in cases:
        bands, ranks = verify_case(weights, target_weight, width)
        band_count += bands
        rank_count += ranks
    print(
        f"Fixed-weight checks passed: {len(cases)} sectors, "
        f"{band_count} band populations, {rank_count} rank/unrank pairs, "
        f"and {rank_count} exact common-offset and coefficient certificates."
    )


if __name__ == "__main__":
    main()
