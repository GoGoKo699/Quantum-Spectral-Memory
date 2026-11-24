# Clean reversible compilation in a fixed-weight sector

A common coupling offset contributes the same phase to every string of the same physical Hamming weight. Fixing that weight makes it possible to compile a memory block using only certified estimates of the coupling differences from the common offset.

## Compiler interface

Let $`m\ge1`$ be the physical block size and $`h\in\{0,\ldots,m\}`$ its required Hamming weight. In the Pauli-$`Z`$ convention, the noise generator and supplied certificate are

```math
A_{\boldsymbol g}=\sum_{i=1}^m g_i Z_i,
\qquad
|g_i-c-\gamma q_i|\le u_i,
\qquad
q_i\in\mathbb Z,\quad \gamma\gt0.
```

A common real offset $`c`$ may be unknown. The endpoint compiler uses the integers $`q_i`$, the weight $`h`$ and an integer band. The scale $`\gamma`$, bounds $`u_i`$ and exposure $`t`$ enter the storage certificate. The [original compiler](encoder.md) uses occupation projectors $`N_i`$, with $`Z_i=I-2N_i`$.

For a computational string $`x`$ of weight $`h`$ define the signed integer energy $`S(x)=\sum_i q_i(1-2x_i)`$. Choose a closed integer band $`[a,b]`$ with population $`C\ge1`$ among those strings. A half-open integer band $`[a,b+1)`$ specifies the same set. For any integer $`0\le r\le\lfloor\log_2C\rfloor`$, the compiler produces clean reversible encoding and inverse decoding for the first $`2^r`$ accepted strings in lexicographic order.

The true energy differs from $`c(m-2h)+\gamma S(x)`$ by at most $`\sum_i u_i`$. The chosen span is invariant under the actual diagonal storage channel. Its half-diamond storage error, including a reference, satisfies

```math
\frac12\|\mathcal R\Phi_{\boldsymbol g,t}\mathcal E-\mathrm{id}\|_\diamond
\le
\min\left\{1,\frac{t}{4}
 \left(\gamma(b-a)+2\sum_i u_i\right)^2\right\}.
```

This follows by applying the [spectral interval bound](spectral_law.md#lemma-1-reference-stable-protection-of-a-spectral-interval) to the true diameter. The offset contributes a scalar throughout the allowed sector, independent of its value.

## Exact counting and rank access

Put $`Q=\sum_i|q_i|`$. Let $`F_i(k,s)`$ count suffix strings on sites $`i,\ldots,m`$ of weight $`k`$ and signed energy $`s`$. The first bit contributes $`q_i`$ for zero and $`-q_i`$ for one. Thus

```math
F_{m+1}(k,s)=\mathbf1_{\{k=0,\ s=0\}},\qquad
F_i(k,s)=F_{i+1}(k,s-q_i)+F_{i+1}(k-1,s+q_i).
```

Use zero outside the valid range, with $`0\le k\le h`$ and $`-Q\le s\le Q`$. Negative weights remain signed. Complementing individual bits to make their weights positive would change the Hamming-weight constraint. The two branches at a zero weight continue to count different physical strings.

For each suffix and each $`k`$, precompute the prefix sum $`P_i(k,z)=\sum_{s\le z}F_i(k,s)`$, saturated at the ends of the table. The band population is $`P_1(h,b)-P_1(h,a-1)`$. These same prefix sums give the population of every supplied band or find a maximum-population closed band of a prescribed integer diameter by scanning its possible start points. One can scan $`a\in[-Q,Q]`$ because the minimum energy of any nonempty accepted set is also a valid start point with at least that population.

Before processing site $`i`$, let $`p`$ be the signed energy already accumulated and let $`k`$ be the remaining weight. The number of accepted completions whose next bit is zero is

```math
C_i(k,p)=P_{i+1}(k,b-p-q_i)-P_{i+1}(k,a-1-p-q_i).
```

Unranking chooses zero when the residual rank is below $`C_i(k,p)`$ and otherwise chooses one and subtracts $`C_i(k,p)`$. Ranking adds the same count on every one branch. After choosing $`x_i`$, both procedures update $`k\gets k-x_i`$ and $`p\gets p+q_i(1-2x_i)`$. The accepted strings with next bit zero precede the one branch, proving the rank and unrank rules by induction. This holds for one-state sectors, truncated logical ranks, and bands with gaps or repeated energies.

For example, $`q=(-3,0,2)`$ at weight one gives energies $`-5,-1,5`$ on the lexicographically ordered strings $`001,010,100`$. The band $`[-5,-1]`$ keeps the first two strings. An arbitrary common shift leaves their energy difference unchanged.

## Clean workspace and finite costs

Precompute $`C_i(k,p)`$ from the prefix sums. Suffix counts, prefix sums and this lookup table have $`O(m(h+1)(2Q+1))`$ words. Each count uses at most $`m+1`$ bits. A lookup uses the joint integer address $`(k,p)`$. Equality checks against classical addresses and controlled XOR of the specified count bits implement it using $`X`$, CNOT and Toffoli gates. Comparisons, additions and subtractions have ordinary Boolean circuits in their bit widths. This gives classical bit preprocessing, emitted reversible gates and temporary wires polynomial in $`m`$, $`Q+1`$ and the input description length. It uses a literal table scan and charges the emitted gate description. The range dependence is on $`Q`$ itself.

Total Boolean extensions on the finite registers are sufficient. Implement signed partial sums with a fixed offset, give unused addresses zero counts and use total fixed-width arithmetic. Apply compute-copy-uncompute separately to rank and unrank, as in the [clean encoder construction](encoder.md#5-clean-coherent-isometry-and-decoding-channel). Unrank into a clean physical block, then XOR the lower $`r`$ bits of the physical word's rank into the original input. For the selected $`2^r`$ words this erases the input, as well as every temporary computation wire. Both operations extend linearly to arbitrary superpositions and external reference entanglement. Inverse decoding on the chosen code span returns the physical block and work wires to zero. For an arbitrary physical input the decoder applies the inverse circuit with fresh zero wires and discards all non-output registers, giving a trace-preserving map.

### Comparison with the optimum within the sector

The [scalar spectral law](spectral_law.md#theorem-1-one-register-storage) applies directly to the noise generator restricted to the weight-$`h`$ sector. Let $`D_\epsilon^{(h)}`$ be the best stored dimension in that sector under the same endpoint model. For $`0\lt\epsilon\lt1/4`$, take the [dyadic step from the original compiler](encoder.md#1-exact-dyadic-grid-selection) with $`n=m`$, so

```math
\gamma^2\le\frac{\epsilon}{16m^2t}\lt4\gamma^2.
```

Suppose the supplied grid certificates satisfy $`u_i\le\gamma`$. Choose a most occupied band of integer diameter $`4m`$ and take $`r=\lfloor\log_2C\rfloor`$. The true diameter is at most $`6m\gamma`$, giving error at most $`9\epsilon/16`$. Any interval of true energies of diameter $`2m\gamma`$ fits in an estimated interval of diameter $`4m\gamma`$ after a common shift. Divide a true resolution interval of width $`t^{-1/2}`$ into at most $`b_\epsilon=\lceil4/\sqrt\epsilon\rceil`$ pieces of that diameter, assigning shared boundaries once. The selected population is at least the maximum true resolution occupancy divided by $`b_\epsilon`$. The [occupancy converse](spectral_law.md#theorem-1-one-register-storage) and power-of-two rounding then give

```math
0\le\log_2 D_\epsilon^{(h)}-r
\le 1+\log_2\frac{(2+\sqrt{2\pi})b_\epsilon}{1-\epsilon}.
```

The comparison includes all encoders confined to the physical sector. The sector restriction can itself reduce the occupancy relative to the full register.

## Use in passive memory with a charged calibration transcript

[Quantum Memory Calibration](https://github.com/GoGoKo699/Quantum-Memory-Calibration/blob/main/science/compiled_calibration.md) uses this compiler on chosen active blocks, at weight $`h=\lfloor m/2\rfloor`$. A transcript supplies the signed midpoint integers and the endpoint circuits use the same public bin partition for each block. Its outer correction handles errors correlated by the one shared Gaussian phase. Together these steps achieve the sharp leading continuous calibration budget with polynomial endpoint costs at polynomial dimensionless hold times.

[Independent finite checks](../verification/README.md#fixed-weight-signed-bands) compare table counts, rank access and exact energy certificates with direct enumeration.

[Scientific overview](README.md) · [Original compiler](encoder.md) · [Learning route](../learning/anchor.md)
