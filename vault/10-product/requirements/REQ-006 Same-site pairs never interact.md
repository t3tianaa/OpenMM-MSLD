---
id: REQ-006
type: requirement
title: Same-site pairs never interact
area: engine
priority: must
status: implemented
derives_from: ["[[G-2 Physically correct MSLD|G-2]]"]
satisfied_by: ["[[FEAT-003 Electrostatics scaling|FEAT-003]]", "[[FEAT-004 Lennard-Jones scaling|FEAT-004]]"]
verified_by: ["test_electrostatics", "test_grill", "test_minimize"]
decisions: ["[[ADR-0010 Same-site pairs excluded in every nonbonded force|ADR-0010]]", "[[ADR-0036 Same-site reciprocal-space convention|ADR-0036]]"]
created: 2026-08-05
updated: 2026-09-27
retrospective: true
---
# REQ-006 — Same-site pairs never interact

**Statement.** Atoms of different blocks at the same site shall have zero direct-space
interaction at every λ. The treatment of their **reciprocal-space** (PME) interaction shall be a
documented, deliberate choice ([[ADR-0036 Same-site reciprocal-space convention|ADR-0036]]), and the BLaDE comparison shall account for it.

## Acceptance criteria
- [x] AC1 — direct space: pairs excluded in all nonbonded forces.
- [x] AC2 — every nonbonded force carries the same exclusion set (platform requirement, [[OpenMM exclusion parity across nonbonded forces]]).
- [ ] AC3 — reciprocal-space convention decided and documented; docs currently describe BLaDE
  backwards ([[ISS-006 Same-site PME differs from BLaDE and docs are backwards|ISS-006]]).

