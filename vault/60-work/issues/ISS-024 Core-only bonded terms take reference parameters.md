---
id: ISS-024
type: issue
title: Core-only bonded terms take reference parameters
status: open
kind: risk
severity: low
confidence: inferred
affects: ["[[Grafting and term transplant]]"]
requirements: ["[[REQ-042 Map amino-acid mutation sites|REQ-042]]", "[[REQ-043 Map ligand R-group sites|REQ-043]]"]
fixed_by: ["[[TASK-040 Audit the preparation layer|TASK-040]]"]
found: 2026-09-27
updated: 2026-09-27
---
# ISS-024 — Bonded terms among core atoms silently use the reference variant's parameters

The grafting transplants only block-touching terms; terms whose atoms are all core come from the
environment (reference). If a variant's force field assigns different parameters to such a term,
the difference is lost without warning. Expected harmless for ff14SB backbones (identical types);
unverified for CHARMM36 and for ligands. Check in [[TASK-040 Audit the preparation layer|TASK-040]]: compare core-only term parameters
across variants and warn/raise on mismatch.

