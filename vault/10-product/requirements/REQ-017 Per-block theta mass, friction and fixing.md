---
id: REQ-017
type: requirement
title: Per-block theta mass, friction and fixing
area: engine
priority: must
status: partial
derives_from: ["[[G-2 Physically correct MSLD|G-2]]", "[[UC-4 Fixed-lambda windows|UC-4]]"]
satisfied_by: ["[[FEAT-008 Lambda-dynamics integrator|FEAT-008]]"]
decisions: ["[[ADR-0038 Theta units and default theta mass|ADR-0038]]"]
created: 2026-08-10
updated: 2026-09-27
retrospective: true
---
# REQ-017 — Per-block θ mass, friction and fixing

**Statement.** Each block shall have its own θ mass, θ friction and initial θ/θ-velocity, and can
be fixed at a λ value (BLaDE `msld fix` / per-block fixed flag) with the other blocks of the site
renormalized to `1 − Σ λ_fixed`. Units and defaults shall be documented and equivalent to BLaDE's
([[BLaDE units and theta mass]]).

## Acceptance criteria
- [x] AC1 — per-block mass/friction honoured.
- [ ] AC2 — fixed-block λ semantics like BLaDE ([[ISS-019 Fixed-block lambda semantics differ from BLaDE|ISS-019]]).
- [ ] AC3 — units/defaults equivalent to BLaDE ([[ISS-002 Theta mass convention differs from BLaDE|ISS-002]]).

