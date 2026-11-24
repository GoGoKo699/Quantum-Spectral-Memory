# Spectral memory with several commuting noise directions

For one Gaussian noise direction, counting eigenvalues in a narrow interval estimates the optimal stored dimension within a constant number of qubits. With several directions, the analogous count uses a ball in the joint spectrum. The ball count still controls storage at fixed rank. As the rank grows, terminal quantum error correction can store many qubits even when every ball contains only one spectral point.

## Model and result

Use the [deterministic storage model](model.md) and the same reference-sensitive half-diamond error criterion. During a single storage interval the finite register experiences random phases from known commuting Hermitian operators $`A_1,\ldots,A_m`$. Let $`\lambda_i\in\mathbb R^m`$ be their joint eigenvalue vectors in a common eigenbasis, listed with multiplicity, and let $`\Sigma\succeq0`$ be the Gaussian phase covariance, including exposure. A known mean phase can be undone at the terminal boundary, so assume zero mean. The Gaussian characteristic function gives

```math
\Phi(|i\rangle\langle j|)
= G_{ij}|i\rangle\langle j|,
\qquad
G_{ij}=e^{-\|z_i-z_j\|^2/2},
\qquad
z_i=\Sigma^{1/2}\lambda_i.
\qquad\text{(R1)}
```

Take $`r`$ to be the dimension of the affine span of the $`z_i`$, identifying that span isometrically with $`\mathbb R^r`$. This removes noise directions that act as scalars or carry redundant signatures. The case $`r=0`$ is the identity channel. For $`r\ge1`$ define

```math
M=\max_{c\in\mathbb R^r}\#\{i:\|z_i-c\|\le1\},
\qquad
C_r=\sum_{j=0}^\infty(2j+3)^r e^{-j^2/2}.
\qquad\text{(R2)}
```

The ball is closed, and $`M`$ counts multiplicity. Let $`D_\epsilon`$ be the optimal deterministic stored dimension for arbitrary endpoint encoding and recovery, including any retained classical record. All logarithms below that measure stored dimension are base two.

For $`0\lt\epsilon\lt1/4`$ and every finite joint spectrum,

```math
\left\lceil\frac{M}{(1+2/\epsilon)^r}\right\rceil
\le D_\epsilon\le\frac{\lambda_{\max}(G)}{1-\epsilon}
\le\frac{M C_r}{1-\epsilon}.
\qquad\text{(R3)}
```

For each fixed $`\epsilon`$, the supremum of $`\log_2D_\epsilon-\log_2M`$ over finite joint spectra of affine rank $`r`$ is

```math
\frac r2\log_2 r+O_\epsilon(r).
\qquad\text{(R4)}
```

The lower bound in (R3) uses one small spectral subspace. The spectra witnessing (R4) have $`M=1`$. Their codes use superpositions of separated spectral points and a terminal recovery. The [one-direction theorem](spectral_law.md) still gives the sharper constants for the original width-one interval in normalized coordinates. The two conventions at rank one differ by at most a factor of two in occupancy because a unit ball there has width two.

## The ball-code guarantee and the arbitrary-code converse

We use the following Euclidean covering bound. A ball of radius $`R`$ in $`\mathbb R^r`$ is coverable by at most $`(1+2R/a)^r`$ balls of radius $`a`$. Indeed, choose a maximal $`a`$-separated set in the larger ball. Balls of radius $`a/2`$ around the chosen points have disjoint interiors and fit inside the ball of radius $`R+a/2`$. Their volumes bound the number of points, and maximality gives the cover. This works for arbitrary centers and finite spectra with repeated eigenvalues.

For the lower bound, cover a unit ball achieving $`M`$ by balls of radius $`\epsilon`$. One of those contains at least $`\lceil M/(1+2/\epsilon)^r\rceil`$ eigenvectors. Center those signatures at the center of the small ball, obtaining $`\|z_i\|\le\epsilon`$ on that subset. The shift leaves its Gaussian channel unchanged.

For real $`z\in\mathbb R^r`$ define a unit vector indexed by multi-indices $`\alpha\in\mathbb Z_{\ge0}^r`$,

```math
|e(z)\rangle
=e^{-\|z\|^2/2}
  \sum_{\alpha\in\mathbb Z_{\ge0}^r}
  \frac{z^\alpha}{\sqrt{\alpha!}}|\alpha\rangle,
\qquad
\langle e(w)|e(z)\rangle=e^{-\|z-w\|^2/2}.
\qquad\text{(R5)}
```

Here $`z^\alpha=\prod_a z_a^{\alpha_a}`$, and $`\alpha!=\prod_a\alpha_a!`$. The overlap follows by summing the exponential series in each coordinate. These are coherent-state vectors, used only to express the channel's Stinespring isometry $`|i\rangle\mapsto |i\rangle|e(z_i)\rangle`$. The ideal isometry on the chosen spectral subspace uses the same system vectors with the environment fixed to $`|e(0)\rangle`$. The operator norm of the isometry difference is the largest norm of the difference in environment vectors over the chosen $`i`$, because the system vectors are orthogonal. Thus

```math
\max_i\lVert |e(z_i)\rangle-|e(0)\rangle\rVert
=\max_i\sqrt{2-2e^{-\|z_i\|^2/2}}
\le\epsilon .
\qquad\text{(R6)}
```

For isometries $`V,W`$ into the same system and environment, the reduced channels differ in half diamond norm by at most $`\|V-W\|`$. To see this, expand the difference of $`VXV^\dagger`$ and $`WXW^\dagger`$ into two terms and bound the trace norm after adjoining any reference. Partial trace and the final recovery are contractions. Applying this observation to (R6) gives the first inequality in (R3), with the subspace decoder from [Lemma 1 of the scalar proof](spectral_law.md#lemma-1-reference-stable-protection-of-a-spectral-interval).

For the converse, the [Schur-channel comparison in Lemma 2](spectral_law.md#lemma-2-a-converse-for-arbitrary-encoding-and-classical-records) applies to (R1). The Gaussian matrix in (R1) is a Gram matrix by (R5). With $`\mu=\lambda_{\max}(G)`$, one has $`\Phi\le_{\rm CP}\mu\Delta`$, where $`\Delta`$ deletes all off-diagonals. After arbitrary encoding and recovery, the comparison output for a maximally entangled input is separable across the reference and the recovered register, even with the retained classical record. Its overlap with the target is at most $`1/D`$. The true overlap is at most $`\mu/D`$ and must be at least $`1-\epsilon`$. This proves the middle bound in (R3).

For the final inequality, fix a row $`i`$ and group the other indices, including $`i`$ itself, by $`j\le\|z_i-z_k\|\lt j+1`$. Each shell lies in the radius-$`(j+1)`$ ball around $`z_i`$. By the covering bound, it contains at most $`M(2j+3)^r`$ indices. An entry in that shell is at most $`e^{-j^2/2}`$, so the Gaussian row sum is at most $`M C_r`$. The matrix is nonnegative entrywise, and its largest eigenvalue is bounded by its maximum row sum. For an explicit estimate, use

```math
\begin{aligned}
(2j+3)^r e^{-j^2/4}
&\le 3^r\,2^{r/2}(j^2+1)^{r/2}e^{-j^2/4}\\
&\le e^{1/4}\bigl(6\sqrt{r/e}\bigr)^r .
\end{aligned}
```

The first step uses $`2j+3\le3(j+1)`$ and $`(j+1)^2\le2(j^2+1)`$. For the second, maximize $`x^{r/2}e^{-x/4}`$ at $`x=2r`$. Since $`\sum_{j\ge0}e^{-j^2/4}\le1+\sqrt\pi`$,

```math
C_r\le e^{1/4}(1+\sqrt\pi)\bigl(6\sqrt{r/e}\bigr)^r .
\qquad\text{(R7)}
```

Equations (R3) and (R7) prove the upper side of (R4).

## A joint spectrum that needs error correction

### Separated signatures

For integer $`r\ge9`$, take a maximal set of points with pairwise distance at least three in the closed ball about the origin of radius $`\sqrt r`$. Start with the points $`0,\sqrt r\,e_1,\ldots,\sqrt r\,e_r`$, where $`e_a`$ are coordinate unit vectors, to ensure affine rank $`r`$. The volume of the disjoint radius-$`3/2`$ interiors around the points bounds the size of any such set, so a greedy extension can stop with a finite maximal set. The radius-three balls around the points cover the original ball. Volume comparison gives

```math
d\ge(\sqrt r/3)^r,\qquad M=1.
\qquad\text{(R8)}
```

Use these points as the normalized signatures of a $`d`$-dimensional register. They define a commuting Gaussian channel by taking the $`r`$ observables diagonal in the chosen eigenbasis and choosing identity phase covariance.

For these signatures, any code whose range is spanned by a subset of at least two joint eigenvectors fails at the target error, even with a general terminal recovery. Equal superpositions of two selected eigenvectors with opposite relative signs are orthogonal inputs, but after (R1) their trace distance is at most $`e^{-9/2}`$. Recovery cannot increase it. To recover both with half-diamond error at most $`\epsilon`$, their output trace distance would have to be at least $`1-2\epsilon`$, by the triangle inequality. This is impossible for $`\epsilon\lt1/4`$.

### Truncating the environment vectors

Let $`P_L`$ be the projection onto $`|\alpha|=\sum_a\alpha_a\le L`$ in (R5), and let $`|\widetilde e_i\rangle`$ be the normalized projection of $`|e(z_i)\rangle`$ onto its range. The zero index ensures nonzero norm. The squared norm removed by the projection is

```math
q_i=\Pr[X_i>L],
\qquad
X_i\sim\mathrm{Poisson}(\|z_i\|^2).
```

This follows by summing the squared coefficients of fixed total degree with the multinomial theorem. For $`\|z_i\|^2\le r`$, Markov's inequality for $`2^{X_i}`$ gives $`q_i\le e^r2^{-L-1}`$. In particular,

```math
L=\left\lceil 2r+\log_2(2/\epsilon^2)\right\rceil
\quad\Longrightarrow\quad
\max_i q_i\le\epsilon^2/2.
\qquad\text{(R9)}
```

The truncated channel $`\widetilde\Phi`$ is defined by the isometry $`|i\rangle\mapsto |i\rangle|\widetilde e_i\rangle`$. Both dilations can be represented in the same environment. Their distance and the induced channel error satisfy

```math
\frac12\|\Phi-\widetilde\Phi\|_\diamond
\le\max_i\lVert |e(z_i)\rangle-|\widetilde e_i\rangle\rVert
=\max_i\sqrt{2-2\sqrt{1-q_i}}
\le\epsilon .
\qquad\text{(R10)}
```

The truncated environment dimension is $`k=\binom{r+L}{r}\le2^{r+L}`$. This dimension bounds the proof representation. The code will access only the noisy system register.

### A deterministic code for the truncated channel

Apply Tverberg's theorem to the $`d`$ matrices $`|\widetilde e_i\rangle\langle\widetilde e_i|`$, regarded as points in the affine real space of unit-trace Hermitian $`k\times k`$ matrices, of dimension $`k^2-1`$. Since $`d\ge (K-1)k^2+1`$ for $`K=\lceil d/k^2\rceil`$, there are $`K`$ disjoint index sets $`S_\ell`$ and probability weights $`p_{\ell i}`$ such that the weighted mixtures in all sets equal the same state $`\omega`$. Equivalently, this is the [diagonal error-space construction in Weaver's Lemma 2.9](https://arxiv.org/abs/1802.07394), following earlier work by [Knill, Laflamme and Viola](https://arxiv.org/abs/quant-ph/9908066).

Encode in orthonormal vectors $`|c_\ell\rangle=\sum_{i\in S_\ell}\sqrt{p_{\ell i}}|i\rangle`$. The complementary channel of $`\widetilde\Phi`$ keeps only diagonal entries in this physical basis. On encoded matrix units it therefore satisfies

```math
\widetilde\Phi^{\,c}(|c_\ell\rangle\langle c_{\ell'}|)
=\delta_{\ell\ell'}\omega.
\qquad\text{(R11)}
```

The condition gives exact recovery on this subspace. Concretely, write $`\omega=\sum_{s:\nu_s>0}\nu_s|u_s\rangle\langle u_s|`$ and form the Kraus operators $`A_s`$ of the encoded system channel by taking the $`\langle u_s|`$ components of the encoded isometry. Equation (R11) implies $`A_s^\dagger A_{s'}=\nu_s\delta_{ss'}I_K`$. Components in the zero-eigenvalue space vanish. Thus $`W_s=A_s/\sqrt{\nu_s}`$ are isometries with orthogonal ranges. Recovery applies $`W_s^\dagger`$ on each such range and sends the complement to any fixed logical state, which defines a trace-preserving decoder. The encoder and decoder are chosen once, with no postselection and no operation during storage. By (R10) the same fixed code for the actual channel satisfies the target half-diamond error.

Finally, (R8)–(R11) give

```math
\begin{aligned}
\log_2D_\epsilon
&\ge \log_2d-2\log_2k\\
&\ge \frac r2\log_2r-r\log_2 3-2(r+L)\\
&=\frac r2\log_2r-O_\epsilon(r).
\end{aligned}
\qquad\text{(R12)}
```

This establishes the other side of (R4) with $`M=1`$. Tverberg's theorem and the finite-channel recovery are inherited coding steps. The Gaussian cutoff estimate, together with the high-dimensional packing and the converse, gives the sharp coefficient of $`r\log r`$.

## A finite example with local noise

For $`r=151`$ physical qubits, take $`z_x=sx`$ for $`x\in\{0,1\}^r`$ and $`s=\sqrt{2\ln8}>2`$. Independent Gaussian fields couple to the local projectors $`s|1\rangle\langle1|_a`$. The joint spectrum again has $`M=1`$. The channel multiplies a computational-basis off-diagonal by $`(1/8)^{d_{\rm H}(x,y)}`$, where $`d_{\rm H}`$ is Hamming distance. It is exactly the product of single-qubit Pauli $`Z`$ errors of probability $`p=7/16`$, because $`1-2p=1/8`$.

Encode one qubit in the two basis vectors $`|+\rangle^{\otimes r}`$ and $`|-\rangle^{\otimes r}`$. Standard binary repetition-code syndrome recovery in the $`X`$ basis changes the logical symbol precisely when more than half the physical qubits have flipped. The syndrome can distinguish an error pattern only up to its complement. Correcting the lower-weight one preserves the encoded coherence and leaves a logical Pauli $`X`$ error for the higher-weight one. The half-diamond error equals the probability of this logical error, since the identity and logical $`X`$ are perfectly distinguishable channels. The resulting error at $`r=151`$ is

```math
\sum_{j=76}^{151}\binom{151}{j}
 \left(\frac{7}{16}\right)^j
 \left(\frac9{16}\right)^{151-j}
=0.06121720444\ldots\lt\frac1{16}.
\qquad\text{(R13)}
```

The comparison can be evaluated by integer arithmetic with common denominator $`16^{151}`$. For a code spanned by joint eigenvectors, the two-sign superposition test above gives a recovered trace distance at most $`1/8`$, well below the required $`1-2/16`$. This establishes a separation for a simple local realization. Equations (R7) and (R12) give the coefficient in (R4) over arbitrary finite commuting spectra.

## Interpretation and scope

The ball count is a reliable storage estimate when the effective noise rank is fixed. It supplies a constructive subspace guarantee at every rank. For the separated spectra, each resolution ball holds just one eigenvector. At large rank there are far more eigenvectors than the dimension required to approximate the environment outputs. An endpoint code can give several orthogonal logical states the same compressed environment output by assigning different superpositions with matching environment mixtures.

The fixed positive error matters. For zero error, joint eigenvectors with identical signatures form exact noiseless subspaces. Distinct joint signatures have a strictly positive definite Gaussian Gram matrix. Its quadratic form is the Gaussian average of a squared finite exponential sum. The Gaussian measure has full support, and restricting that sum to a line whose direction separates the finitely many signatures gives linearly independent exponentials. Applying [the scalar exact-error argument](spectral_law.md#proposition-2-exact-storage-at-every-positive-time) to the distinct joint signature blocks then gives exact stored dimension equal to the largest joint multiplicity.

All physical system carriers count. The endpoint operations in the theorem are ideal, and the signatures and phase covariance are supplied. The environment vectors in (R5) are a mathematical representation. The scheme requires neither added bosonic carriers nor access to the actual environment. Finding the Tverberg partition and its weights, and implementing the exact endpoint maps, can be costly. The result for arbitrary commuting observables establishes a storage-dimension law with no efficiency, calibration, or local gate guarantee. The [existing calibrated compiler](encoder.md) treats one known noise direction with additive qubit couplings.

The channel comparison with complete dephasing follows the scalar account's use of established completely positive ordering techniques. Singh and Datta's [storage theorem](https://arxiv.org/html/2504.10436v2) treats finite-time convergence toward an asymptotic peripheral-space characterization. Aydin, Albert and Barg use [Tverberg geometry for spin, bosonic and permutation-invariant codes](https://doi.org/10.1103/kx3b-4nrp). Here the finite-time objective is the largest possible failure of joint ball occupancy to estimate unrestricted storage, with matching rank dependence and a code for one Gaussian storage interval. The [related-work account](../references/related_work.md) gives further comparisons.

[Scientific overview](README.md) · [Repository overview](../README.md) · [Related work](../references/related_work.md)
