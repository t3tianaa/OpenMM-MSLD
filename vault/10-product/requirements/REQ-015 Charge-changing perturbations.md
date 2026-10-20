---
id: REQ-015
type: requirement
title: Charge-changing perturbations
area: engine
priority: could
status: deferred
derives_from: ["[[G-1 Free energies for many variants at once|G-1]]"]
satisfied_by: ["[[FEAT-037 Charge-changing perturbations|FEAT-037]]"]
created: 2026-08-13
updated: 2026-09-27
retrospective: true
---
# REQ-015 — Charge-changing perturbations

**Statement.** Support variants with different net charge, using BLaDE-style charge restraints or
co-alchemical ions ([[Net charge changes in alchemical calculations]], [[BLaDE charge restraints]]).
Until then prep refuses unequal net charges ([[ADR-0021 Charge averaging, renormalization, iso-charge guard|ADR-0021]]).

