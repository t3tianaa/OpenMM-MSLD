---
id: REQ-016
type: requirement
title: Canonical sampling of atoms and theta
area: engine
priority: must
status: partial
derives_from: ["[[G-2 Physically correct MSLD|G-2]]"]
satisfied_by: ["[[FEAT-008 Lambda-dynamics integrator|FEAT-008]]"]
verified_by: ["test_integrator", "[[EXP-001 Theta samples the exact Boltzmann distribution on a toy|EXP-001]]"]
decisions: ["[[ADR-0012 Python driver integrator instead of CustomIntegrator|ADR-0012]]", "[[ADR-0038 Theta units and default theta mass|ADR-0038]]"]
created: 2026-08-10
updated: 2026-09-27
retrospective: true
---
# REQ-016 — Canonical sampling of atoms and θ

**Statement.** Atoms and θ shall be integrated by a Langevin scheme that samples the Boltzmann
distribution at temperature T; the θ kinetic temperature shall equal T within statistical error in
production systems.

## Acceptance criteria
- [x] AC1 — exact λ/θ distribution on an analytic toy site ([[EXP-001 Theta samples the exact Boltzmann distribution on a toy|EXP-001]]).
- [ ] AC2 — θ temperature ≈ T on MDM2 with reference-equivalent θ mass/friction ([[TASK-033 Rerun MDM2 with reference theta parameters|TASK-033]],
  [[ISS-018 Theta runs hot in MDM2|ISS-018]]).
- [ ] AC3 — λ histograms match BLaDE for the same system ([[REQ-070 Agree with BLaDE on a shared CHARMM system|REQ-070]]).

