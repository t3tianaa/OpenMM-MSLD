---
id: REQ-005
type: requirement
title: Nonbonded pair scaling rules
area: engine
priority: must
status: implemented
derives_from: ["[[G-2 Physically correct MSLD|G-2]]"]
satisfied_by: ["[[FEAT-003 Electrostatics scaling|FEAT-003]]", "[[FEAT-004 Lennard-Jones scaling|FEAT-004]]"]
verified_by: ["test_lj", "test_electrostatics", "test_within_block_elec", "test_grill", "test_master"]
decisions: ["[[ADR-0007 Charges scaled by NonbondedForce offsets|ADR-0007]]", "[[ADR-0008 LJ scaled by grouped CustomNonbondedForces|ADR-0008]]", "[[ADR-0009 Within-block real-space electrostatics linear|ADR-0009]]"]
created: 2026-08-05
updated: 2026-09-27
retrospective: true
---
# REQ-005 — Nonbonded pair scaling rules

**Statement.** Direct-space nonbonded pair energies (LJ and Coulomb) shall be scaled:
env–env 1; env–block b and within block b → λ_b (linear); blocks at different sites → λ_b·λ_c;
same site, different blocks → 0 ([[REQ-006 Same-site pairs never interact|REQ-006]]). This is BLaDE's `nbdirect` rule
([[BLaDE nonbonded direct space]], [[Alchemical scaling rules in MSLD]]).

## Acceptance criteria
- [x] AC1 — LJ follows the rule exactly with analytic dU/dλ (`test_lj`).
- [x] AC2 — direct-space Coulomb within a block is linear (NoCutoff, PME real space) (`test_within_block_elec`).
- [ ] AC3 — correct for every supported nonbonded method (fails for reaction-field cutoffs, [[ISS-003 Within-block correction wrong for cutoff methods|ISS-003]]).
- [ ] AC4 — matches BLaDE at partial λ ([[REQ-070 Agree with BLaDE on a shared CHARMM system|REQ-070]]).

