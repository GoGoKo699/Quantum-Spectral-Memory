# Thirty milestones for Quantum Spectral Memory

The map follows one question: how much unknown quantum information can a finite memory preserve during a prescribed interval of Gaussian dephasing, and how can a nearly optimal code be compiled from calibrated couplings?

**Background/preliminaries contains M01–M11.** These eleven milestones connect individual coherences, reference systems, channel representations, admissible records and coherent encoding into the complete operational question. **Narrative/innovation contains M12–M30.** These nineteen milestones assemble the spectral converse and construction, then the finite-bit compiler, before integrating examples, limiting regimes and the separate communication corollary. The allocation reflects the project's two linked results: a characterization against arbitrary codes and an explicit implementation approaching that characterization.

The sole educational anchor is John Watrous, *The Theory of Quantum Information* (2018), using the [author-hosted manuscript](https://jhwatrous.github.io/TQI.pdf). Section numbers below refer to that version. The [anchor bridge](anchor.md) translates its notation and provides a worked example. Watrous supplies the channel-theoretic foundations; the spectral estimates, calibration arithmetic and compiler arguments have their authoritative derivations in the linked scientific pages. This map identifies the main understanding targets without replacing those proofs.

The true coupling vector is fixed throughout each storage interval. For calibrated compilation it lies within the supplied uncertainty certificates. Uniformity over those fixed vectors does not include unmodeled time-dependent coupling drift.

## Phase I: Background/preliminaries — M01–M11

### M01: Coherence between noise eigenstates

**Central question.** Which part of a quantum state is sensitive to the separation of two noise eigenvalues?

**Understanding target.** Explain why populations remain fixed while an off-diagonal matrix element decays according to an eigenvalue difference. Identify the noise operator separately from a system Hamiltonian, and recognize why a scalar shift has no effect.

**Dependencies and story role.** This is the local physical starting point for the spectral geometry.

**Conceptual connection.** Matrix entries turn dephasing into a question about which coherences a code must retain.

**Sources.** [Watrous §§1.1.2][W1], [2.1.2][W2]; [model, (M1)–(M3)](../science/model.md#gaussian-dephasing-on-one-finite-memory).

### M02: A register and its inaccessible reference

**Central question.** What must survive when the logical input is part of a larger entangled state?

**Understanding target.** Distinguish the physical memory, logical register and inaccessible reference. Explain why preserving an isolated state's appearance does not establish preservation of its external correlations, and why the reference supplies no assistance to the encoder or decoder.

**Dependencies and story role.** Builds on M01 by enlarging the object being preserved from matrix entries to a joint state.

**Conceptual connection.** Purification makes storage quality a statement about information beyond the memory itself.

**Sources.** [Watrous §§2.1.2–2.1.3][W2]; [model, allowed registers and (M6)](../science/model.md#error-criterion-and-stored-dimension).

### M03: Channel representations and complete positivity

**Central question.** How can one physical transformation be described through its action, Choi matrix and environment?

**Understanding target.** Relate completely positive trace-preserving maps to positive Choi matrices and isometric dilations. Track the unnormalized Choi convention, whose trace equals the input dimension. Explain why positivity must persist when an inaccessible reference is included.

**Dependencies and story role.** Uses M02 to supply the common language for both the converse and the later capacity corollary.

**Conceptual connection.** A channel representation converts an operational claim into an operator inequality.

**Sources.** [Watrous §2.2.2, Theorem 2.22][W2]; [spectral law, Lemma 2](../science/spectral_law.md#lemma-2-a-converse-for-arbitrary-encoding-and-classical-records).

### M04: Classical records across a quantum storage interval

**Central question.** How can a retained classical record depend on an unknown input without becoming a quantum bypass?

**Understanding target.** Describe an encoding instrument, its subnormalized branches and conditional recovery. Explain why all outcomes contribute to a deterministic logical channel. Identify the physical memory as the only quantum carrier through the interval, including when temporary workspace is used at its boundaries.

**Dependencies and story role.** Combines M02–M03 into the full admissible code class.

**Conceptual connection.** Instruments distinguish classical side information from preserved quantum coherence and postselection.

**Sources.** [Watrous §2.3.2][W2]; [model, (M4)–(M5) and workspace assumptions](../science/model.md#allowed-storage-codes).

### M05: Half-diamond error and reference preservation

**Central question.** Which channel distance certifies preservation uniformly over unknown, reference-entangled inputs?

**Understanding target.** Interpret half the completely bounded trace norm as the project's error criterion. Connect it to output trace distance, composition with channels, and a lower bound on maximally entangled target overlap. Distinguish that overlap from Watrous's square-root fidelity convention.

**Dependencies and story role.** Gives M02–M04 a quantitative success criterion usable by both constructions and converses.

**Conceptual connection.** An operational distance makes separate error contributions composable.

**Sources.** [Watrous §§3.1.1, 3.2, 3.3.2–3.3.3][W3]; [model, (M6)](../science/model.md#error-criterion-and-stored-dimension); [spectral law, (S12)](../science/spectral_law.md#lemma-2-a-converse-for-arbitrary-encoding-and-classical-records).

### M06: Subspace encoding and trace-preserving recovery

**Central question.** How does an isometric code become a valid storage protocol on the entire physical state space?

**Understanding target.** Identify the code projector, embedding and inverse action on the code. Explain why recovery needs a trace-preserving extension outside that subspace, even when the specified dephasing preserves the encoded span. Relate this extension to the allowed channel model.

**Dependencies and story role.** Uses M03–M05 to turn a candidate collection of eigenvectors into a complete protocol.

**Conceptual connection.** A protected subspace and an admissible decoder are separate ingredients of achievability.

**Sources.** [Watrous §2.2.2][W2]; [spectral law, Lemma 1 and (S7)](../science/spectral_law.md#lemma-1-reference-stable-protection-of-a-spectral-interval).

### M07: Schur channels and complete dephasing

**Central question.** What matrix describes how a diagonal-noise channel changes every coherence?

**Understanding target.** Recognize entrywise multiplication by a positive semidefinite matrix with unit diagonal as a Schur channel. Identify complete dephasing as its diagonal comparator. Translate Watrous's Schur multiplier matrix, called $`A`$ there, into the project's $`G_t`$; the project's $`A`$ is instead the Hermitian coupling operator.

**Dependencies and story role.** Connects M01 and M03 to the matrix structure needed for the converse.

**Conceptual connection.** Correlation-matrix positivity packages the entire channel, including its action on references.

**Sources.** [Watrous §4.1.3][W4]; [spectral law, (S2), Lemma 2](../science/spectral_law.md#lemma-2-a-converse-for-arbitrary-encoding-and-classical-records).

### M08: Positive channel comparison and entanglement witnesses

**Central question.** How can comparison with a simpler channel constrain every encoding strategy?

**Understanding target.** Interpret completely positive order as positivity of the difference after adjoining any reference. Explain why complete dephasing produces a separable comparison state and why its overlap with a maximally entangled target of dimension $`D`$ is at most $`1/D`$.

**Dependencies and story role.** Joins the Choi representation in M03, records in M04 and Schur structure in M07 into a converse mechanism.

**Conceptual connection.** An entanglement witness converts channel domination into a dimension bound.

**Sources.** [Watrous §2.2.2][W2], [§§6.1.1–6.1.2][W6]; [spectral law, (S9)–(S11)](../science/spectral_law.md#lemma-2-a-converse-for-arbitrary-encoding-and-classical-records).

### M09: Logical dimension, whole qubits and resource accounting

**Central question.** Which quantities measure storage size, and which measure the cost of realizing it?

**Understanding target.** Distinguish a logical dimension $`D`$, its logarithm and the number of whole qubits obtained by taking a floor. Separate physical storage qubits from temporary workspace, classical table bits and gates. Recognize that a constant-qubit loss is a multiplicative dimension guarantee at fixed error.

**Dependencies and story role.** Organizes the resources introduced in M04–M08 before the constructive result.

**Conceptual connection.** Information-theoretic size and computational cost answer different questions about the same code.

**Sources.** [Watrous §2.1.2][W2]; [model, (M7)–(M8)](../science/model.md#error-criterion-and-stored-dimension); [encoder, resource accounting](../science/encoder.md#4-rank-and-unrank-as-total-boolean-circuits).

### M10: Coherent basis maps and temporary workspace

**Central question.** When does a classical map between basis labels encode an arbitrary quantum register?

**Understanding target.** Explain how an injective label map extends linearly to an isometry. Identify why residual label-dependent workspace would retain information about the input, and how a reversible computation can erase it. Distinguish this fixed transformation from preparing a state using classically supplied amplitudes.

**Dependencies and story role.** Adds an implementation route to the subspace protocol in M06 and the resource distinctions in M09.

**Conceptual connection.** Reversible classical logic can realize quantum encoding while preserving external entanglement.

**Sources.** [Watrous §§2.1.3, 2.2.2][W2]; [encoder, clean isometry](../science/encoder.md#5-clean-coherent-isometry-and-decoding-channel).

### M11: The complete finite-memory question

**Central question.** What must a proposed storage theorem specify before its optimality or efficiency can be assessed?

**Understanding target.** Assemble the fixed noise operator and exposure, physical carrier, allowed encoding instrument, terminal recovery, error tolerance and resource model. Distinguish the unrestricted optimization over endpoint channels from efficient implementation for explicitly given weighted-qubit couplings.

**Dependencies and story role.** Integrates M01–M10 into the framework used by every subsequent result.

**Conceptual connection.** Spectral geometry becomes a memory characterization only after the operational experiment and its resources are fixed.

**Sources.** [Watrous §2.2.2][W2], [§3.3.3][W3]; [complete operational model](../science/model.md); [scientific dependencies](../science/README.md#main-logical-dependencies).

## Phase II: Narrative/innovation — M12–M30

### M12: Spectral occupancy at the noise-resolution scale

**Central question.** Which feature of a finite spectrum remains relevant before complete dephasing has occurred?

**Understanding target.** Explain the resolution width $`t^{-1/2}`$ and the maximum occupancy $`M_t`$. Count eigenvalues with multiplicity, handle closed endpoints consistently, and distinguish a dense group of distinct levels from an exactly degenerate eigenspace.

**Dependencies and story role.** Applies the complete model in M11 to identify the statistic that both sides of the theorem will use.

**Conceptual connection.** The decay of a single coherence in M01 determines a scale for counting an entire spectrum.

**Sources.** [Watrous §4.1.3][W4]; [model, (M9)](../science/model.md#spectral-occupancy); [spectral law, (S1)–(S3)](../science/spectral_law.md#theorem-1-one-register-storage).

### M13: From spectral bandwidth to an achievable memory

**Central question.** Why does a narrow spectral interval protect every state in its span, including reference correlations?

**Understanding target.** Follow the role of centering the generator, bounding its diamond norm and integrating the semigroup. Explain how subdividing a maximally occupied resolution interval supplies a sufficiently narrow cell with a controlled population.

**Dependencies and story role.** Combines M05–M06 with M12 to establish the constructive side of the occupancy law.

**Conceptual connection.** A bandwidth estimate becomes a whole-channel guarantee, then an achievable logical dimension.

**Sources.** [Watrous §§3.3.2–3.3.3][W3]; [Lemma 1, (S4)–(S7)](../science/spectral_law.md#lemma-1-reference-stable-protection-of-a-spectral-interval); [achievability](../science/spectral_law.md#achievability-in-theorem-1).

### M14: The Gaussian Gram matrix as a channel comparator

**Central question.** How does the largest eigenvalue of the Gaussian kernel bound the full noise channel?

**Understanding target.** Identify the common Choi support on which the noise channel has matrix $`G_t`$ and complete dephasing has the identity matrix. Explain how a spectral matrix bound yields completely positive domination and survives adjoining an arbitrary reference.

**Dependencies and story role.** Specializes M07–M08 to the Gaussian memory and supplies the algebraic input to the unrestricted converse.

**Conceptual connection.** An operator-norm estimate controls an operational transformation, rather than only selected coherence entries.

**Sources.** [Watrous §2.2.2][W2], [§4.1.3][W4]; [spectral law, (S9)](../science/spectral_law.md#lemma-2-a-converse-for-arbitrary-encoding-and-classical-records).

### M15: The converse for arbitrary encoders and records

**Central question.** Why does the comparator constrain mixed encoders and input-dependent retained records as well as subspace codes?

**Understanding target.** Track subnormalized instrument branches through the positive comparison, conditional recovery and final sum. Explain normalization and separability of the comparison output, then combine its entangled overlap bound with the half-diamond success condition.

**Dependencies and story role.** Uses M04–M05, M08 and M14 to extend the conclusion beyond the construction in M13.

**Conceptual connection.** The theorem compares against all allowed endpoint codes without assuming their optimal encoder selects eigenvectors.

**Sources.** [Watrous §2.3.2][W2], [§6.1.1][W6]; [Lemma 2, (S8)–(S12)](../science/spectral_law.md#lemma-2-a-converse-for-arbitrary-encoding-and-classical-records).

### M16: Local row sums complete the uniform occupancy law

**Central question.** How can local spectral counts bound a global Gaussian matrix independently of dimension?

**Understanding target.** Explain the partition into intervals of one resolution width, the summable Gaussian envelope and the maximum-row-sum estimate. Combine this bound with M13 and M15 to obtain the fixed-error additive-constant characterization of stored logical qubits.

**Dependencies and story role.** Integrates M12–M15 into the first principal result, including its uniformity and unoptimized constants.

**Conceptual connection.** The same occupancy statistic certifies both a useful code and the limit of every allowed code.

**Sources.** [Watrous §1.1.3][W1], [§4.1.3][W4]; [Lemma 3, (S13)–(S14)](../science/spectral_law.md#lemma-3-gaussian-row-sums-from-local-occupancy); [Theorem 1](../science/spectral_law.md#theorem-1-one-register-storage).

### M17: The exact-error boundary and degeneracy

**Central question.** Why does demanding zero error recover exact eigenspace multiplicity rather than finite-resolution occupancy?

**Understanding target.** Explain the role of strict positivity of the distinct-level Gaussian kernel, its positive block-dephasing component, and extremality of the identity channel. Connect exact correction to the largest eigenspace dimension and distinguish this statement from taking the approximate theorem's constants to zero error.

**Dependencies and story role.** Uses M03, M08 and M16 to identify a sharp boundary of the storage characterization.

**Conceptual connection.** Approximate spectral proximity and exact noiseless structure support different operational guarantees.

**Sources.** [Watrous §§2.2.2–2.2.4][W2]; [Proposition 2, (S15)](../science/spectral_law.md#proposition-2-exact-storage-at-every-positive-time).

### M18: Certified couplings and an exact dyadic grid

**Central question.** How can finite classical input certify a useful code for true couplings that need not be rational?

**Understanding target.** Separate supplied estimates, uncertainty certificates and actual coefficients. Explain exact dyadic grid selection from rational exposure and error, the precision condition, and the accumulated energy discrepancy for a basis string. Identify the guarantee as uniform over each fixed coupling vector consistent with the certificates throughout storage.

**Dependencies and story role.** Uses M09, M12 and M16 to turn the characterization into a finite-input construction.

**Conceptual connection.** Calibration uncertainty determines which spectral-band argument remains physically valid.

**Sources.** [Watrous §1.1.2][W1]; [encoder, §1 and (2)–(7)](../science/encoder.md#1-exact-dyadic-grid-selection).

### M19: Signed weights and the optimal closed band

**Central question.** How does the rounded spectrum become an exact counting problem without losing negative weights or degeneracies?

**Understanding target.** Explain the known bit flips that replace signed weights by nonnegative ones. Preserve zero-weight multiplicities and distinguish an integer band's diameter from its number of integer values. Identify the deterministic maximizing band and the power-of-two subset used for logical qubits.

**Dependencies and story role.** Converts M18's calibration statement into the discrete object the compiler will count.

**Conceptual connection.** A unitary relabeling preserves the physical problem while simplifying classical arithmetic.

**Sources.** [Watrous §2.2.2][W2]; [encoder, §2 and (8)–(10)](../science/encoder.md#2-signed-weights-and-the-optimal-closed-band).

### M20: Physical protection and constant-qubit optimality

**Central question.** Why is the chosen rounded band protected and close to the true unrestricted optimum?

**Understanding target.** Combine rounded bandwidth with calibration discrepancy to bound the true spectral diameter. Explain why every sufficiently narrow true interval fits an allowed rounded band, then connect its population to the occupancy converse. Track the additional loss when taking a power-of-two code dimension.

**Dependencies and story role.** Joins M13, M16 and M18–M19 to certify the construction before its implementation.

**Conceptual connection.** The same uncertainty bound controls both storage error and instance-wise optimality.

**Sources.** [Watrous §3.3.2][W3]; [encoder, (11)–(13)](../science/encoder.md#storage-error); [constant-qubit guarantee](../science/encoder.md#constant-qubit-optimality).

### M21: Counting accepted suffixes exactly

**Central question.** How can the compiler count an exponentially large set without listing its members?

**Understanding target.** Interpret suffix subset-sum counts and their recurrence, then explain how prefix sums count accepted completions of a partial string. Track the bit width of counts, including zero weights and the all-strings case, and the cost of finding the maximizing closed band.

**Dependencies and story role.** Implements the discrete search defined in M19 while preserving the certificate in M20.

**Conceptual connection.** Exact counting supplies a compact description from which coherent codeword selection can be constructed.

**Sources.** [Watrous §2.1.2][W2] for basis labels; [encoder, §3 and (14)–(16)](../science/encoder.md#3-exact-classical-preprocessing).

### M22: Ranking and unranking without listing codewords

**Central question.** How do accepted-completion counts provide reversible access to the selected codewords?

**Understanding target.** Explain how unranking chooses each next bit and how ranking accumulates preceding accepted strings. Identify their inverse relation on the selected code, and why total Boolean extensions outside that set are sufficient for circuit construction without becoming inverse there.

**Dependencies and story role.** Uses M10 and M21 to replace a population certificate by explicit maps on logical labels.

**Conceptual connection.** A compact classical description becomes an amplitude-independent quantum encoding route.

**Sources.** [Watrous §2.2.2][W2] for isometries; [encoder, rank/unrank construction](../science/encoder.md#4-rank-and-unrank-as-total-boolean-circuits).

### M23: Compiled lookups and charged polynomial resources

**Central question.** Which operations and storage must be counted before the compiler can be called efficient?

**Understanding target.** Explain equality-controlled table scans and explicit arithmetic gates without a unit-cost quantum-memory oracle. Account for table bits, count widths, emitted gates, work qubits and the circuit description. Relate polynomial cost to the integer sum range and distinguish polynomial exposure from polynomial dependence on its bit length.

**Dependencies and story role.** Attaches an implementation cost to M21–M22 using M09's resource distinctions.

**Conceptual connection.** An efficiently specified isometry requires an explicit computational realization.

**Sources.** [Watrous §2.2.2][W2]; [encoder, (7), (16)–(18) and compilation costs](../science/encoder.md#4-rank-and-unrank-as-total-boolean-circuits).

### M24: A clean unknown-register isometry and decoder

**Central question.** How is the logical input transferred completely into the physical code before storage?

**Understanding target.** Explain compute-copy-uncompute, followed by ranking to erase the original logical label. Identify the resulting phase-free basis permutation and its linear action on reference-entangled states. Follow inverse decoding on the invariant code span and the full trace-preserving channel obtained by discarding non-output registers.

**Dependencies and story role.** Integrates M06, M10 and M21–M23 into the actual quantum implementation.

**Conceptual connection.** Workspace cleanup enforces the physical-memory constraint, rather than merely improving memory usage.

**Sources.** [Watrous §§2.1.3, 2.2.2][W2]; [encoder, §5 and (19)–(20)](../science/encoder.md#5-clean-coherent-isometry-and-decoding-channel).

### M25: Composing storage and boundary-operation errors

**Central question.** How does the ideal storage certificate survive imperfect encoding and decoding?

**Understanding target.** Combine half-diamond errors using channel contractivity and the triangle inequality. Identify the reserved boundary-operation budget and how operation-level errors may be summed when they are composable. Include discarded imperfect workspace and noisy initialization in the appropriate boundary channel.

**Dependencies and story role.** Connects M05, M20 and M24 to an explicit total-error statement.

**Conceptual connection.** A mathematical storage guarantee and an implementation-error assumption fit into the same channel metric; neither determines hardware overhead by itself.

**Sources.** [Watrous §§3.3.2–3.3.3][W3]; [encoder, §6 and (21)–(23)](../science/encoder.md#6-composable-implementation-error-budget).

### M26: What the examples and primitive circuits establish

**Central question.** Which aspects of the result become visible in a small code, a larger spectrum and executable circuits?

**Understanding target.** Connect the two-qubit worked example to the nondegenerate 16-qubit bands and the small primitive-gate checks. Distinguish exact arithmetic, tested state errors, analytic channel bounds and a conservative converse ceiling. Explain what enumeration verifies and why the general compiler avoids that enumeration.

**Dependencies and story role.** Brings M12–M25 together in concrete instances while keeping the evidence levels explicit.

**Conceptual connection.** Examples expose the mechanism and implementation; uniform claims retain their analytical proofs.

**Sources.** [Watrous §§3.2–3.3][W3]; [worked example](anchor.md#worked-example-one-logical-qubit-without-an-exact-degeneracy); [examples](../science/examples.md); [verification limits](../verification/README.md#what-the-checks-do-not-establish).

### M27: Variance, extensive storage and the order of limits

**Central question.** How can nearly all qubits remain storable at polynomial exposures while each fixed nondegenerate register eventually loses its memory?

**Understanding target.** Connect spectral variance, concentration and occupancy to the extensive-rate bound. Distinguish a growing family of registers at prescribed exposures from infinite time at fixed dimension. Relate homogeneous fixed-weight sectors and Proposition 2 to these approximate finite-time conclusions.

**Dependencies and story role.** Synthesizes M16–M17, M20 and M26 into the main storage interpretation.

**Conceptual connection.** The limiting noiseless algebra and finite-resolution spectral population answer different asymptotic questions.

**Sources.** [Watrous §4.1.3][W4]; [variance bound, (I2)–(I4)](../science/interpretation.md#a-rate-bound-from-spectral-variance); [infinite-time limit, (I5)](../science/interpretation.md#finite-time-and-the-infinite-time-algebra).

### M28: Independent-use achievability from environmental entropy

**Central question.** What additional communication statement follows when complete memory channels are used independently?

**Understanding target.** Define the new experiment with fresh noise for every complete use. Explain the coherent-state dilation, displacement to the occupied interval's midpoint, environmental entropy bound and coherent-information achievable rate. Recognize the oscillator as a mathematical representation, without imposing a physical bath-energy constraint.

**Dependencies and story role.** Uses M03, M12 and M16 for a separate corollary, beyond the single-interval storage theorem.

**Conceptual connection.** Limited environmental distinguishability turns spectral crowding into an asymptotic communication rate.

**Sources.** [Watrous §5.2][W5], [§8.2.2][W8]; [interpretation, (I7)–(I10) and Devetak attribution](../science/interpretation.md#lower-bound-and-coherent-state-normalization).

### M29: Adaptive classical assistance and the converse rate

**Central question.** How does the one-use comparator constrain protocols with classical communication between independent uses?

**Understanding target.** Follow successive channel replacements through an adaptive deterministic protocol. Explain why the comparison output remains separable without initial shared entanglement, and how its target overlap yields an exponentially vanishing fidelity above the bound. Distinguish this rate bound from equality of assisted and unassisted capacities.

**Dependencies and story role.** Combines M08, M14–M15 and M28 to complete the independent-use corollary.

**Conceptual connection.** Complete positivity allows the same comparison argument to survive arbitrary permitted inter-use processing.

**Sources.** [Watrous §6.1.2][W6], [§8.2.1][W8]; [interpretation, (I11)–(I12)](../science/interpretation.md#upper-bound-for-adaptive-classical-assistance).

### M30: The combined contribution and its physical scope

**Central question.** What does the occupancy law together with the calibrated compiler establish about this memory model?

**Understanding target.** Connect arbitrary-code optimality, finite-input construction and clean quantum implementation into one instance-wise guarantee. Separate the unrestricted spectral theorem from its efficient weighted-qubit realization, fixed-error conclusions from exact storage, and single-interval storage from independent-use communication. Identify inherited techniques and the assumptions needed for a physical application.

**Dependencies and story role.** Integrates M11–M29 into the project's complete scientific claim.

**Conceptual connection.** Finite spectral resolution replaces exact degeneracy as the useful organizing quantity for approximate storage.

**Sources.** [Watrous §3.3.3][W3], [§8.2.1][W8]; [scientific synthesis](../science/README.md); [specific contribution and limits](../references/related_work.md#what-remains-after-these-comparisons).

[Scientific account](../science/README.md) · [Anchor and bridge](anchor.md) · [Repository overview](../README.md)

[W1]: https://jhwatrous.github.io/TQI.1.pdf
[W2]: https://jhwatrous.github.io/TQI.2.pdf
[W3]: https://jhwatrous.github.io/TQI.3.pdf
[W4]: https://jhwatrous.github.io/TQI.4.pdf
[W5]: https://jhwatrous.github.io/TQI.5.pdf
[W6]: https://jhwatrous.github.io/TQI.6.pdf
[W8]: https://jhwatrous.github.io/TQI.8.pdf
