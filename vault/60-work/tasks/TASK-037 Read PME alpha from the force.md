---
id: TASK-037
type: task
title: Read PME alpha from the force
status: todo
kind: fix
priority: P2
milestone: M4
feature: "[[FEAT-047 Engine hardening|FEAT-047]]"
issues: ["[[ISS-008 PME alpha recomputed from the tolerance|ISS-008]]"]
created: 2026-09-27
updated: 2026-09-27
---
# TASK-037 — Read PME α from the force, not from the tolerance

Use `getPMEParameters()`; if α = 0 (automatic), compute OpenMM's formula; test with a user-set α.

