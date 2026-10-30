---
id: ADR-0028
type: adr
title: Refuse what cannot be scaled
status: accepted
date: 2026-08-05
deciders: [Tetiana]
affects: ["[[Force scaling component]]", "[[Charge renormalization]]"]
requirements: ["[[REQ-022 Refuse unsupported input loudly|REQ-022]]", "[[REQ-010 CMAP scaling|REQ-010]]", "[[REQ-009 1-4 pair scaling|REQ-009]]", "[[REQ-015 Charge-changing perturbations|REQ-015]]"]
retrospective: true
---
# ADR-0028 — Refuse what cannot be scaled correctly

## Decision
Raise instead of producing silently wrong physics: alchemical CMAP (`_check_unhandled`), cross-site
and same-site 1-4 exceptions, same-site bonded terms, charge-changing sites, alchemical atoms with
remaining charge/LJ in an unexpected `NonbondedForce`.

## Consequences
- Some real systems (CHARMM backbone mutations) cannot run yet ([[ISS-015 Cross-site 1-4 and CMAP are refused|ISS-015]]).
- The guard is incomplete: only CMAP is checked among force types ([[ISS-005 Unsupported force types silently unscaled|ISS-005]]) → extended by
  [[ADR-0037 Whitelist force types|ADR-0037]] (proposed).

