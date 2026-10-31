---
id: FEAT-045
type: feature
title: Independent partial-lambda oracle tests
status: done
milestone: M4
implements: ["[[REQ-072 Every feature has an automated test|REQ-072]]", "[[REQ-070 Agree with BLaDE on a shared CHARMM system|REQ-070]]"]
components: ["[[Partial-lambda oracle tests]]"]
tasks: ["[[TASK-067 NumPy partial-lambda oracle tests|TASK-067]]"]
issues: ["[[ISS-012 No validation at partial lambda|ISS-012]]"]
created: 2026-09-27
updated: 2026-10-31
---
# FEAT-045 — Independent partial-λ oracle tests

NumPy re-implementation of the MSLD energy function for small NoCutoff systems; compare energies
and every dU/dλ at random λ.


**Done 2026-10-31** ([[TASK-067 NumPy partial-lambda oracle tests|TASK-067]]). NoCutoff only; PME reciprocal space is not covered.
