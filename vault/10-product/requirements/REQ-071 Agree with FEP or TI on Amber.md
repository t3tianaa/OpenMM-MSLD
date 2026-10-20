---
id: REQ-071
type: requirement
title: Agree with FEP or TI on Amber
area: validation
priority: should
status: proposed
derives_from: ["[[G-2 Physically correct MSLD|G-2]]", "[[UC-4 Fixed-lambda windows|UC-4]]"]
satisfied_by: ["[[FEAT-041 Amber validation vs FEP or TI|FEAT-041]]"]
created: 2026-09-01
updated: 2026-09-27
retrospective: true
---
# REQ-071 — Agree with FEP/TI on Amber

**Statement.** Because BLaDE cannot read Amber, validate the Amber path by comparing MSLD ΔG for a
simple perturbation with an independent FEP/TI calculation (e.g. openmmtools / OpenFE) using the
same force field, within combined uncertainty.

