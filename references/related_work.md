# Related work and the specific contribution

The task is to preserve an arbitrary logical register through one fixed interval of Gaussian dephasing,

```math
\Phi_t(|i\rangle\langle j|)
=e^{-t(\lambda_i-\lambda_j)^2/2}|i\rangle\langle j|,
```

using deterministic encoding and recovery at the interval boundaries. The physical memory is the only quantum carrier across the interval. Error is measured in half diamond distance, including an inaccessible reference. For the eigenvalues counted with multiplicity, define

```math
M_t=\max_a\#\{i:\lambda_i\in[a,a+t^{-1/2}]\}.
```

The contribution has two connected parts. First, for every finite spectrum and fixed target error $`0\lt \varepsilon\lt 1/4`$, the optimal logical dimension satisfies $`\log_2 D_\varepsilon(t)=\log_2 M_t+O_\varepsilon(1)`$, with constants independent of spectrum, dimension and time. The converse permits arbitrary mixed encoders, recovery channels and retained classical records. Second, for $`A=\sum_jg_j|1\rangle\langle1|_j`$, a compiler using finitely specified coupling estimates constructs a coherent code within $`O_\varepsilon(1)`$ logical qubits of that unrestricted optimum. Its preprocessing, storage and compiled gate counts are polynomial for bounded couplings, polynomial $`t`$, and fixed or inverse-polynomial $`\varepsilon`$. When $`\varepsilon`$ varies, the explicit logical-qubit gap grows as $`O(\log(1/\varepsilon))`$; it is a constant in system size at fixed error.

## Finite-time storage and channel converses

**Bardet, Junge, Laracuente, Rouze and Stilck Franca, “Group transference techniques for the estimation of the decoherence times and capacities of quantum Markov semigroups,” IEEE Transactions on Information Theory 67, 2878–2909 (2021).** [Primary text](https://arxiv.org/html/1904.11043v2); [DOI](https://doi.org/10.1109/TIT.2021.3065452).

Theorem V.1 bounds two-way quantum and private capacities by the largest noiseless matrix block once the semigroup is sufficiently close to its fixed algebra; related results treat other capacities and convergence estimates. Lemma VI.8 explicitly converts bounds on a modified Choi matrix into completely positive ordering against a conditional expectation. These are direct precedents for both finite-time capacity analysis and the comparison technique used here. The additional statement is a matching characterization at every time by spectral occupation at resolution $`t^{-1/2}`$. It remains informative when nearby distinct eigenvalues have not decohered, although the eventual fixed algebra has no nontrivial quantum block.

**Singh and Datta, “Information storage and transmission under Markovian noise,” PRX Quantum 7, 020312 (2026).** [Primary text](https://arxiv.org/html/2504.10436v2); [DOI](https://doi.org/10.1103/8rnj-667b).

Theorem 3.1 and its consequences connect one-shot storage and communication to the matrix blocks of a channel's peripheral space, with finite-time bounds obtained through convergence estimates. This establishes a general framework for the storage question and its long-time limit. The present Gaussian result resolves the finite-time geometry of one structured family uniformly over irregular spectra. Its lower bound uses approximate spectral bands, and the weighted-register construction gives an explicit compiler tied to that finite resolution. These statements do not replace the broader channel classification.

**Tomamichel, Wilde and Winter, “Strong converse rates for quantum communication,” IEEE Transactions on Information Theory 63, 715–727 (2017), and Berta and Wilde, “Amortization does not enhance the max-Rains information of a quantum channel,” New Journal of Physics 20, 053044 (2018).** [TWW primary text](https://arxiv.org/abs/1406.2946); [Berta–Wilde DOI](https://doi.org/10.1088/1367-2630/aac153).

Generalized-dephasing strong converses and adaptive communication bounds from entanglement measures are established results. Here the Gaussian Gram matrix gives the explicit feasible comparison $`\Phi_t\le_{\rm CP}\|G_t\|_\infty\Delta`$, where $`\Delta`$ is complete basis pinching. Bounding $`\|G_t\|_\infty`$ by a constant times $`M_t`$ evaluates this familiar comparison in a geometric form. A new general converse principle is not claimed.

## Protected subspaces and efficient coding

**Hamann, Sekatski and Dür, “Approximate decoherence free subspaces for distributed sensing,” Quantum Science and Technology 7, 025003 (2022).** [Primary text](https://arxiv.org/abs/2106.13828); [DOI](https://doi.org/10.1088/2058-9565/ac44de).

This work exploits spatially inhomogeneous commuting noise to construct approximate protected subspaces for sensing. It establishes that useful noise suppression need not require exact cancellation. The sensing task selects a two-dimensional subspace that remains sensitive to a desired field and permits controls that adjust effective couplings. The present task concerns the entire unknown logical register, passive storage during the interval, and comparison with every endpoint quantum code. Approximate DFS protection itself is an antecedent.

**Skotiniotis, Dür and Kraus, “Efficient quantum communication under collective noise,” Quantum Information and Computation 13, 290–323 (2013).** [Primary text](https://arxiv.org/html/1204.0891v3).

Their channel model, Eq. (1), applies the same local representation $`U_g`$ to each carrier. Theorem 1 constructs suitable token states when a tensor power contains the regular representation of the finite group. The ensuing protocol transmits $`m`$ logical qudits using $`m+r`$ physical qudits, with efficient encoding and decoding and an asymptotic rate tending to one. Thus efficient coherent transmission at high rate under collective noise is established. The weighted Gaussian problem instead fixes one register with arbitrary real local couplings and asks for its near-optimal finite-time code. Treating that whole register as one high-dimensional carrier in the earlier theorem does not preserve either the physical-register budget or its efficient circuit bounds.

**Li and Liu, “Efficient preparation of decoherence-free subspace basis states,” Physical Review A 113, 012410 (2026).** [Primary text](https://arxiv.org/html/2509.11544v1); [DOI](https://doi.org/10.1103/ndjm-z894).

Section II treats the total-spin-zero singlet DFS for an even number of qubits. Its preparation procedure constructs specified orthogonal basis states by projective operations and restarts. The full-basis resource bound, Eq. (17), is expressed in terms of the DFS dimension and a conditioning parameter. This is a different output task from implementing an isometry on an arbitrary unknown logical register. It does not address calibrated unequal-coupling bands or a finite-time comparison with unrestricted encoding and recovery.

**Farias, Maciel, Camilo, Lin, Ramos-Calderer and Aolita, “Quantum encoder for fixed-Hamming-weight subspaces,” Physical Review Applied 23, 044014 (2025).** [Primary text](https://arxiv.org/html/2405.20408v3); [DOI](https://doi.org/10.1103/PhysRevApplied.23.044014).

This earlier work, coauthored by Ruge Lin, is a direct structured-subspace encoding precedent. Definition III.1 and Eq. (4) specify a loader whose rotation angles depend on a supplied classical amplitude vector. Algorithms 3–4 traverse the fixed-weight basis in Ehrlich Gray-code order; Lemmas III.3–III.4 give an $`O(k\binom nk)`$ CNOT bound. Section IV also loads explicitly specified sparse supports. For homogeneous couplings, a fixed-weight space is an exact eigenspace of the memory generator. The present compiler instead implements a fixed isometry $`\sum_r\alpha_r|r\rangle\mapsto\sum_r\alpha_r|b_r\rangle`$, with no access to the unknown amplitudes, by weighted-band rank and unrank maps. Its contribution is the calibrated band choice and its near-optimal storage guarantee. The different input tasks preclude interpreting the resource bounds as a speedup over that amplitude loader; this construction is not a direct extension of its RBS synthesis.

**Cleve and DiVincenzo, “Schumacher's quantum data compression as a quantum computation,” Physical Review A 54, 2636 (1996).** [Primary text](https://arxiv.org/abs/quant-ph/9603009); [DOI](https://doi.org/10.1103/PhysRevA.54.2636).

Coherent combinatorial encoding and reversible workspace management have a substantial history. This paper implements a binary-string bijection for quantum compression using polynomially many primitive reversible operations. The present compiler uses that established strategy: classical weighted-sum counting supplies rank and unrank maps, and reversible computation implements their action on superpositions. Its additional content is the calibration-aware choice of a band, its uniform error guarantee, and its constant-qubit comparison with the best physical memory code. Dynamic programming, reversible enumeration and workspace cleanup are not claimed as new techniques.

## Computational communication capacity

**Meyer, Rizzo, Raza, Leone, Jerbi and Eisert, “The computational two-way quantum capacity,” arXiv:2601.15393 (2026).** [Primary text](https://arxiv.org/html/2601.15393v1).

This work shows that restricting encoding and decoding to polynomial resources can qualitatively change quantum capacity. Its Eq. (14) specializes to mixtures of Pauli-$`Z`$ strings. Theorem 9 gives efficient near-maximal communication for uniform distributions on polynomial-size supports, while computational assumptions produce hard channels beyond that regime. Generic weighted Gaussian dephasing is not of this Pauli form: its coherence attenuation depends on signed energy differences, rather than only the bitwise difference of the basis labels. The present result gives an unconditional, single-interval compiler and a fixed-error constant-qubit guarantee for a different structured family. It does not establish a new general computational-capacity framework or a computational separation.

## Bosonic dephasing and the related oscillator benchmark

**Arqand, Memarzadeh and Mancini, “Quantum capacity of a bosonic dephasing channel,” Physical Review A 102, 042413 (2020), and Lami and Wilde, “Exact solution for the quantum and private capacities of bosonic dephasing channels,” Nature Photonics 17, 525–530 (2023).** [Arqand et al. primary text](https://arxiv.org/html/2007.03897v4); [Lami–Wilde primary text](https://arxiv.org/html/2205.05736v2).

The coherent-state environment representation and diagonal-input coherent-information optimization are established in the former work. The latter determines exact asymptotic capacities for bosonic dephasing using the integer number spectrum and its Fourier/Toeplitz structure. The present arbitrary finite-spectrum estimate does not improve their exact lattice-spectrum answer. The supporting additive-constant bounds on independent-use capacities use these inherited tools; the primary result is the single-interval occupation law and its finite-bit compiler.

**Related repository: Bosonic Phase Memory.** [Exact benchmark at revision aa346e09df1d52381a77ae08ac3677fda8c64b8b](https://github.com/GoGoKo699/Bosonic-Phase-Memory/blob/aa346e09df1d52381a77ae08ac3677fda8c64b8b/science/02-exact-benchmark.md); [prior-work account at that revision](https://github.com/GoGoKo699/Bosonic-Phase-Memory/blob/aa346e09df1d52381a77ae08ac3677fda8c64b8b/science/06-prior-work.md).

That result solves the exact one-use memory optimum for one nondegenerate oscillator, arbitrary symmetric unimodal wrapped phase density, unrestricted deterministic encoding and recovery, and no energy constraint. Its optimum is a central phase-cell probability, approached by a number-phase comb construction. This is the closest related memory benchmark. Its complete-twirl comparison and arbitrary-code viewpoint are antecedents. The present spectrum can be finite, degenerate or incommensurate; the relevant statistic is occupation of an energy interval, and the compiler operates on a fixed weighted qubit register. The compact integer phase action and oscillator comb do not supply those statements.

## What remains after these comparisons

The substantive remainder is the combination of a dimension- and spectrum-uniform finite-time characterization with a calibrated polynomial compiler that approaches the unrestricted optimum within a fixed number of logical qubits at fixed error. No novelty is attributed to the existence of approximate DFSs, high rates under exact collective symmetry, generalized-dephasing degradability, entanglement-based converse machinery, or reversible combinatorial encoding.

The general occupation theorem is information theoretic. Efficient implementation requires the explicit linear-coupling form; it does not promise efficient diagonalization of an arbitrary many-body operator. The construction assumes supplied coupling estimates with certified error, and counts their representation and processing costs without identifying those costs with the physical resources needed to perform calibration. It covers one known common Gaussian noise direction, boundary operations, and the specified storage-error metric. Independent local noise, interleaved correction, and a polynomial-in-$`\log t`$ compiler are outside the result.

[Scientific overview](../science/README.md) · [Bibliography](references.bib)
