---
id: TASK-045
type: task
title: Import BLaDE MSLD setups
status: todo
kind: impl
priority: P1
milestone: M5
feature: "[[FEAT-030 BLaDE cross-validation harness|FEAT-030]]"
refs: ["[[BLaDE input script language]]", "[[MSLD model data contract]]"]
created: 2026-09-27
updated: 2026-09-27
---
# TASK-045 — Import a BLaDE/CHARMM MSLD setup into an `MSLDModel`

Parse the `msld`/`selection` subset of a BLaDE input (or accept equivalent Python), map to blocks,
biases, flags; build the System from the same PSF + parameters ([[REQ-052 Import a BLaDE or CHARMM MSLD setup|REQ-052]]).

