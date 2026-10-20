---
id: REQ-009
type: requirement
title: 1-4 pair scaling
area: engine
priority: must
status: partial
derives_from: ["[[G-2 Physically correct MSLD|G-2]]"]
satisfied_by: ["[[FEAT-005 1-4 exception scaling|FEAT-005]]"]
verified_by: ["test_exceptions"]
decisions: ["[[ADR-0007 Charges scaled by NonbondedForce offsets|ADR-0007]]"]
created: 2026-08-05
updated: 2026-09-27
retrospective: true
---
# REQ-009 — 1-4 pair scaling

**Statement.** 1-4 pairs shall scale like other pairs: within a block or env–block → λ_b;
different sites → λ_b·λ_c. Same-site 1-4 pairs are illegal (BLaDE `nb14_scaling` is fatal).

## Acceptance criteria
- [x] AC1 — single-λ 1-4 via exception offsets.
- [ ] AC2 — cross-site product-λ 1-4 ([[FEAT-039 Cross-site 1-4 scaling|FEAT-039]]); currently raises ([[ISS-015 Cross-site 1-4 and CMAP are refused|ISS-015]]).

