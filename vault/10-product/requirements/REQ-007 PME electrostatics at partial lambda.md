---
id: REQ-007
type: requirement
title: PME electrostatics at partial lambda
area: engine
priority: must
status: partial
derives_from: ["[[G-2 Physically correct MSLD|G-2]]"]
satisfied_by: ["[[FEAT-003 Electrostatics scaling|FEAT-003]]"]
verified_by: ["test_electrostatics", "test_grill"]
decisions: ["[[ADR-0007 Charges scaled by NonbondedForce offsets|ADR-0007]]", "[[ADR-0009 Within-block real-space electrostatics linear|ADR-0009]]", "[[ADR-0036 Same-site reciprocal-space convention|ADR-0036]]"]
created: 2026-08-05
updated: 2026-09-27
retrospective: true
---
# REQ-007 — PME electrostatics at partial λ

**Statement.** With PME, charges shall be scaled by their block λ (reciprocal space λ_i·λ_j,
self-energy λ², within-block reciprocal λ²), matching BLaDE's `nbrecip` convention
([[PME with lambda-scaled charges]], [[BLaDE PME reciprocal space and exclusions]]); the Ewald
α used by any correction shall be the one the force actually uses.

## Acceptance criteria
- [x] AC1 — λ = 1 reproduces base PME energy and forces.
- [ ] AC2 — α read from the force, not re-derived from the tolerance ([[ISS-008 PME alpha recomputed from the tolerance|ISS-008]]).
- [ ] AC3 — partial-λ PME energy and dU/dλ match BLaDE ([[REQ-070 Agree with BLaDE on a shared CHARMM system|REQ-070]]).
- [ ] AC4 — analytic dU/dλ for PME ([[REQ-020 Accurate dU-dlambda for every term|REQ-020]]).

