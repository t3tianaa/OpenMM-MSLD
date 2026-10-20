---
id: REQ-004
type: requirement
title: Configurable bonded scaling per term type
area: engine
priority: must
status: partial
derives_from: ["[[G-2 Physically correct MSLD|G-2]]"]
satisfied_by: ["[[FEAT-002 Bonded term scaling|FEAT-002]]"]
verified_by: ["test_biases"]
decisions: ["[[ADR-0014 Bonded scaling on by default|ADR-0014]]", "[[ADR-0041 Default bonded scaling follows BLaDE practice|ADR-0041]]"]
created: 2026-08-10
updated: 2026-09-27
retrospective: true
---
# REQ-004 — Configurable bonded scaling per term type

**Statement.** The user shall be able to turn λ-scaling off per bonded term type (bond, urey,
angle, dihedral, improper, cmap) exactly like BLaDE `msld removescaling`, including BLaDE's rule
that terms among **restrained** atoms stay scaled ([[BLaDE bonded term scaling]]).

**Rationale.** Production MSLD keeps a switched-off substituent attached to the core by *not*
scaling its bonds/angles ([[Bonded terms and dummy atoms in alchemy]]).

## Acceptance criteria
- [x] AC1 — `model.scale_bond / scale_angle / scale_torsion` switches (impropers follow torsion;
  Urey–Bradley follows bond — **check**).
- [ ] AC2 — separate switches for urey, dihe, impr, cmap (BLaDE has 6 flags).
- [ ] AC3 — restrained-atom exception implemented ([[ISS-023 Restrained-atom bonded scaling rule missing|ISS-023]]).
- [ ] AC4 — safe default matching BLaDE practice ([[ADR-0041 Default bonded scaling follows BLaDE practice|ADR-0041]], [[ISS-014 Bonded scaling defaults differ from BLaDE|ISS-014]]).

