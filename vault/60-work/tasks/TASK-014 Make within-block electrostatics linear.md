---
id: TASK-014
type: task
title: Make within-block electrostatics linear
status: done
kind: impl
priority: P1
milestone: M1
feature: "[[FEAT-003 Electrostatics scaling|FEAT-003]]"
created: 2026-08-16
done: 2026-08-17
retrospective: true
---
# TASK-014 — Make within-block real-space electrostatics linear

`add_within_block_elec_correction`, `test_within_block_elec` ([[ADR-0009 Within-block real-space electrostatics linear|ADR-0009]]). Correct for NoCutoff and
PME only ([[ISS-003 Within-block correction wrong for cutoff methods|ISS-003]]).

