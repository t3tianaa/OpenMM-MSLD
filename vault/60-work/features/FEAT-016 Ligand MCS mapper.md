---
id: FEAT-016
type: feature
title: Ligand MCS mapper
status: done
milestone: M3
implements: ["[[REQ-043 Map ligand R-group sites|REQ-043]]"]
components: ["[[Mapping component]]"]
decisions: ["[[ADR-0019 Core defined by identity and equal LJ|ADR-0019]]"]
tasks: ["[[TASK-016 MCS ligand mapper and RDKit|TASK-016]]"]
created: 2026-08-19
updated: 2026-09-27
retrospective: true
---
# FEAT-016 — Ligand MCS mapper

`MCSMapper` with RDKit, ring-break guard, LJ filter. Unit-tested; no real ligand series built yet
([[UC-2 Ligand R-group scan|UC-2]]).

