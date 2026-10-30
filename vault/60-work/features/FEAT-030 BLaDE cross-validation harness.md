---
id: FEAT-030
type: feature
title: BLaDE cross-validation harness
status: planned
milestone: M5
implements: ["[[REQ-070 Agree with BLaDE on a shared CHARMM system|REQ-070]]", "[[REQ-052 Import a BLaDE or CHARMM MSLD setup|REQ-052]]"]
components: ["[[BLaDE cross-validation harness]]"]
decisions: ["[[ADR-0002 BLaDE is the reference and validation oracle|ADR-0002]]", "[[ADR-0036 Same-site reciprocal-space convention|ADR-0036]]"]
tasks: ["[[TASK-042 Get BLaDE running with reference data|TASK-042]]", "[[TASK-043 BLaDE fixed-lambda cross-check|TASK-043]]", "[[TASK-045 Import BLaDE MSLD setups|TASK-045]]", "[[TASK-070 CHARMM force switching for the cross-check|TASK-070]]"]
created: 2026-09-01
updated: 2026-09-27
---
# FEAT-030 — BLaDE cross-validation harness

Same CHARMM system in BLaDE and our engine; per-term energies and dU/dλ at a λ grid; then λ
statistics. The validation that closes "matches BLaDE".

