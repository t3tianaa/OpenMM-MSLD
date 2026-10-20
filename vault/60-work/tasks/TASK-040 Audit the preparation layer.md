---
id: TASK-040
type: task
title: Audit the preparation layer
status: todo
kind: research
priority: P1
milestone: M4
feature: "[[FEAT-013 Ingest pipeline|FEAT-013]]"
issues: ["[[ISS-021 Preparation layer never audited|ISS-021]]", "[[ISS-024 Core-only bonded terms take reference parameters|ISS-024]]", "[[ISS-025 NBFIX recovery assumes the OpenMM table convention|ISS-025]]"]
refs: ["[[Preparation subsystem]]", "[[Ingest component]]", "[[Mapping component]]", "[[Assembly component]]"]
created: 2026-09-27
updated: 2026-09-27
---
# TASK-040 — Audit the preparation layer

Same rigor as [[AUD-001 Engine audit of the local working copy|AUD-001]]: read every prep module against its architecture note; run checks.
Questions to answer at least:
- [ ] core-only bonded terms: do variants disagree? ([[ISS-024 Core-only bonded terms take reference parameters|ISS-024]])
- [ ] charge averaging: size of changes vs force-field charges on MDM2; RESP-refit alternative?
- [ ] ligand path: which aligner works for MCS sites ([[Coordinate alignment]])? build and run one
      ligand pair end to end.
- [ ] `recover_charmm_lj` convention guard ([[ISS-025 NBFIX recovery assumes the OpenMM table convention|ISS-025]]); CHARMM hybrid end to end.
- [ ] solvation: water/FF mismatch detection; box size; ion placement.
- [ ] mapping JSON round trip and model reconstruction; multi-site.
Output: an AUD note + issues.

