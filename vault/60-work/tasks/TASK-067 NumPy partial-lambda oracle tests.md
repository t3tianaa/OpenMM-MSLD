---
id: TASK-067
type: task
title: NumPy partial-lambda oracle tests
status: done
kind: test
priority: P1
milestone: M4
feature: "[[FEAT-045 Independent partial-lambda oracle tests|FEAT-045]]"
issues: ["[[ISS-012 No validation at partial lambda|ISS-012]]"]
refs: ["[[Partial-lambda oracle tests]]", "[[Multisite lambda dynamics]]", "[[Alchemical scaling rules in MSLD]]"]
created: 2026-09-27
updated: 2026-10-31
---
# TASK-067 — NumPy oracle for partial-λ energies and dU/dλ

## Acceptance criteria
- [x] Independent NumPy implementation of the MSLD energy for NoCutoff systems (bonded + LJ + Coulomb
      + 1-4 + biases + restraints), written from the theory notes, not from `forces.py`.
- [x] 2 sites × (3, 2) blocks toy; ≥ 20 random interior λ vectors; energies and all dU/dλ agree to
      1e-8 relative on Reference.
- [x] Runs in < 30 s; part of the suite.


**Done (2026-10-31).** `tests/msld_oracle.py` (pure NumPy, complex-step dU/dλ and dU/dθ) and
`tests/test_oracle_partial_lambda.py`: 2 sites × (3, 2) blocks, 24 random λ vectors with soft-core on
and off, a soft-core overlap case (env atom 0.01 nm from a block atom, λ down to 1e-3), and dU/dθ
through the softmax. Energies, every dU/dλ and dU/dθ agree to 1e-8 relative on Reference; ~3 s.
Mutating the oracle (within-block λ² Coulomb, a wrong cross-site product) makes the tests fail.
`tests/data/oracle_toy.json` freezes the parameters and 8 reference (λ, E, dU/dλ) cases for the
plugin's own tests. The only discrepancy found was the oracle's own dihedral sign (fixed to IUPAC,
as OpenMM), so no engine bug turned up.
