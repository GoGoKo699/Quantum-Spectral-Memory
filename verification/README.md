# Reproducible finite verification

The tested environment is Python 3.12 with the versions pinned in [requirements.txt](requirements.txt). From the repository root, run:

```bash
python -m pip install -r verification/requirements.txt
python verification/run_all.py
python verification/generate_examples.py
```

The verification runner uses NumPy; the example generator also uses Matplotlib. `run_all.py` **always invokes the complete primitive-gate encoder suite**. A missing gate module or a failed assertion aborts the run; an import check or an instruction to run another script is not counted as verification.

To run only the primitive encoder suite:

```bash
python verification/verify_reversible_encoder.py
```

Its optional `--output PATH` changes the result directory. The default is `verification/results/`. Seeds and input cases are fixed. The generated JSON contains no timestamps or timing measurements and is deterministic in the tested environment.

## What is checked

### Gaussian kernels and classical bands

The unified runner checks 20 finite Gaussian kernels from scalar, lattice, clustered, degenerate and irregular spectra. It verifies kernel positivity, the completely positive domination residual, and the spectral-occupancy row bound to floating-point tolerance.

It also checks 120 exact-rational band instances with one through ten physical qubits, signed and zero coefficients, and extremal allowed calibration displacements. Across those cases, it enumerates 24,552 computational strings, compares the dynamic-program optimum with exhaustive band search, checks every accepted rank/unrank pair, and verifies the actual bandwidth and occupancy guarantee. The convention throughout is `A = sum_j g_j |1><1|_j`.

### An actual reversible circuit

`verify_reversible_encoder.py` independently constructs its suffix subset-sum and accepted-completion tables. It compiles table scans, unsigned comparisons, subtraction, addition, Boolean selection, and cleanup into literal `X`, `CX` and `CCX` gates. A table lookup is an equality-controlled XOR scan of classical constants. Ranking and unranking are not simulated as single black-box permutations, and no QRAM instruction is used.

The encoder computes the physical bit string, erases the original logical rank by a second reversible computation, and applies the known sign flips. Each oracle uses compute-copy-uncompute. The decoder is the full encoder gate list in reverse. Only the physical memory qubits remain nontrivial during the noise interval.

The suite performs 504 exact-rational arithmetic checks, including an independent comparison with `band_code.py` on 120 grids and 21 signed rounding ties. Its five main compiled circuit cases cover three through six physical qubits with signed and zero weights. One of the five is a four-qubit all-zero rounded case that retains nonzero true coefficients within their calibration intervals.

For each circuit, all logical basis inputs are propagated through the emitted gates. The inverse is also checked on arbitrary full-register basis states. Maximally entangled logical-reference states and generic complex entangled inputs are encoded, dephased on the physical register, and decoded. Every non-output register must be clean, and the decoded density matrix must agree with the predicted logical Schur channel. Sparse basis propagation is exact for these permutation gates and avoids a dense state vector exponential in temporary workspace.

The independently constructed tables and classical maps are compared against `band_code.py` on the same five calibration inputs: the grids, signed weights, bands and populations must match, as must every accepted codeword, its rank, and every partial-sum completion count. The circuit itself remains compiled from the independent implementation.

Two separate boundary checks exercise the zero-logical-qubit case and a one-physical-qubit negative-weight code. For weights `[-9, 18]`, the encoder has logical dimension one and prepares the nonzero physical word `10`; the decoder must clean both physical qubits. For weight `[-3]`, it encodes one logical qubit into the physical words `1, 0`. Both cases propagate the actual primitive gates, check cleanup and the decoded channel, and compare the classical maps with `band_code.py`. The dimension-one logical test cannot be entangled with its reference; the one-qubit case includes entangled inputs. These checks have their own summary and do not change the five-case performance table.

### Numerical tolerances

Grid selection, integer counts, rounding, codewords, gate permutations, bandwidth certificates and exact workspace-zero checks use no floating tolerance. The floating-point checks use the following explicit thresholds:

| Check | Threshold |
|---|---|
| Gaussian kernel positivity and CP-domination residual | Minimum eigenvalue at least `-1e-10` |
| Decoded Schur-channel maximum entrywise residual | Strictly less than `1e-13` |
| Decoded density-matrix trace | Absolute deviation from one strictly less than `1e-12` |
| Decoded density-matrix positivity | Minimum eigenvalue strictly greater than `-1e-12` |
| Tested state trace distance versus the analytic storage bound | At most the bound plus `1e-12` |

## Generated evidence

- `results/checks.json` contains the kernel and exact-band cases plus the mandatory gate-suite summary.
- `results/reversible_encoder.json` contains the primitive suite's rational inputs, physical codewords, populations, analytic bounds, gate counts, work-qubit counts, reference-channel diagnostics, independent implementation comparisons, and separate boundary-check summary.
- `results/signed_zero_n4_primitive_gates.json` contains a literal four-physical-qubit encoder. An instruction `["CCX", a, b, c]` has controls `a,b` and target `c`; `CX` and `X` use the corresponding shorter forms. Logical values use little-endian binary significance. Physical wire order follows coefficient/site order. Reversing the instruction list gives the decoder because all three primitive gates are self-inverse.

The example-generation script writes `results/examples.json` and the PNG/SVG figures under `figures/`. It verifies distinctness of the 65,536 exactly specified rational eigenvalues and reproduces the 16-qubit table in [the scientific examples](../science/examples.md). Those examples do not replace the mandatory checks above.

## What the checks do not establish

The analytical arguments establish the uniform spectral theorem, the unrestricted converse, the calibration guarantee, and the asymptotic resource bounds. Finite tests support the implementation and expose arithmetic or cleanup errors; they are not substitutes for those proofs. The tested state trace distances lie below the analytic bandwidth bound, but the script does not numerically optimize the unrestricted diamond norm.

Calibration certificates are supplied assumptions rather than simulated experiments. Gaussian matrix entries and density-matrix diagnostics use floating-point arithmetic; grid selection, integer tables, codewords, gate permutations and bandwidth certificates use exact arithmetic.

The reversible implementation intentionally retains intermediate Boolean wires and then uncomputes them. It uses hundreds or thousands of temporary work qubits in these small examples. It is an explicit polynomial-size construction, not an optimized claim about space, depth, locality, fault-tolerant overhead, physical gate fidelity, or experimental memory advantage.
