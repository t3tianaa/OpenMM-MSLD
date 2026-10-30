---
id: REQ-003
type: requirement
title: Scale bonded terms by block lambdas
area: engine
priority: must
status: implemented
derives_from: ["[[G-2 Physically correct MSLD|G-2]]"]
satisfied_by: ["[[FEAT-002 Bonded term scaling|FEAT-002]]"]
verified_by: ["test_builder", "test_angles_torsions", "test_charmm_terms", "test_master"]
decisions: ["[[ADR-0006 Bonded scaling via grouped custom forces|ADR-0006]]"]
created: 2026-07-31
updated: 2026-09-27
retrospective: true
---
# REQ-003 — Scale bonded terms by block λ's

**Statement.** A bonded term (bond, Urey–Bradley, angle, proper and improper dihedral) whose atoms
touch non-environment blocks shall be multiplied by the product of the distinct block λ's
(at most 2 for these terms; CMAP up to 3, see [[REQ-010 CMAP scaling|REQ-010]]). A term that spans two blocks of the
**same** site is illegal and shall raise.

## Acceptance criteria
- [x] AC1 — env-only terms unchanged; env+block → λ_b; blocks at different sites → λ_b·λ_c.
- [x] AC2 — analytic ∂U/∂λ equals finite difference.
- [x] AC3 — same-site spanning term raises (`classify_bonded`).
- [ ] AC4 — per-term values match BLaDE at partial λ ([[REQ-070 Agree with BLaDE on a shared CHARMM system|REQ-070]]).

