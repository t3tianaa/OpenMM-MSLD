---
id: ADR-0029
type: adr
title: Tests as self-running scripts
status: accepted
date: 2026-07-31
deciders: [Tetiana]
affects: ["[[Test catalog]]"]
requirements: ["[[REQ-072 Every feature has an automated test|REQ-072]]"]
retrospective: true
---
# ADR-0029 — Tests are self-running scripts, one file per feature

## Decision
`tests/test_<feature>.py`, each with a `__main__` runner; run all with
`for t in tests/test_*.py; do python "$t"; done`. No pytest dependency.

## Consequences
- Zero tooling; each file readable as documentation.
- No collection/reporting, no selective runs, no parallelism control; CI would need a wrapper. A
  pytest-compatible layout (functions named `test_*`) would allow both — open option ([[TASK-066 Consider a pytest-compatible test layout|TASK-066]]).

