---
id: FEAT-017
type: feature
title: Hybrid structure grafting
status: done
milestone: M3
implements: ["[[REQ-044 Multiple sites per system|REQ-044]]", "[[REQ-045 Place variant coordinates in the shared frame|REQ-045]]", "[[REQ-048 No bonded term between same-site blocks|REQ-048]]"]
components: ["[[Grafting and term transplant]]", "[[Coordinate alignment]]"]
decisions: ["[[ADR-0017 Staged prep pipeline|ADR-0017]]"]
tasks: ["[[TASK-010 Merge per-variant topologies with ParmEd|TASK-010]]", "[[TASK-011 Cross-variant check and CHARMM impropers|TASK-011]]", "[[TASK-015 Prep redesign phases A to I|TASK-015]]"]
issues: ["[[ISS-024 Core-only bonded terms take reference parameters|ISS-024]]"]
created: 2026-08-14
updated: 2026-09-27
retrospective: true
---
# FEAT-017 — Hybrid structure grafting

Align, append block atoms, transplant block-touching terms, cross-variant guard. Gate test: WT-on =
original peptide to 3e-15.

