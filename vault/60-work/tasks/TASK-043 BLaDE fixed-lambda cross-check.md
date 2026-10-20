---
id: TASK-043
type: task
title: BLaDE fixed-lambda cross-check
status: todo
kind: test
priority: P1
milestone: M5
feature: "[[FEAT-030 BLaDE cross-validation harness|FEAT-030]]"
issues: ["[[ISS-012 No validation at partial lambda|ISS-012]]", "[[ISS-006 Same-site PME differs from BLaDE and docs are backwards|ISS-006]]"]
depends_on: ["[[TASK-042 Get BLaDE running with reference data|TASK-042]]", "[[TASK-045 Import BLaDE MSLD setups|TASK-045]]", "[[TASK-070 CHARMM force switching for the cross-check|TASK-070]]"]
refs: ["[[BLaDE cross-validation harness]]"]
created: 2026-09-27
updated: 2026-09-27
---
# TASK-043 — BLaDE fixed-λ per-term cross-check on a small CHARMM system

Per [[BLaDE cross-validation harness]]; soft-core off first; account for the same-site PME
convention ([[ADR-0036 Same-site reciprocal-space convention|ADR-0036]]).

