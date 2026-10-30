---
id: REQ-014
type: requirement
title: Atom restraints between substituents
area: engine
priority: must
status: partial
derives_from: ["[[G-2 Physically correct MSLD|G-2]]"]
satisfied_by: ["[[FEAT-007 Atom restraints|FEAT-007]]"]
verified_by: ["test_restraints"]
decisions: ["[[ADR-0023 Restraint groups per block centroid|ADR-0023]]", "[[ADR-0033 Atom restraints group equivalent atoms|ADR-0033]]"]
created: 2026-08-10
updated: 2026-09-27
retrospective: true
---
# REQ-014 — Atom restraints between substituents

**Statement.** The engine shall support BLaDE atom restraints: each restraint **group** is a set of
**equivalent atoms taken from different substituents of one site** (e.g. the duplicated backbone N
of every variant), each atom held to the group's centroid with k = 59.2 kcal/mol/Å² (default),
not λ-scaled ([[Atom restraints between substituents]], [[BLaDE atom restraints and soft bonds]]).
Prep shall generate these groups when substituents duplicate equivalent atoms.

## Acceptance criteria
- [x] AC1 — restraint force math (centroid ⇔ pairwise identity) correct (`test_restraints`).
- [ ] AC2 — groups are equivalent-atom groups, one atom per substituent ([[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]]).
- [ ] AC3 — prep emits groups only where needed (duplicated core atoms), none for plain side
  chains.

