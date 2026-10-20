---
id: TASK-016
type: task
title: MCS ligand mapper and RDKit
status: done
kind: impl
priority: P1
milestone: M3
feature: "[[FEAT-016 Ligand MCS mapper|FEAT-016]]"
created: 2026-08-19
done: 2026-08-21
retrospective: true
---
# TASK-016 — MCS ligand mapper (Phase J) and RDKit as a hard dependency

`MCSMapper`, shared `build_hybrid_local_mapping`, buffer-aware renormalizer; RDKit made a hard
dependency, which exposed and fixed an unsanitized-ring bug ([[ADR-0030 Hard dependencies and a ParmEd-free engine|ADR-0030]]).

