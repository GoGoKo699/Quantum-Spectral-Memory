# Operational model and notation

## Gaussian dephasing on one finite memory

Let $`S\simeq\mathbb C^d`$ be the physical memory and let $`A=A^\dagger\in\mathcal B(S)`$ be known. Fix an orthonormal eigenbasis,

```math
A=\sum_{i=1}^d\lambda_i|i\rangle\langle i|,
```

where eigenvalues are listed with multiplicity. The storage channel at exposure $`t\ge0`$ is

```math
\mathcal L_A(X)=AXA-\tfrac12(A^2X+XA^2)
              =-\tfrac12[A,[A,X]],
\qquad
\Phi_t=e^{t\mathcal L_A}.
\tag{M1}
```

Thus

```math
\Phi_t(|i\rangle\langle j|)
=e^{-t(\lambda_i-\lambda_j)^2/2}|i\rangle\langle j|.
\tag{M2}
```

The normalization is fixed by (M1)–(M2). In particular, $`t(\lambda_i-\lambda_j)^2`$ is dimensionless; if $`t`$ is physical time, the noise-rate units are included in $`A`$. For $`t\gt 0`$, an equivalent random-unitary representation is

```math
\Phi_t(X)=\int_{\mathbb R}\frac{e^{-s^2/(2t)}}{\sqrt{2\pi t}}
 e^{-isA}Xe^{isA}\,ds.
\tag{M3}
```

There is no assumption that the spectrum is equally spaced, nondegenerate, or integer valued. Shifting $`A`$ by a scalar multiple of the identity changes neither the generator nor the channel. A separate system Hamiltonian is not included in this model.

## Allowed storage codes

The logical register is $`Q\simeq\mathbb C^D`$. Encoding occurs before the storage interval and recovery occurs after it. The only quantum register carried across the interval is $`S`$. An arbitrary classical record may also be retained.

For a discrete classical record $`c`$, an encoder is an instrument $`\{\mathcal E_c\}_c`$, where each

```math
\mathcal E_c:\mathcal B(Q)\longrightarrow\mathcal B(S)
```

is completely positive and trace nonincreasing, and $`\sum_c\mathcal E_c`$ is trace preserving. The joint encoded state is the classical–quantum state

```math
\mathcal E(X)=\sum_c\mathcal E_c(X)\otimes|c\rangle\langle c|.
\tag{M4}
```

Conditional on $`c`$, the terminal recovery $`\mathcal R_c:\mathcal B(S)\to\mathcal B(Q)`$ is an arbitrary completely positive trace-preserving map. The resulting logical channel is

```math
\Lambda_t=\sum_c\mathcal R_c\circ\Phi_t\circ\mathcal E_c.
\tag{M5}
```

The sum in (M5) includes every outcome. This is deterministic storage, with no conditioning on a favorable outcome. Ordinary mixed encoders, private randomness, shared classical randomness, and arbitrary processing of the retained record are contained in this description. A general classical outcome space is handled by replacing sums by instrument integrals; the converse uses only positivity and trace normalization and is unchanged.

Temporary quantum workspace may be used during encoding and recovery. It is discarded or reset before storage, rather than retained as an additional quantum carrier. No bath record, quantum bypass, preshared entanglement available to the encoder and decoder, or intervention during storage is supplied. An inaccessible reference used to define the error is not an assistance resource. Boundary operations are ideal in the storage theorem; their circuit complexity and the required calibration precision are separate resources in the constructive result.

## Error criterion and stored dimension

For a linear map $`\Gamma`$, $`\|\Gamma\|_\diamond`$ denotes its completely bounded trace norm. A code has error at most $`\epsilon`$ if

```math
\frac12\|\Lambda_t-\operatorname{id}_D\|_\diamond\le\epsilon.
\tag{M6}
```

For a difference of channels this equals the maximum output trace distance over input states entangled with an inaccessible reference register of dimension $`D`$. Hence (M6) protects an unknown logical state together with all of its correlations with a reference.

Let $`D_\epsilon(t;A)`$ be the largest positive integer $`D`$ for which an allowed code exists. Logical dimensions are not restricted to $`D\le d`$ by definition. The converse proves

```math
D_\epsilon(t;A)\le \frac{d}{1-\epsilon},\qquad 0\le\epsilon\lt 1,
\tag{M7}
```

so this maximum is finite. Dimension one is always feasible. Restricting a feasible code to a smaller logical subspace preserves its error bound, using an isometric embedding and a trace-preserving extension of the inverse embedding. Consequently the maximum number of whole logical qubits is

```math
q_\epsilon(t;A)=\big\lfloor\log_2D_\epsilon(t;A)\big\rfloor.
\tag{M8}
```

For $`d=2^n`$ and $`\epsilon\lt 1/2`$, (M7) implies $`q_\epsilon\le n`$. No claim that $`D_\epsilon=d`$ for every positive-error identity channel is needed: arbitrary-dimensional approximate compression with classical records is included in the model.

## Spectral occupancy

For $`t\gt 0`$, define the noise-resolution width and its largest spectral occupancy by

```math
w_t=t^{-1/2},\qquad
M_t(A)=\max_{x\in\mathbb R}\#\{i:\lambda_i\in[x,x+w_t]\}.
\tag{M9}
```

Intervals are closed and multiplicities are counted. Since the spectrum is finite, the maximum exists. Every half-open interval of the same width has occupancy at most $`M_t`$, a fact used in the Gaussian row estimate. When an interval is partitioned, boundary eigenvectors are assigned to one cell only. Each assigned cell remains contained in a closed interval of the stated diameter.

## Explicit qubit coupling convention

The efficient construction concerns

```math
A=\sum_{j=1}^n g_jN_j,
\qquad N_j=|1\rangle\langle1|_j,
\qquad |g_j|\le G.
\tag{M10}
```

For $`x=(x_1,\ldots,x_n)\in\{0,1\}^n`$, its noise eigenvalue is

```math
\lambda(x)=\sum_jg_jx_j.
\tag{M11}
```

Weights may be negative or zero. Under the uniform distribution on computational basis strings,

```math
\bar\lambda=\tfrac12\sum_jg_j,
\qquad
V:=2^{-n}\sum_x(\lambda(x)-\bar\lambda)^2
  =\tfrac14\sum_jg_j^2.
\tag{M12}
```

The general spectral theorem is information theoretic and does not assume an efficient description of an eigenbasis. Efficient compilation is asserted only for the explicitly supplied form (M10), with finite-precision coupling estimates and a stated error certificate.

## Relation to the storage literature

The use of arbitrary boundary encoders and recoveries to define quantum storage is part of the established Markovian-memory framework; see Singh and Datta, *Information storage and transmission under Markovian noise*, [arXiv:2504.10436v2](https://arxiv.org/html/2504.10436v2), Theorem 3.1. The present definitions specify the finite-time channel, classical record, and worst-case reference-sensitive error criterion used below.

[Scientific overview](README.md) · [Repository overview](../README.md) · [Related work](../references/related_work.md)
