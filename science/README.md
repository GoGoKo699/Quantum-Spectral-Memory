# Scientific account

The central question is the recoverable dimension of one finite memory after Gaussian dephasing for a prescribed time. The spectrum matters at a finite resolution: nearby eigenvalues can support a large approximate memory even when no two are exactly equal.

The [operational model](model.md) fixes the noise normalization, deterministic endpoint operations, retained classical records and half-diamond error. Only the physical memory crosses the interval. These choices are essential to the interpretation of every bound.

## Main logical dependencies

| Step | Result | What it establishes |
|---|---|---|
| Spectral interval protection | [Lemma 1](spectral_law.md#lemma-1-reference-stable-protection-of-a-spectral-interval) | A band of diameter $`a`$ has storage error at most $`ta^2/4`$, including an arbitrary reference. |
| General-code converse | [Lemma 2](spectral_law.md#lemma-2-a-converse-for-arbitrary-encoding-and-classical-records) | The Gaussian Gram matrix bounds every allowed code through completely positive comparison with full dephasing. |
| Occupancy estimate | [Lemma 3](spectral_law.md#lemma-3-gaussian-row-sums-from-local-occupancy) | Gaussian row sums are bounded by a constant times the maximum population of a resolution interval. |
| Finite-time law | [Theorem 1](spectral_law.md#theorem-1-one-register-storage) | The optimal number of logical qubits is $`\log_2M_t+O_\epsilon(1)`$. |
| Calibrated compilation | [Encoder construction](encoder.md) | Certified finite-precision couplings suffice to compile a clean coherent code within a fixed-error constant number of qubits of the unrestricted optimum. |

The general theorem assumes no efficient eigenbasis. The compiler makes a stronger implementation statement for the explicitly supplied weighted-qubit operator $`A=\sum_jg_jN_j`$. Its integer counting tables, arithmetic, lookups, reversible gates, workspace and input precision are all charged. It uses no unpriced quantum RAM.

## Interpretation and boundaries

The [examples](examples.md) compare the homogeneous exact-noiseless limit with a nondegenerate finite register, then connect the construction to executable checks. The [interpretation](interpretation.md) derives a rate bound from spectral variance and explains the difference between finite-time approximate storage and the infinite-time algebra.

The exact-error boundary is independently proved in [Proposition 2](spectral_law.md#proposition-2-exact-storage-at-every-positive-time): at every positive time, the largest exactly correctable dimension is the largest exact eigenspace. This does not limit the larger approximate code permitted at a prescribed nonzero error.

A separate [independent-use capacity corollary](interpretation.md#separate-corollary-communication-over-independent-complete-uses) uses the same occupancy statistic to bound communication rates when complete channels are used independently. It is optional to the storage theorem and compiler. It assumes fresh noise between uses and does not describe active correction during one passive interval.

## Evidence and attribution

The [verification guide](../verification/README.md) distinguishes exact integer checks, floating-point matrix diagnostics, primitive-gate simulations and the larger classical compilation example. No finite test replaces an asymptotic proof or establishes physical gate fidelity.

The [related-work account](../references/related_work.md) identifies the existing channel converse, approximate-subspace and reversible-coding techniques. The contribution is the specific uniform finite-time characterization and its calibrated, efficiently compiled consequence.

[Repository overview](../README.md)
