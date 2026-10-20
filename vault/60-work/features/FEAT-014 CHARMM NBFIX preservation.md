---
id: FEAT-014
type: feature
title: CHARMM NBFIX preservation
status: done
milestone: M3
implements: ["[[REQ-041 Lossless parameters including NBFIX|REQ-041]]"]
components: ["[[Ingest component]]", "[[Solvation]]"]
decisions: ["[[ADR-0018 Two ingest modes and NBFIX recovery|ADR-0018]]"]
tasks: ["[[TASK-012 Scale CHARMM NBFIX LJ|TASK-012]]", "[[TASK-013 Solvation by overlay|TASK-013]]"]
issues: ["[[ISS-025 NBFIX recovery assumes the OpenMM table convention|ISS-025]]"]
created: 2026-08-17
updated: 2026-09-27
retrospective: true
---
# FEAT-014 — CHARMM NBFIX preservation

`recover_charmm_lj` after OpenMM→ParmEd hops; ion–water NBFIX kept through solvation.

