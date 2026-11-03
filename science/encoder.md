# A finite-bit, clean reversible encoder for a calibrated spectral band

## Statement and scope

Consider an $`n`$-qubit memory, with $`n\ge1`$, and

```math
A=\sum_{j=1}^n g_j N_j,\qquad N_j=|1\rangle\langle1|_j,
```

and Gaussian dephasing

```math
\Phi_t(|x\rangle\langle y|)
=e^{-t(E_x-E_y)^2/2}|x\rangle\langle y|,
\qquad E_x=\sum_j g_jx_j.
```

The coefficients can have either sign and can vanish. The time $`t\gt 0`$ and target error $`0\lt \epsilon\lt 1/4`$ are supplied as positive rational numbers. The true coefficients need not be rational. The classical input supplies rational estimates $`\widehat g_j`$ and certified error bounds $`u_j`$ satisfying

```math
|g_j-\widehat g_j|\le u_j.
```

The certificates are assumptions about the physical model. The compiler does not infer them from measurement data. All statements below hold uniformly for every fixed coefficient vector consistent with the certificates.

The construction produces a deterministic isometric encoder for $`m`$ unknown logical qubits, including inputs entangled with an inaccessible reference. All input and temporary computation registers are clean before storage. Only the $`n`$ physical qubits carry quantum information through the storage interval. The decoder uses fresh temporary registers after storage. There are no interventions during storage and no quantum bypass.

With ideal end operations, the storage half-diamond error is at most $`9\epsilon/16`$. The remaining $`7\epsilon/16`$ can be assigned to encoder and decoder implementation errors. If $`D_\epsilon(t)`$ denotes the unrestricted deterministic memory dimension at total half-diamond error at most $`\epsilon`$, the construction satisfies

```math
0\le\log_2D_\epsilon(t)-m
\le 1+\log_2\frac{(2+\sqrt{2\pi})b_\epsilon}{1-\epsilon},
\qquad
b_\epsilon=\left\lceil\frac4{\sqrt\epsilon}\right\rceil.
\qquad\text{(1)}
```

Thus its loss is a constant number of logical qubits for fixed $`\epsilon`$, uniformly in the number, spacing, signs and degeneracies of the actual spectrum. The constant in (1) is not optimized. For inverse-polynomial $`\epsilon`$, the loss is $`O(\log(1/\epsilon))`$, not a constant independent of $`\epsilon`$.

## 1. Exact dyadic grid selection

Set

```math
v=\frac{\epsilon}{16n^2t},\qquad
e=\lfloor\log_2v\rfloor,\qquad
k=\left\lfloor\frac e2\right\rfloor,\qquad
\delta=2^k.
\qquad\text{(2)}
```

These definitions can be evaluated with integer arithmetic. If $`v=p/q\gt 0`$, the difference between the binary lengths of $`p`$ and $`q`$ gives a candidate for $`e`$; one integer comparison against a shifted numerator or denominator determines whether to subtract one. No floating logarithm or square root is needed. Negative $`e`$ requires mathematical floor division by two.

Equation (2) gives the exact certificate

```math
\delta^2\le\frac{\epsilon}{16n^2t}\lt 4\delta^2.
\qquad\text{(3)}
```

Equivalently, for $`\delta_*=\sqrt\epsilon/(4n\sqrt t)`$,

```math
\delta_*/2\lt \delta\le\delta_*.
```

The input precision condition is

```math
u_j\le\delta/2\quad\text{for every }j.
\qquad\text{(4)}
```

If the supplied certificates fail (4), this theorem does not certify that input at the requested $`t,\epsilon`$. The compiler can state the required precision; it must not silently substitute a smaller uncertainty. As a more general diagnostic, any estimates and grid give the valid bandwidth bound $`4n\delta+2\sum_j(u_j+\delta/2)`$, but the specific constants and optimality guarantee below use (4).

Round exactly to

```math
q_j=\mathrm{nint}(\widehat g_j/\delta)\in\mathbb Z.
\qquad\text{(5)}
```

Any fixed nearest-integer tie rule works. The prototype uses ties toward $`+\infty`$, namely $`\lfloor\widehat g_j/\delta+1/2\rfloor`$. From (4)–(5),

```math
|g_j-\delta q_j|\le\delta,
\qquad
\left|E_x-\delta\sum_jq_jx_j\right|\le n\delta
\quad\text{for every }x.
\qquad\text{(6)}
```

If $`|g_j|\le G`$, then

```math
S:=\sum_j|q_j|
\le n(G/\delta+1)
\le8n^2G\sqrt{t/\epsilon}+n.
\qquad\text{(7)}
```

The number of fractional bits sufficient to specify coefficients to this accuracy is $`O(\log(n+1)+\log(1+t)+\log(1/\epsilon))`$, with the integer range charged separately through $`G`$. The full classical input length includes the rational descriptions of $`t,\epsilon,\widehat g_j,u_j`$. A description-length estimate is not a bound on physical calibration time or sample complexity.

## 2. Signed weights and the optimal closed band

Remove signed weights by a known bit relabeling:

```math
h_j=|q_j|,\qquad
y_j=\begin{cases}x_j,&q_j\ge0,\\1-x_j,&q_j\lt 0,\end{cases}
\qquad
S_-=\sum_{q_j\lt 0}|q_j|.
```

Then

```math
\sum_jq_jx_j=-S_-+\sum_jh_jy_j.
\qquad\text{(8)}
```

The shift $`-S_-`$ does not affect spectral diameters. Quantumly, the relabeling is a set of known $`X`$ gates. Zero weights require no special exclusion: both branches are counted, including their degeneracy.

Put $`B=4n`$. Choose the smallest integer $`a\in\{0,\ldots,S\}`$ maximizing

```math
N(a)=\#\left\{y\in\{0,1\}^n:
a\le\sum_jh_jy_j\le a+B\right\},\qquad N=\max_aN(a).
\qquad\text{(9)}
```

The interval in (9) is **closed**. It contains $`B+1`$ possible integer values and has diameter $`B`$. These are different quantities. Restricting $`a`$ to $`0,\ldots,S`$ loses nothing: a band starting below zero can be shifted to zero without losing any nonnegative sum, and a band starting above $`S`$ is empty. The definition covers $`S=0`$, $`B\gt S`$, and ties among maximizers. Since the all-zero $`y`$-string exists, $`N\ge1`$.

Set

```math
m=\lfloor\log_2N\rfloor,\qquad K=2^m,
\qquad\text{(10)}
```

and use the first $`K`$ accepted strings in lexicographic $`y`$-order. This is a fixed deterministic order; after the known sign flips, it need not coincide with lexicographic $`x`$-order.

### Storage error

Any two chosen strings have rounded energies separated by at most $`B\delta`$. Equation (6) therefore bounds their true spectral diameter by

```math
w\le B\delta+2n\delta=6n\delta.
\qquad\text{(11)}
```

For a generator supported in an interval of diameter $`w`$, center it to norm at most $`w/2`$. The double-commutator generator has diamond norm at most $`w^2/2`$. Integrating the dephasing semigroup gives

```math
\frac12\|\Phi_t|_{\mathcal C}-\mathrm{id}_{\mathcal C}\|_\diamond
\le\frac{tw^2}{4}
\le9n^2t\delta^2
\le\frac{9\epsilon}{16}.
\qquad\text{(12)}
```

This is a whole-channel statement and includes arbitrary entangled references. In the $`N_j`$ convention, one can sharpen some of these constants by using the range of the rounding-error function; the conservative bound (11) is sufficient here.

### Constant-qubit optimality

Let

```math
M_t=\max_z\#\{x:E_x\in[z,z+t^{-1/2}]\}.
```

All strings whose true energies lie in an interval of diameter $`2n\delta`$ have rounded integer energies in an interval of diameter at most $`4n=B`$. Taking the minimum sign-shifted nonnegative rounded sum from (8) as the band start shows that (9) contains at least as many strings as every such true interval. This argument uses the estimates only through (6), so it applies to every consistent true coefficient vector.

By (3), a resolution interval of width $`t^{-1/2}`$ can be divided into $`b_\epsilon=\lceil4/\sqrt\epsilon\rceil`$ pieces of diameter at most $`2n\delta`$. Assign shared boundary points to one piece so that multiplicities are counted once. Hence

```math
N\ge\left\lceil\frac{M_t}{b_\epsilon}\right\rceil,
\qquad K\ge\frac{M_t}{2b_\epsilon}.
\qquad\text{(13)}
```

The integer $`b_\epsilon`$ can itself be computed without a square root: it is the least integer $`k`$ with $`k^2\epsilon\ge16`$. Combining (13) with the unrestricted spectral-occupancy converse

```math
D_\epsilon(t)\le\frac{(2+\sqrt{2\pi})M_t}{1-\epsilon}
```

proves (1). The lower inequality in (1) follows because the constructed channel, including separately budgeted end-operation errors, is an admissible protocol at error $`\epsilon`$.

## 3. Exact classical preprocessing

Use suffix counts

```math
F_{n+1}(s)=\mathbf1_{s=0},\qquad
F_j(s)=F_{j+1}(s)+F_{j+1}(s-h_j),
\qquad\text{(14)}
```

with out-of-range entries zero and $`0\le s\le S`$. For $`h_j=0`$, (14) correctly doubles the count. Counts are at most $`2^n`$, so $`c=n+1`$ bits suffice, including the all-strings case. A sliding sum over $`F_1`$ finds (9) exactly.

Precompute suffix prefix sums $`P_j(z)=\sum_{s\le z}F_j(s)`$, saturated to zero below zero and to the full suffix count above $`S`$. For each site $`j`$ and partial nonnegative sum $`p\in\{0,\ldots,S\}`$, store

```math
C_j(p)=P_{j+1}(a+B-p)-P_{j+1}(a-1-p).
\qquad\text{(15)}
```

This is the number of accepted completions if the next bit is zero. Precomputing (15) avoids signed-address arithmetic during coherent lookup. The sum register uses

```math
\ell=\max\{1,\lceil\log_2(S+1)\rceil\}
```

bits. Values at unused binary addresses above $`S`$ can be defined as zero.

There are $`O(n(S+1))`$ count words. The table storage is $`O(n(n+1)(S+1))`$ bits. On a classical random-access bit-cost model, ordinary addition, subtraction and address arithmetic give the conservative preprocessing bound

```math
O\bigl(n(S+1)(n+\ell)\bigr)
\qquad\text{(16)}
```

elementary bit operations, in addition to polynomial arithmetic in the rational input length. This does not regard an $`n`$-bit count addition as a unit-cost operation. Generating and storing the compiled gate description has its own cost below.

## 4. Rank and unrank as total Boolean circuits

**Unranking.** Start with residual rank $`r\in\{0,\ldots,K-1\}`$ and partial sum $`p=0`$. At site $`j`$, obtain $`c_j=C_j(p)`$. If $`r\lt c_j`$, set $`y_j=0`$. Otherwise set $`y_j=1`$ and replace $`r\leftarrow r-c_j`$. In either case update $`p\leftarrow p+h_jy_j`$. At termination the residual rank is zero and $`y`$ is the required accepted string.

**Ranking.** Start with $`r=0,p=0`$. At site $`j`$, add $`y_jC_j(p)`$ to $`r`$, then update $`p\leftarrow p+h_jy_j`$. For an accepted string this returns its lexicographic rank.

The count and rank arithmetic can use $`n+1`$ bits. Ranking arbitrary $`n`$-bit strings returns the number of accepted strings lexicographically preceding them, which is at most $`N\le2^n`$. Unranking can be extended to all binary inputs by the same finite arithmetic. These total extensions need not be inverses outside the valid code sets; their clean XOR evaluations are nevertheless well-defined reversible circuits. In the cleanup oracle only the lower $`m`$ rank bits are copied. For the chosen codewords the full rank is below $`K=2^m`$, so this erases the input exactly.

Comparisons, addition, subtraction and Boolean selection have ordinary linear-size bit circuits. A table lookup is implemented by scanning each classical address, computing an equality flag against the quantum address, and applying controlled XORs to the output bits prescribed by that table word. Equality flags can be made with $`X`$, CNOT and Toffoli gates. A lookup therefore costs

```math
O((S+1)(\ell+n))
\qquad\text{(17)}
```

primitive reversible gates. There is no unit-cost quantum RAM operation and no uncharged loading oracle. The literal table entries determine which controlled gates the compiler emits.

There are $`n`$ lookups in each rank or unrank computation. An intentionally simple fresh-wire Boolean implementation, followed by uncomputation, gives

```math
G_{\mathrm{enc}}=O\bigl(n(S+1)(n+\ell)\bigr),
\qquad
G_{\mathrm{dec}}=G_{\mathrm{enc}},
\qquad\text{(18)}
```

primitive $`X`$, CNOT and Toffoli gates, and at most the same asymptotic number of temporary work qubits. This generous workspace bound is achieved by retaining intermediate Boolean wires and then reversing their computation. It does not require a nontrivial space-time optimization theorem.

A literal gate description has $`O(G_{\mathrm{enc}}\log(G_{\mathrm{enc}}+n))`$ bits because wire indices are written in binary. A straightforward compiler can generate it with that additional bit-time and working-storage cost after table construction. The table-storage bound by itself is not a bound on the storage needed to retain the entire emitted circuit.

Together with (7), these costs are polynomial in $`n`$, the rational input length, and $`G\sqrt{t/\epsilon}`$. For bounded $`G`$, polynomial $`t`$, and inverse-polynomial $`\epsilon`$, they are polynomial in $`n`$ and the supplied input size. They are not promised polynomial in $`\log t`$. Large workspace constants in this transparent implementation are not a claim of hardware efficiency, low depth, geometric locality, or fault-tolerant overhead.

## 5. Clean coherent isometry and decoding channel

Let $`U(r)`$ denote the selected $`y`$-string and $`R(y)`$ its rank on the accepted set. Standard compute-copy-uncompute gives the clean XOR oracles

```math
O_U:|r\rangle|y\rangle|0\rangle_W
\mapsto|r\rangle|y\oplus U(r)\rangle|0\rangle_W,
```

```math
O_R:|y\rangle|r\rangle|0\rangle_W
\mapsto|y\rangle|r\oplus R(y)\bmod2^m\rangle|0\rangle_W.
```

In each oracle, first compute the Boolean function using initially zero work wires, copy its output by CNOTs into the target, and reverse every computation gate. Input registers remain unchanged by that oracle and all work wires return to zero.

Apply $`O_U`$, then $`O_R`$, then the known physical sign flips. For every $`0\le r\lt K`$,

```math
|r\rangle_L|0^n\rangle_P|0\rangle_W
\longmapsto
|0^m\rangle_L|x(r)\rangle_P|0\rangle_W.
\qquad\text{(19)}
```

This is a literal computational-basis permutation with no rank-dependent phase. Linearity proves the clean isometry for arbitrary superpositions and reference-entangled states. The logical input register and all work registers can be discarded or reset before storage. Neither carries any logical information in the ideal construction.

The dephasing channel preserves the span of the selected computational basis strings. After storage, initialize fresh logical and work registers to zero and run the full encoding circuit in reverse. On this subspace it returns the physical and work registers to zero. The exact decoded channel is

```math
\Lambda_t(|r\rangle\langle s|)
=e^{-t(E_{x(r)}-E_{x(s)})^2/2}|r\rangle\langle s|.
\qquad\text{(20)}
```

Discarding non-output registers defines a completely positive trace-preserving decoder on the entire physical input space, including states outside the code. No inverse is assumed to exist outside the chosen subspace.

Reversible enumerative coding and compute-copy-uncompute are inherited circuit techniques. The contribution here is their explicit finite-bit specialization to the calibrated weighted band that satisfies the all-code optimality guarantee (1).

## 6. Composable implementation-error budget

Let $`\widetilde E,\widetilde D`$ be the actual boundary channels, with all nonphysical encoder registers discarded before storage and all nonlogical decoder registers discarded afterwards. Suppose their composable half-diamond errors relative to the ideal boundaries satisfy

```math
\eta_E+\eta_D\le7\epsilon/16.
\qquad\text{(21)}
```

Contractivity and the triangle inequality give

```math
\frac12\|\widetilde D\Phi_t\widetilde E-\mathrm{id}\|_\diamond
\le\eta_E+\frac{9\epsilon}{16}+\eta_D
\le\epsilon.
\qquad\text{(22)}
```

An approximate encoder may leave imperfectly cleaned work registers. They are discarded before storage rather than retained as an unintended quantum carrier; this discarding does not increase the channel-distance bound.

For a circuit with $`T_{\mathrm{end}}`$ implemented operations in total, a sufficient uniform allocation is half-diamond error at most

```math
\frac{7\epsilon}{16T_{\mathrm{end}}}
\qquad\text{(23)}
```

per operation. More generally, the sum of the composable operation errors can be at most $`7\epsilon/16`$. Noisy initializations or resets must be included in this budget if they are not ideal. Equation (23) is a sufficient error allocation, not a fault-tolerance resource estimate or a statement that arbitrary temporally correlated hardware noise is described by independent gate channels. If a native decomposition changes the operation count, use the actual native count in (23).

All arithmetic comparisons and reversible gates in the ideal compiler are exact; there is no additional floating-point or rotation-synthesis error hidden in the mathematical encoding.

## 7. Executable primitive-gate verification

The accompanying [`verify_reversible_encoder.py`](../verification/verify_reversible_encoder.py) is a small-instance implementation of the preceding construction. It emits and simulates actual $`X`$, CNOT and Toffoli gates for the lookup, arithmetic, rank/unrank and cleanup circuits. It does not implement a rank/unrank call as a single black-box permutation. Sparse propagation of computational basis amplitudes avoids allocating a state vector exponential in temporary workspace; this is exact for the emitted permutation gates. Gaussian dephasing is applied to the encoded physical density-matrix entries before the inverse circuit.

The verification includes 504 exact-rational checks of grid selection, subdivision constants and signed rounding, and the following five circuit instances. All use $`t=4`$, $`\epsilon=1/16`$, and coefficient uncertainties equal to $`\delta/2`$.

| Physical qubits | Rounded weights | Band population | Logical qubits | Encoder primitive gates | Temporary work qubits |
|---:|---|---:|---:|---:|---:|
| 3 | $`0,-5,12`$ | 6 | 2 | 652 | 132 |
| 4 | $`-17,0,11,25`$ | 6 | 2 | 2,007 | 361 |
| 5 | $`0,-9,14,21,-31`$ | 12 | 3 | 4,238 | 756 |
| 6 | $`-7,0,11,16,-23,29`$ | 28 | 4 | 9,684 | 1,688 |
| 4 | $`0,0,0,0`$ | 16 | 4 | 848 | 191 |

For every case, all accepted strings are exhaustively checked against the exact classical dynamic program, and all logical basis inputs are propagated through the primitive encoder gates. The input and temporary work registers are exactly zero after encoding. The inverse circuit is additionally checked on arbitrary full-register basis states, verifying its global permutation inverse.

Each circuit is tested on a maximally entangled logical-reference state and a generic complex entangled input with a three-dimensional reference. After physical dephasing and gate-level inverse decoding, every non-output register is clean and the decoded density matrix agrees with (20); the observed maximum entrywise residual is zero at the stored floating-point precision. The tested state trace distances are below the corresponding analytic bandwidth bounds. The all-zero rounded-weight case retains nonzero true coefficients within their uncertainty intervals, so it also checks that rounding to zero does not silently replace the actual noise by zero.

[`reversible_encoder.json`](../verification/results/reversible_encoder.json) records the rational inputs, bands, physical codewords, gate counts, workspace counts and quantum-channel diagnostics. [`signed_zero_n4_primitive_gates.json`](../verification/results/signed_zero_n4_primitive_gates.json) contains a literal primitive gate list. These tests verify the implemented small instances and support the bookkeeping. The analytical derivation, not the finite checks, establishes the asymptotic complexity or unrestricted optimality theorem. The prototype does not establish physical gate fidelity or an experimental memory advantage.

[Scientific overview](README.md) · [Repository overview](../README.md) · [Related work](../references/related_work.md)
