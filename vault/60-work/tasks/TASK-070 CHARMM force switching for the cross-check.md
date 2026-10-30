---
id: TASK-070
type: task
title: CHARMM force switching for the cross-check
status: todo
kind: impl
priority: P1
milestone: M5
feature: "[[FEAT-030 BLaDE cross-validation harness|FEAT-030]]"
refs: ["[[Cutoffs, switching and dispersion correction]]", "[[BLaDE nonbonded direct space]]"]
created: 2026-09-27
updated: 2026-09-27
---
# TASK-070 — CHARMM force switching (vfswitch) for the BLaDE cross-check

BLaDE only does vfswitch; OpenMM's NonbondedForce only potential switching. Build the CHARMM
reference System with a force-switched LJ `CustomNonbondedForce` (as CHARMM-GUI does) and make the
MSLD LJ copies use the same expression.

