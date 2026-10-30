---
id: TASK-038
type: task
title: Refuse reaction-field cutoff methods
status: todo
kind: fix
priority: P1
milestone: M4
feature: "[[FEAT-047 Engine hardening|FEAT-047]]"
issues: ["[[ISS-003 Within-block correction wrong for cutoff methods|ISS-003]]"]
refs: ["[[ADR-0040 Supported nonbonded methods|ADR-0040]]", "[[Reaction-field electrostatics]]"]
created: 2026-09-27
updated: 2026-09-27
---
# TASK-038 — Refuse (or fix) reaction-field cutoff methods

Per [[ADR-0040 Supported nonbonded methods|ADR-0040]]: raise for CutoffPeriodic / CutoffNonPeriodic / LJPME; keep NoCutoff, Ewald, PME.

