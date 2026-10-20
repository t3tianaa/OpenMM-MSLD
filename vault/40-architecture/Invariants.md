---
title: Invariants
type: architecture
status: as-built
decisions: ["[[ADR-0011 Master invariant as the primary gate|ADR-0011]]", "[[ADR-0010 Same-site pairs excluded in every nonbonded force|ADR-0010]]", "[[ADR-0009 Within-block real-space electrostatics linear|ADR-0009]]", "[[ADR-0021 Charge averaging, renormalization, iso-charge guard|ADR-0021]]"]
updated: 2026-09-27
---
# Invariants

Properties that must hold after every change. Each has a guard (test or runtime check).

| # | invariant | why | guard |
|---|---|---|---|
| I1 | **Master invariant**: at λ = 1 for every block (biases/restraints off) the scaled System reproduces the base System's energy **and** forces to machine precision | proves the rewriting is pure bookkeeping | `tests/test_master.py` (~1e-13) |
| I2 | per site Σ λ = 1, λ ∈ (0,1); environment λ ≡ 1 | MSLD definition | softmax construction |
| I3 | every variant at a site has the same integer net charge | PME neutrality, no charge-change artefacts | `charges.assert_iso_charge` (raises) |
| I4 | no bonded term spans two blocks of the same site | mutually exclusive variants | `classify_bonded` (raises); `assert_no_cross_variant_terms` |
| I5 | same-site atom pairs never interact in direct space (all λ) | mutually exclusive, overlapping | exclusions in every nonbonded force |
| I6 | within-block real-space nonbonded is linear in λ_b; reciprocal is λ_b² | BLaDE convention | `test_within_block_elec` |
| I7 | shared atoms exist once (environment, block 0) | hybrid topology | assembler appends only block atoms |
| I8 | all nonbonded forces carry identical exclusion sets | CPU/OpenCL/CUDA requirement | `test_minimize::test_scaled_forces_share_one_exclusion_set` |
| I9 | prep's plain System has no MSLD modifications and loses no parameters (NBFIX kept) | makes I1 meaningful; correctness of parameters | `test_hybrid_builder` (WT-on = original peptide, 3e-15) |
| I10 | the engine never silently leaves a λ-dependent term unscaled | correctness | `_check_unhandled` (**incomplete**, [[ISS-005 Unsupported force types silently unscaled\|ISS-005]]) |

**I1 is necessary, not sufficient.** λ = 1 for *every* block is not a physical MSLD state. Partial-λ
correctness needs independent checks ([[Partial-lambda oracle tests]], [[BLaDE cross-validation harness]]).
Planned invariant I11: *at any λ, energies and dU/dλ equal an independent reference within
tolerance* ([[REQ-070 Agree with BLaDE on a shared CHARMM system|REQ-070]]).

