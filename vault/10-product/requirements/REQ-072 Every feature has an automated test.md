---
id: REQ-072
type: requirement
title: Every feature has an automated test
area: process
priority: must
status: implemented
derives_from: ["[[G-6 Traceable engineering process|G-6]]"]
verified_by: ["test_master"]
decisions: ["[[ADR-0029 Tests as self-running scripts|ADR-0029]]"]
created: 2026-07-27
updated: 2026-09-27
retrospective: true
---
# REQ-072 — Every feature has an automated test

**Statement.** Each feature has at least one test file; the full suite runs with one command and
must pass before merge. Partial-λ behaviour must be tested against an **independent** calculation,
not only against the code's own finite differences ([[FEAT-045 Independent partial-lambda oracle tests|FEAT-045]]).

