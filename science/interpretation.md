# Consequences and operational interpretation

## What the spectral law determines

At exposure $`t`$, the Gaussian dephasing factor resolves eigenvalue separations on the scale $`t^{-1/2}`$. Theorem 1 shows that the largest number $`M_t`$ of eigenvectors in one interval at that resolution determines the recoverable logical dimension within multiplicative constants at fixed error. Equivalently, it determines the number of stored logical qubits within additive constants.

This statement includes a converse against every allowed mixed encoder, terminal recovery, and retained classical record. It does not require an optimal code to be a spectral subspace. A narrow spectral subspace is a sufficient construction; the converse establishes that more general codes cannot improve the number of logical qubits by more than the stated constant. The constant depends on the allowed error, so the theorem does not characterize the optimal dependence on error as that error tends to zero.

For a general many-body operator, evaluating the full spectrum or implementing an eigenbasis can be difficult. The spectral law is an information-theoretic characterization. The calibrated band construction supplies an efficient encoder for the particular explicitly given family

```math
A=\sum_{j=1}^ng_jN_j,\qquad N_j=|1\rangle\langle1|_j.
\tag{I1}
```

Its guarantee is relative to the optimum for the actual couplings, even though the compiler uses only estimates with a certified finite error.

## A rate bound from spectral variance

Let

```math
\bar\lambda=d^{-1}\operatorname{Tr}A,
\qquad V=d^{-1}\operatorname{Tr}(A-\bar\lambda I)^2.
```

For $`V\gt 0`$, Chebyshev's inequality implies that at least $`3d/4`$ eigenvalues lie in an interval of width $`4\sqrt V`$. Partition that interval into $`\lceil4\sqrt{Vt}\rceil`$ cells of diameter at most $`t^{-1/2}`$, assigning each boundary eigenvector to one cell. The number of cells is at most $`1+4\sqrt{Vt}`$. Pigeonholing gives

```math
M_t\ge\frac{3d}{4(1+4\sqrt{Vt})}.
\tag{I2}
```

When $`V=0`$, $`A`$ is scalar and $`M_t=d`$, so (I2) remains a valid, weaker bound.

For (I1), $`d=2^n`$ and $`V=\frac14\sum_jg_j^2`$. Define $`x=t\sum_jg_j^2`$. Since $`1+2\sqrt x\le\sqrt{5(1+x)}`$, any band construction with population guarantee $`N\ge M_t/k`$ and $`m=\lfloor\log_2N\rfloor`$ obeys

```math
m\ge n-\frac12\log_2(1+x)
-\left[1+\log_2\left(\frac{4k\sqrt5}{3}\right)\right].
\tag{I3}
```

For the finite dyadic construction one may use $`k=\lceil4/\sqrt\epsilon\rceil`$. Thus bounded couplings and any prescribed polynomial exposure give an explicit passive code storing $`n-O_\epsilon(\log n)`$ logical qubits. The additional dimension guarantee relative to all allowed codes is

```math
0\le\log_2D_\epsilon(t;A)-m
\le1+\log_2\left(\frac{Ck}{1-\epsilon}\right).
\tag{I4}
```

The compiler is polynomial for bounded couplings, polynomial $`t`$, and inverse-polynomial error tolerance. It is not asserted polynomial in the bit length of $`t`$. Required calibration accuracy is an input assumption; the number of bits specifying the estimates is not the physical cost of obtaining them. Temporary encoder workspace is cleaned before storage; decoder workspace is introduced only after storage and is discarded after recovery. Independent local noise, coupling drift beyond the stated certificate, and imperfect boundary operations require separate models and are not included in these guarantees.

High rates for homogeneous collective dephasing already follow from exact noiseless sectors. For example, the perfect-memory limit in D'Arrigo, Benenti and Falci, [arXiv:quant-ph/0703014v3](https://arxiv.org/html/quant-ph/0703014v3), Section 3.3, uses the equal-weight sector with dimension of order $`2^n/\sqrt n`$. Here the occupancy law and the calibrated construction apply to unequal bounded weights, including cases without exact spectral degeneracy.

## Finite time and the infinite-time algebra

For each fixed finite $`A`$, the limit channel is

```math
\lim_{t\to\infty}\Phi_t=\Pi_A,
\qquad
\Pi_A(X)=\sum_\alpha P_\alpha X P_\alpha,
\tag{I5}
```

where $`P_\alpha`$ are the projectors onto distinct eigenspaces. The convergence holds in diamond norm in finite dimension. The fixed algebra is the direct sum of full matrix algebras on those eigenspaces. Its largest exact noiseless subspace has dimension $`m_*:=\max_\alpha\operatorname{rank}P_\alpha`$. Proposition 2 shows that $`D_0(t;A)=m_*`$ at every positive time.

If the spectrum is nondegenerate, $`\Pi_A`$ is entanglement breaking. Moreover $`\lambda_{\max}(G_t)\to1`$. For any fixed $`\epsilon\lt 1/2`$, eventually $`\lambda_{\max}(G_t)\lt 2(1-\epsilon)`$; the all-code converse then forces $`D_\epsilon(t;A)=1`$. Thus every fixed nondegenerate register eventually loses the ability to store even one logical qubit at that error.

This is compatible with (I3). For a sequence of $`n`$-qubit operators with bounded unequal couplings, the spectrum contains $`2^n`$ levels in a range growing at most linearly with $`n`$. Many levels can remain within one finite-time resolution interval even though no two are exactly equal. At polynomial times $`t=t_n`$, the constructed rate $`m/n`$ tends to one. Taking infinite time at each fixed $`n`$ gives a different limit. No nontrivial infinite-time noiseless algebra is inferred from the finite-time rate.

The general role of peripheral matrix blocks in long-time storage is established by Singh and Datta, [arXiv:2504.10436v2](https://arxiv.org/html/2504.10436v2), Theorem 3.1 and Corollary 3.3. The finite-time statistic used here retains information about near-degenerate spectral clusters before that limiting description becomes sufficient.

## Separate corollary: communication over independent complete uses

This corollary concerns a different experiment. Fix $`A`$ and $`t`$, and use the complete channel $`\Phi_t`$ independently many times, with a fresh independent noise realization for each use. Let $`Q(\Phi_t)`$ be its unassisted quantum communication capacity in qubits per complete use, and let $`Q_{\leftrightarrow}(\Phi_t)`$ allow unlimited classical communication between uses, but no initial shared entanglement. These are not single-register storage dimensions, and the communication protocols do not introduce operations inside a storage interval.

Write

```math
h_{\rm bos}(u)=(u+1)\log_2(u+1)-u\log_2u,
\qquad h_{\rm bos}(0)=0.
```

Then

```math
\boxed{
\max\{0,\log_2M_t-h_{\rm bos}(1/4)\}
\le Q(\Phi_t)
\le Q_{\leftrightarrow}(\Phi_t)
\le\log_2\lambda_{\max}(G_t)
\le\log_2M_t+\log_2C.
}
\tag{I6}
```

The upper bound is a strong-converse bound for fixed-length deterministic entanglement-generation protocols. No equality between assisted and unassisted capacities is asserted. This corollary is not needed to prove the one-register theorem.

### Lower bound and coherent-state normalization

Use canonical one-mode coherent states

```math
|\alpha\rangle=e^{-|\alpha|^2/2}\sum_{r=0}^{\infty}\frac{\alpha^r}{\sqrt{r!}}|r\rangle,
\qquad
\langle\beta|\alpha\rangle
=e^{-(|\alpha|^2+|\beta|^2)/2+\beta^*\alpha}.
\tag{I7}
```

The isometry

```math
V_t|i\rangle=|i\rangle\otimes|\sqrt t\,\lambda_i\rangle
\tag{I8}
```

has reduced system channel $`\Phi_t`$, because the environmental overlap for real amplitudes is exactly $`e^{-t(\lambda_i-\lambda_j)^2/2}`$. Its complementary channel is

```math
\Phi_t^c(\rho)=\sum_i\rho_{ii}|\sqrt t\,\lambda_i\rangle\langle\sqrt t\,\lambda_i|.
\tag{I9}
```

The coherent-state environmental representation is established for the bosonic number-spectrum dephasing channel by Arqand, Memarzadeh and Mancini, [arXiv:2007.03897v4](https://arxiv.org/html/2007.03897v4), Eqs. (7)–(9) and (16)–(19). Their amplitudes $`-i\sqrt\gamma\,m`$ become real after an environment phase rotation. Here $`\gamma=t`$ in the matrix-element normalization of their Eq. (9), and (I7)–(I9) verify the finite-spectrum extension directly.

This oscillator is a mathematical dilation of the specified channel. The displacement below is an entropy-preserving change of representation; it adds no bath access or physical bath-energy assumption to the storage model.

Choose $`M_t`$ eigenvectors inside a resolution interval with midpoint $`c`$, and use their uniform mixture as the channel input. The system output entropy is $`\log_2M_t`$. Displace the environment by $`-\sqrt t\,c`$; this leaves its entropy unchanged. Every displaced amplitude then has absolute value at most $`1/2`$. The resulting environment state $`\tau_E`$ satisfies

```math
\operatorname{Tr}(b^\dagger b\,\tau_E)\le1/4.
\tag{I10}
```

For completeness, a state of mean number at most $`u\gt 0`$ has entropy at most $`h_{\rm bos}(u)`$. Compare it by nonnegativity of relative entropy with the thermal state

```math
\theta_u=\frac1{u+1}\sum_{r=0}^{\infty}
\left(\frac{u}{u+1}\right)^r|r\rangle\langle r|.
```

If the state's mean number is $`E\le u`$, this gives

```math
S(\tau_E)\le\log_2(u+1)+E\log_2\frac{u+1}{u}
\le h_{\rm bos}(u).
```

The input therefore has coherent information at least $`\log_2M_t-h_{\rm bos}(1/4)`$. The quantum channel coding theorem makes this an achievable independent-use rate; see Devetak, *The private classical capacity and quantum capacity of a quantum channel*, IEEE TIT 51, 44–55 (2005), [arXiv:quant-ph/0304127](https://arxiv.org/abs/quant-ph/0304127), [DOI:10.1109/TIT.2004.839515](https://doi.org/10.1109/TIT.2004.839515). Truncating a negative lower bound at zero proves the first inequality in (I6).

### Upper bound for adaptive classical assistance

Let $`\mu=\lambda_{\max}(G_t)`$. The CP order $`\Phi_t\le_{\rm CP}\mu\Delta`$ holds on arbitrary ancillary systems. In a deterministic protocol using the channel $`L`$ times, replace the channel at each step by $`\Delta`$, leaving all local operations and classical communication unchanged. Induction through the positive maps of the protocol gives

```math
\rho_L\le\mu^L\sigma_L.
\tag{I11}
```

The comparison protocol has only entanglement-breaking communication and starts without shared entanglement. Thus $`\sigma_L`$ is separable across the sender–receiver partition. Its overlap with a maximally entangled target of dimension $`K_L`$ is at most $`1/K_L`$, so

```math
F_L\le\frac{\mu^L}{K_L}.
\tag{I12}
```

If $`\liminf_L L^{-1}\log_2K_L\gt \log_2\mu`$, the target overlap tends to zero exponentially. This proves the upper bound and its stated strong-converse meaning. Failure branches are included in the output state; no bound on a postselected normalized branch is being asserted.

[Scientific overview](README.md) · [Repository overview](../README.md) · [Related work](../references/related_work.md)
