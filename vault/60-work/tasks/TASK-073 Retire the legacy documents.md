---
id: TASK-073
type: task
title: Retire the legacy documents
status: done
kind: docs
priority: P2
milestone: M4
feature: "[[FEAT-044 Knowledge vault and process|FEAT-044]]"
refs: ["[[Migration map]]"]
created: 2026-09-27
updated: 2026-09-29
---
# TASK-073 — Retire or slim the legacy documents

After the owner reviews the vault: shrink `README.md` to a quick start pointing to the vault; move
`GUIDE.md`, `DEFERRED.md`, `PLUGIN_PLAN.md`, `AUDIT_2026-09-26.md` to `vault/80-history/legacy/` (or
delete); decide about `MSLD_obsidian/`.


**Done 2026-09-29:** owner chose deletion. `GUIDE.md`, `DEFERRED.md`, `PLUGIN_PLAN.md`,
`AUDIT_2026-09-26.md` and `MSLD_obsidian/` were deleted (never committed, so not recoverable from git);
code comments and `README.md` now point to vault notes. Also removed `test_systems/mdm2/out/` (regenerable run output).
