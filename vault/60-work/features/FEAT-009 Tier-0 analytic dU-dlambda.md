---
id: FEAT-009
type: feature
title: Tier-0 analytic dU/dlambda
status: done
milestone: M2
implements: ["[[REQ-020 Accurate dU-dlambda for every term|REQ-020]]"]
components: ["[[Force groups and derivative routing]]"]
decisions: ["[[ADR-0013 Tier 0 analytic dU-dlambda via force groups|ADR-0013]]"]
tasks: ["[[TASK-026 Tier 0 analytic dU-dlambda|TASK-026]]"]
issues: ["[[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]"]
created: 2026-09-17
updated: 2026-09-27
retrospective: true
---
# FEAT-009 — Tier-0 analytic dU/dλ

Force-group split; analytic derivatives from the same `getState`; FD only group 0. Verified
([[EXP-008 Tier-0 derivative exactness|EXP-008]]).

