---
id: REQ-031
type: requirement
title: Reproducible runs
area: run
priority: should
status: partial
derives_from: ["[[G-6 Traceable engineering process|G-6]]"]
created: 2026-09-27
updated: 2026-09-27
---
# REQ-031 — Reproducible runs

**Statement.** Every run shall record its inputs, code version (git commit), library versions,
platform/precision, all MSLD parameters and the random seed, so it can be repeated.

Status: `LambdaDynamics(seed=…)` exists; nothing is recorded automatically.
