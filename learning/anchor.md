# Selected anchor: Watrous (2018)

A memory must preserve the relative phases in an unknown quantum state, including its correlations with another system. Under common-mode dephasing, nearby noise eigenvalues acquire nearly the same random phase. This project asks how much quantum information that observation can protect at a specified finite exposure, and whether an encoder achieving nearly the best possible size can actually be compiled.

## Selected source and version

The single educational anchor is **John Watrous, *The Theory of Quantum Information*, Cambridge University Press, 2018**, [DOI:10.1017/9781316848142](https://doi.org/10.1017/9781316848142).

Use the [author's book page](https://jhwatrous.github.io/books-and-courses.html), [standard-layout manuscript PDF](https://jhwatrous.github.io/TQI.pdf), and [author's errata](https://jhwatrous.github.io/TQI.errata.pdf). The linked manuscript identifies itself as the 2018 pre-publication version; section references below follow that version. The official chapter PDFs are linked directly below. This repository provides links, without redistributing the manuscript.

The linked errata are dated July 23, 2025; they include corrected norm-conversion constants in Theorems 3.56 and 8.45. The project's interval-error estimate is proved directly, without using those conversions.

Watrous supplies the mathematical foundations. The project's spectral occupancy law and calibrated compiler require the additional arguments identified here. Primary papers in [Related work](../references/related_work.md) supply research attribution and theorem dependencies; they are separate from this one educational anchor.

## Targeted reading map

Consult the sections when their role becomes relevant; completing the whole book is unnecessary. The [30-milestone map](milestones.md) organizes the project's story rather than following textbook chapter order.

| Project need | Watrous sections and official PDF | Connection to the project |
|---|---|---|
| Operators and matrix norms | §§1.1.2–1.1.3, [Chapter 1](https://jhwatrous.github.io/TQI.1.pdf) | Eigenvalues, positive operators, spectral norm and trace norm. |
| States and inaccessible references | §§2.1.2–2.1.3, [Chapter 2](https://jhwatrous.github.io/TQI.2.pdf) | Reduced states and purifications explain what the memory must preserve. |
| Channels and classical records | §2.2.2 and the instrument discussion in §2.3.2, [Chapter 2](https://jhwatrous.github.io/TQI.2.pdf) | Choi representations, isometries and branches of an encoder instrument. |
| Operational error | §§3.1.1, 3.2, 3.3.2–3.3.3, [Chapter 3](https://jhwatrous.github.io/TQI.3.pdf) | Trace distance, fidelity conventions and error stable under references. |
| Entrywise dephasing | §4.1.3, [Chapter 4](https://jhwatrous.github.io/TQI.4.pdf) | Recognize the Gaussian channel as a Schur channel. |
| Universal converse | §§6.1.1–6.1.2, [Chapter 6](https://jhwatrous.github.io/TQI.6.pdf) | Separability and local operations support the comparison argument. |
| Optional independent-use corollary | §5.2, [Chapter 5](https://jhwatrous.github.io/TQI.5.pdf); §§8.2.1–8.2.2, [Chapter 8](https://jhwatrous.github.io/TQI.8.pdf) | Entropy, coherent information and asymptotic quantum capacity. |

The first six rows support background milestones M01–M11 and the one-register proof. The last row supports M28–M29 only. Dynamic programming and the explicit reversible compiler are supplied in [the construction](../science/encoder.md), not assigned to an unrelated textbook chapter.

## Notation and operational translation

| Convention | Translation used here |
|---|---|
| Vectors and adjoints | Watrous's $`u`$, $`uv^*`$, and $`B^*`$ correspond to $`\lvert u\rangle`$, $`\lvert u\rangle\langle v\rvert`$, and $`B^\dagger`$. |
| Choi normalization | Both use unnormalized $`J(\Phi)`$. A channel with input dimension $`d`$ has $`\operatorname{Tr}J(\Phi)=d`$; $`J(\Phi)/d`$ is its normalized Choi state. |
| Channel norm | Watrous's completely bounded trace norm, written with triple bars and subscript one, is our $`\lVert\Gamma\rVert_\diamond`$. Our error is **half** that norm: $`\frac12\lVert\Lambda-\operatorname{id}\rVert_\diamond`$. |
| Fidelity | Watrous defines $`F(\rho,\sigma)=\lVert\sqrt\rho\sqrt\sigma\rVert_1`$. Our $`F_e=\langle\Omega_D\rvert\rho_{\rm out}\lvert\Omega_D\rangle`$ is an overlap without a square root: $`F_e=F(\rho_{\rm out},\lvert\Omega_D\rangle\langle\Omega_D\rvert)^2`$. |
| Dimensions and qubits | $`d`$ is physical dimension, $`D`$ logical dimension, and $`\lfloor\log_2D\rfloor`$ whole logical qubits. The compiler uses band population $`N`$ and selects $`K=2^{\lfloor\log_2N\rfloor}`$ codewords. |
| Schur matrix and noise operator | The multiplier called $`A`$ in Watrous §4.1.3 corresponds to our $`G_t`$. Our Hermitian $`A`$ instead determines $`\mathcal L_A=-[A,[A,\cdot]]/2`$ and $`\Phi_t=e^{t\mathcal L_A}`$. |
| One register and capacity | $`D_\epsilon(t;A)`$ concerns one storage interval. $`Q(\Phi_t)`$ and $`Q_{\leftrightarrow}(\Phi_t)`$ concern asymptotically many independent complete uses, measured in qubits per use. |

Explicitly, the Choi convention is

```math
J(\Phi)=\sum_{i,j}\Phi(|i\rangle\langle j|)\otimes|i\rangle\langle j|.
```

Changing tensor-factor order requires a swap, not a normalization factor. The maximally entangled target $`|\Omega_D\rangle=D^{-1/2}\sum_a|a\rangle|a\rangle`$ is normalized.

The [model](../science/model.md) permits a retained classical record and includes every instrument outcome. The true couplings are fixed throughout the storage interval. Only the physical memory survives quantumly through storage: no retained quantum workspace, bath record, preshared entanglement or intermediate intervention is supplied. The reference in the error criterion is inaccessible, not an extra storage resource.

## Bridge from the book to the project

**First, identify the finite-time geometry.** In an eigenbasis of the noise operator,

```math
\Phi_t(X)=G_t\odot X,\qquad
(G_t)_{ij}=e^{-t(\lambda_i-\lambda_j)^2/2}.
```

For $`t\gt0`$, the dimensionless quantity $`t(\lambda_i-\lambda_j)^2`$ determines coherence attenuation. Counting eigenvectors in a width $`t^{-1/2}`$ interval gives $`M_t`$, with multiplicities included. This counts a near-degenerate cluster; exact degeneracy is unnecessary at finite time. The approximate occupancy theorem assumes $`0\lt\epsilon\lt1/4`$.

**Second, turn a cluster into reference-stable protection.** Watrous's norm tools allow auxiliary systems, but a dimension-independent estimate still needs proof. [Lemma 1](../science/spectral_law.md#lemma-1-reference-stable-protection-of-a-spectral-interval) centers an interval of diameter $`a`$, bounds the double-commutator generator, and integrates its semigroup to obtain half-diamond error at most $`ta^2/4`$. Subdivision supplies a sufficiently narrow populated interval. Bounding individual matrix entries alone would not establish this channel guarantee.

**Third, rule out better general encoders.** Choi positivity from Watrous §2.2.2 converts $`G_t\preceq\mu I`$, with $`\mu=\lambda_{\max}(G_t)`$, into $`\Phi_t\le_{\rm CP}\mu\Delta`$, where $`\Delta`$ completely dephases the eigenbasis. [Lemma 2](../science/spectral_law.md#lemma-2-a-converse-for-arbitrary-encoding-and-classical-records) propagates this order through arbitrary encoders and conditional recoveries. The comparison output is separable even with input-dependent classical records, so its maximally entangled overlap is at most $`1/D`$. Thus $`D\le\mu/(1-\epsilon)`$. The separate Gaussian row estimate gives $`\mu\le(2+\sqrt{2\pi})M_t`$. Together with protection, this proves $`\log_2D_\epsilon=\log_2M_t+O_\epsilon(1)`$ at fixed positive error.

**Finally, make the code executable.** For $`A=\sum_jg_jN_j`$, with $`N_j=|1\rangle\langle1|_j`$, [the compiler](../science/encoder.md) rounds certified coefficient estimates to an exact dyadic grid. It finds a populated integer-sum band by dynamic programming, then coherently ranks and unranks accepted strings. Reversing intermediate computations cleans all temporary workspace before storage. Explicit lookup gates and bit arithmetic establish polynomial resources under the stated parameter scaling. The precision certificate is an input assumption, not a claim about calibration sample cost.

This construction loses only a constant number of qubits relative to the all-code optimum at fixed error. Neither the occupancy theorem nor this calibration-to-circuit conclusion is attributed to the textbook.

## Worked example: one logical qubit without an exact degeneracy

Take two physical qubits with nominal operator

```math
A=N_1+\frac{33}{32}N_2,\qquad t=16,\qquad\epsilon=\frac1{16}.
```

The eigenvalues are $`0,1,33/32,65/32`$. They are all distinct, but the middle pair lies within the resolution width $`1/\sqrt t=1/4`$, so $`M_t=2`$.

Supply estimates $`(1,33/32)`$ with certified uncertainties $`u_1=u_2=1/256`$. The compiler chooses $`\delta=1/128`$, rounded weights $`(128,132)`$, and integer width $`B=4n=8`$. The smallest maximizing closed band is $`[124,132]`$. It selects $`|01\rangle,|10\rangle`$, giving population two and one logical qubit.

Here the selected isometry has a direct two-gate realization. Starting with $`|\psi\rangle|0\rangle`$, a CNOT from qubit one to two followed by $`X`$ on qubit two implements

```math
\alpha|0\rangle+\beta|1\rangle
\longmapsto\alpha|01\rangle+\beta|10\rangle.
```

The inverse gates decode after storage. Only the two physical qubits cross the interval; the second qubit returns to zero after decoding.

At the nominal coefficients, the selected eigenvalue gap is $`1/32`$. The logical channel is exactly

```math
\Lambda(\rho)=(1-p)\rho+pZ\rho Z,\qquad
p=\frac{1-e^{-1/128}}2\approx0.00389103.
```

Here $`Z=\operatorname{diag}(1,-1)`$ acts on the decoded logical qubit. Its half-diamond error is exactly $`p`$: the norm triangle inequality gives the upper bound, and input $`|+\rangle`$ attains it. Measuring that decoded input in the $`X`$ basis returns the minus outcome with probability $`p`$; a maximally entangled input has target overlap $`1-p`$.

For every fixed coefficient vector consistent with the supplied certificates, the compiler's conservative storage bound is instead $`9\epsilon/16=9/256`$. The nominal exact value and robust bound answer different questions. This is finite-time approximate protection: the nondegenerate nominal operator has exact storage dimension one at every positive exposure, as [Proposition 2](../science/spectral_law.md#proposition-2-exact-storage-at-every-positive-time) establishes. The example demonstrates a functioning band code, without claiming its optimality from these small numbers alone.

[Milestone map](milestones.md) · [Scientific overview](../science/README.md) · [Repository overview](../README.md)
