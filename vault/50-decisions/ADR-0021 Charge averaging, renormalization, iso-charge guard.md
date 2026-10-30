---
id: ADR-0021
type: adr
title: Charge averaging, renormalization, iso-charge guard
status: accepted
date: 2026-08-13
deciders: [Tetiana]
affects: ["[[Charge renormalization]]"]
requirements: ["[[REQ-046 Consistent charges across variants|REQ-046]]", "[[REQ-015 Charge-changing perturbations|REQ-015]]"]
retrospective: true
---
# ADR-0021 — Average env charges, renormalize blocks to integers, refuse charge changes

## Context
Amber charges are fitted per residue, so a shared backbone atom has different charges in each
variant; the core can carry only one. Each end state must have an integer total charge. A site
whose variants differ in net charge changes the system charge with λ (PME artefacts).

## Decision
Per-atom average for env atoms (refuse if the spread > 0.5 e); spread each block's residual equally
(or by |q|) so env + block is an integer; require the same integer for all variants of a site.

## Consequences
- Small charge changes relative to the force field (documented, not validated against RESP refits).
- Charge-changing mutations (e.g. Lys → Ala) are refused until [[FEAT-037 Charge-changing perturbations|FEAT-037]].

