---
id: REQ-008
type: requirement
title: LJ scaling including NBFIX
area: engine
priority: must
status: partial
derives_from: ["[[G-2 Physically correct MSLD|G-2]]", "[[G-3 Automated system preparation|G-3]]"]
satisfied_by: ["[[FEAT-004 Lennard-Jones scaling|FEAT-004]]"]
verified_by: ["test_lj", "test_charmm_nbfix_lj"]
decisions: ["[[ADR-0008 LJ scaled by grouped CustomNonbondedForces|ADR-0008]]"]
created: 2026-08-05
updated: 2026-09-27
retrospective: true
---
# REQ-008 — LJ scaling including NBFIX

**Statement.** Lennard-Jones shall be λ-scaled for Amber (Lorentz–Berthelot in `NonbondedForce`)
and CHARMM (tabulated A/B with NBFIX), on every platform, with analytic dU/dλ.

## Acceptance criteria
- [x] AC1 — Amber and CHARMM LJ λ = 1 ≡ base; analytic dU/dλ.
- [ ] AC2 — CHARMM NBFIX systems run on CPU ([[ISS-004 CHARMM NBFIX systems fail on CPU|ISS-004]]).
- [ ] AC3 — switching function form matches the force field (CHARMM vfswitch for BLaDE
  comparison, [[TASK-070 CHARMM force switching for the cross-check|TASK-070]]).

