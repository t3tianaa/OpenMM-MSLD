---
id: TASK-067
type: task
title: NumPy partial-lambda oracle tests
status: todo
kind: test
priority: P1
milestone: M4
feature: "[[FEAT-045 Independent partial-lambda oracle tests|FEAT-045]]"
issues: ["[[ISS-012 No validation at partial lambda|ISS-012]]"]
refs: ["[[Partial-lambda oracle tests]]", "[[Multisite lambda dynamics]]", "[[Alchemical scaling rules in MSLD]]"]
created: 2026-09-27
updated: 2026-09-27
---
# TASK-067 — NumPy oracle for partial-λ energies and dU/dλ

## Acceptance criteria
- [ ] Independent NumPy implementation of the MSLD energy for NoCutoff systems (bonded + LJ + Coulomb
      + 1-4 + biases + restraints), written from the theory notes, not from `forces.py`.
- [ ] 2 sites × (3, 2) blocks toy; ≥ 20 random interior λ vectors; energies and all dU/dλ agree to
      1e-8 relative on Reference.
- [ ] Runs in < 30 s; part of the suite.

