---
id: REQ-010
type: requirement
title: CMAP scaling
area: engine
priority: should
status: deferred
derives_from: ["[[G-2 Physically correct MSLD|G-2]]", "[[UC-1 Protein mutation scan|UC-1]]"]
satisfied_by: ["[[FEAT-036 CMAP scaling|FEAT-036]]"]
decisions: ["[[ADR-0028 Refuse what cannot be scaled|ADR-0028]]"]
created: 2026-08-19
updated: 2026-09-27
retrospective: true
---
# REQ-010 — CMAP scaling

**Statement.** CHARMM CMAP terms touching alchemical atoms shall be scaled by the product of up to
3 block λ's (BLaDE `cmap_scaling`, Nsc = 3), or the builder shall refuse them.

Status: refused by a guard today (backbone mutations under CHARMM36/ff19SB). Needed for Gly/Pro
mutations with CHARMM force fields ([[UC-1 Protein mutation scan|UC-1]]).

