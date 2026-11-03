# The finite-time spectral occupancy law

All logarithms in information quantities are base two. Let $`A=A^\dagger`$ act on a $`d`$-dimensional memory, let $`\Phi_t=e^{-t[A,[A,\cdot]]/2}`$, and use the code class and error criterion defined in the operational model.

## Theorem 1: one-register storage

For $`t\gt 0`$ and $`0\lt \epsilon\lt 1/4`$, set

```math
M_t=\max_x\#\{i:\lambda_i\in[x,x+t^{-1/2}]\},\qquad
k_\epsilon=\left\lceil\frac1{2\sqrt\epsilon}\right\rceil,
\qquad C=2+\sqrt{2\pi}.
```

Then

```math
\boxed{
\left\lceil\frac{M_t}{k_\epsilon}\right\rceil
\le D_\epsilon(t;A)
\le \frac{\lambda_{\max}(G_t)}{1-\epsilon}
\le \frac{CM_t}{1-\epsilon},
}
\qquad\text{(S1)}
```

where

```math
(G_t)_{ij}=e^{-t(\lambda_i-\lambda_j)^2/2}.
\qquad\text{(S2)}
```

In particular,

```math
-\log_2k_\epsilon
\le\log_2D_\epsilon(t;A)-\log_2M_t
\le\log_2\frac{C}{1-\epsilon}.
\qquad\text{(S3)}
```

The constants are uniform in dimension, exposure, degeneracies, and spacings. They are not optimized. The statement concerns fixed positive error; the error dependence in (S3) is not claimed sharp as $`\epsilon\downarrow0`$.

### Lemma 1: reference-stable protection of a spectral interval

Suppose a subspace $`P S`$ is spanned by eigenvectors whose eigenvalues lie in an interval of diameter $`a\ge0`$. There is a subspace encoder and a trace-preserving terminal decoder for which

```math
\frac12\|\Lambda_t-\mathrm{id}_{\mathrm{rank}P}\|_\diamond
\le \min\{1,ta^2/4\}.
\qquad\text{(S4)}
```

**Proof.** Let $`V:\mathbb C^{\mathrm{rank}P}\to S`$ be an isometry with range $`P S`$. The encoded subspace is invariant under $`\Phi_t`$. Subtract the midpoint of its spectral interval from $`V^\dagger A V`$, obtaining a Hermitian $`B`$ with $`\|B\|\le a/2`$. Scalar shifts leave the double commutator unchanged.

For every ancillary register and trace-class operator $`X`$, left and right multiplication satisfy

```math
\|(B\otimes I)X(B\otimes I)\|_1\le\|B\|^2\|X\|_1,
```

and the two terms involving $`B^2`$ obey the corresponding bounds. Therefore

```math
\|\mathcal L_B\|_\diamond\le 2\|B\|^2\le a^2/2.
\qquad\text{(S5)}
```

The semigroup $`e^{s\mathcal L_B}`$ is a channel, so its diamond norm is one. Integrating the derivative gives

```math
e^{t\mathcal L_B}-\mathrm{id}
=\int_0^t e^{s\mathcal L_B}\mathcal L_B\,ds,
\qquad
\frac12\|e^{t\mathcal L_B}-\mathrm{id}\|_\diamond
\le ta^2/4.
\qquad\text{(S6)}
```

Use $`\mathcal E(X)=VXV^\dagger`$ and, for an arbitrary fixed logical density operator $`\tau_0`$,

```math
\mathcal R(Y)=V^\dagger YV+\mathrm{Tr}[(I-P)Y]\,\tau_0.
\qquad\text{(S7)}
```

This is a completely positive trace-preserving extension of the inverse embedding. The encoded channel has support inside $`P S`$, so $`\mathcal R\Phi_t\mathcal E=e^{t\mathcal L_B}`$. This proves (S4), including arbitrary inaccessible references. The bound by one is the general maximum half-diamond distance between channels. $`\square`$

### Achievability in Theorem 1

Choose a closed interval of width $`w_t=t^{-1/2}`$ containing $`M_t`$ eigenvalues. Divide it into $`k_\epsilon`$ equal cells, assigning every boundary eigenvector to one cell. Some cell contains at least $`\lceil M_t/k_\epsilon\rceil`$ eigenvectors and has diameter at most

```math
\frac{w_t}{k_\epsilon}\le2\sqrt{\epsilon/t}.
```

Lemma 1 protects their span with error at most $`\epsilon`$. This proves the first inequality in (S1). The construction uses no retained record and no noise estimation during storage.

### Lemma 2: a converse for arbitrary encoding and classical records

Let $`\Phi_G(X)=G\odot X`$ be any Schur channel, so $`G\succeq0`$ and $`G_{ii}=1`$. Let $`\Delta(X)=\sum_i|i\rangle\langle i|X|i\rangle\langle i|`$ be complete dephasing in that basis. If $`\mu=\lambda_{\max}(G)`$, every allowed $`D`$-dimensional storage code obeys

```math
F_e\le\frac{\mu}{D},
\qquad\text{(S8)}
```

where $`F_e=\langle\Omega_D|\rho_{RQ}^{\rm out}|\Omega_D\rangle`$ and $`\left|\Omega_D\right\rangle=D^{-1/2}\sum_{a=1}^D|a\rangle_R|a\rangle_Q`$. This is the overlap with a pure maximally entangled target, without a square root.

**Proof.** Use unnormalized Choi matrices. On the subspace spanned by $`\{|i\rangle\otimes|i\rangle\}_{i=1}^d`$, the Choi matrices of $`\Phi_G`$ and $`\Delta`$ are respectively $`G`$ and $`I_d`$, and both vanish on its orthogonal complement. Hence

```math
\Phi_G\le_{\rm CP}\mu\Delta,
\qquad\text{(S9)}
```

meaning that $`\mu\Delta-\Phi_G`$ is completely positive.

Apply the encoder instrument $`\{\mathcal E_c\}`$ to the logical half of $`|\Omega_D\rangle\langle\Omega_D|`$, producing subnormalized states $`\rho_{RS}^{(c)}\ge0`$ with total trace one. Applying (S9), then the conditional recovery, and summing all outcomes yields

```math
\rho_{RQ}^{\rm out}\le\mu\sigma_{RQ},
\qquad
\sigma_{RQ}:=\sum_c(\mathrm{id}_R\otimes\mathcal R_c\Delta)(\rho_{RS}^{(c)}).
\qquad\text{(S10)}
```

The comparison state $`\sigma_{RQ}`$ is normalized and separable. Explicitly, set

```math
X_{ci}:=(I_R\otimes\langle i|)\rho_{RS}^{(c)}(I_R\otimes|i\rangle)\succeq0,
\qquad
\tau_{ci}:=\mathcal R_c(|i\rangle\langle i|).
```

Then

```math
\sigma_{RQ}=\sum_{c,i}X_{ci}\otimes\tau_{ci},
\qquad \sum_{c,i}\mathrm{Tr}X_{ci}=1.
\qquad\text{(S11)}
```

Here every $`\tau_{ci}`$ is a density operator. This explicitly includes a retained record whose distribution depends on the unknown input. For normalized product states $`\alpha\otimes\beta`$,

```math
\langle\Omega_D|\alpha\otimes\beta|\Omega_D\rangle
=D^{-1}\mathrm{Tr}(\alpha^{\mathsf T}\beta)\le D^{-1}.
```

Convexity gives the same upper bound for $`\sigma_{RQ}`$. Taking the maximally entangled overlap in (S10) proves (S8). Instrument integrals obey the same positive-operator argument. $`\square`$

If a code has half-diamond error at most $`\epsilon`$, then

```math
1-F_e\le\tfrac12\|\rho_{RQ}^{\rm out}-|\Omega_D\rangle\langle\Omega_D|\|_1\le\epsilon.
\qquad\text{(S12)}
```

Combining (S8)–(S12) gives $`D\le\mu/(1-\epsilon)`$. Since $`G\succeq0`$ has trace $`d`$, $`\mu\le d`$, proving the dimension bound in the model as well. No assertion that an optimal encoder selects eigenvectors is used in this converse.

### Lemma 3: Gaussian row sums from local occupancy

For $`G_t`$ in (S2),

```math
\lambda_{\max}(G_t)\le CM_t,
\qquad C=2+\sqrt{2\pi}.
\qquad\text{(S13)}
```

**Proof.** Fix $`i`$ and write $`y_j=\sqrt t(\lambda_j-\lambda_i)`$. For $`k=0,1,\ldots`$, each of the intervals $`[k,k+1)`$ and $`(-k-1,-k]`$ contains at most $`M_t`$ of the $`y_j`$, counting multiplicity. Their union covers the line; only zero is counted twice. On either interval $`e^{-y_j^2/2}\le e^{-k^2/2}`$. Therefore

```math
\sum_j(G_t)_{ij}
\le2M_t\sum_{k=0}^\infty e^{-k^2/2}
\le2M_t\left(1+\int_0^\infty e^{-u^2/2}\,du\right)
=CM_t.
\qquad\text{(S14)}
```

The spectral radius of a matrix with nonnegative entries is at most its maximum row sum. Since $`G_t\succeq0`$, its spectral radius is $`\lambda_{\max}(G_t)`$. This proves (S13) and completes Theorem 1. $`\square`$

## Boundary cases

At $`t=0`$, the channel is the identity; (M9) is not needed. If $`A`$ is scalar, the channel is the identity for every $`t`$, and $`M_t=d`$. In either case a $`d`$-dimensional code is exact and every positive-error code obeys $`D\le d/(1-\epsilon)`$. For an $`n`$-qubit physical register and $`\epsilon\lt 1/2`$, exactly $`n`$ whole logical qubits can be stored.

Repeated eigenvalues and interval endpoints require no limiting argument: they are covered by the multiplicity and assignment conventions above. A one-dimensional code always exists, even when the displayed real-valued lower bounds are less than one. Whole-qubit statements follow by restricting a feasible code and taking a logarithm floor, losing less than one qubit.

The case $`\epsilon=0`$ has a different, exact description. It is useful for distinguishing finite-time approximate storage from an exact noiseless subspace.

### Proposition 2: exact storage at every positive time

Let $`m_*`$ be the largest eigenvalue multiplicity of $`A`$. Then

```math
D_0(t;A)=m_*,\qquad t\gt 0.
\qquad\text{(S15)}
```

**Proof.** Write the distinct eigenvalues as $`\nu_1,\ldots,\nu_\ell`$, with spectral projectors $`P_\alpha`$, and define block dephasing

```math
\Pi_A(X)=\sum_{\alpha=1}^{\ell}P_\alpha X P_\alpha.
```

The $`\ell\times\ell`$ Gaussian matrix $`H_{\alpha\beta}=e^{-t(\nu_\alpha-\nu_\beta)^2/2}`$ is strictly positive definite. Indeed, its quadratic form is the Gaussian integral of the squared modulus of a finite sum of exponentials with distinct frequencies. Such a sum vanishes almost everywhere only if all coefficients vanish, by linear independence of the exponentials.

Let $`\eta=\lambda_{\min}(H)\gt 0`$. If $`T:\mathbb C^\ell\to\mathbb C^d`$ maps $`|\alpha\rangle`$ to the sum of the eigenbasis vectors in its eigenspace, then the Choi-support matrices of $`\Phi_t`$ and $`\Pi_A`$ are $`THT^\dagger`$ and $`TT^\dagger`$. Thus $`\Phi_t\ge_{\rm CP}\eta\Pi_A`$. Since $`\eta\le1`$, either $`\Phi_t=\Pi_A`$, or

```math
\Phi_t=\eta\Pi_A+(1-\eta)\Theta
```

for a channel $`\Theta`$. If an allowed encoder and recovery make $`\Phi_t`$ exactly the logical identity, the same convex decomposition holds for the resulting logical channels. The identity channel has a rank-one Choi matrix and is an extreme channel, so the same code must correct $`\Pi_A`$ exactly. This conclusion also holds for an encoding instrument after summing its branches.

The correlation matrix of $`\Pi_A`$ consists of all-one blocks of sizes $`\mathrm{rank}P_\alpha`$, and hence has maximum eigenvalue $`m_*`$. Lemma 2 with $`F_e=1`$ now gives $`D\le m_*`$. Encoding in a largest eigenspace attains equality. $`\square`$

## Attribution of the converse method

Comparison with an entanglement-breaking channel and completely positive order are established methods. In particular, Bardet et al., [arXiv:1904.11043v2](https://arxiv.org/html/1904.11043v2), Theorem V.1 and Lemma VI.8, use entanglement measures and Choi-based CP ordering for Markov-semigroup capacity bounds. Singh and Datta, [arXiv:2504.10436v2](https://arxiv.org/html/2504.10436v2), Theorem 3.1, develop the general long-time storage characterization. The proofs here give the explicit finite-spectrum occupancy estimate and its constants without requiring closeness to the infinite-time channel.

[Scientific overview](README.md) · [Repository overview](../README.md) · [Related work](../references/related_work.md)
