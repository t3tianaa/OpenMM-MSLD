---
id: FEAT-006
type: feature
title: Lambda biases
status: done
milestone: M2
implements: ["[[REQ-012 Fixed and variable lambda biases|REQ-012]]"]
components: ["[[Bias module]]"]
decisions: ["[[ADR-0024 Home-grown ALF heuristic|ADR-0024]]"]
tasks: ["[[TASK-007 Add biases, restraints and constraints|TASK-007]]", "[[TASK-041 Analytic bias derivatives|TASK-041]]"]
issues: ["[[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]"]
created: 2026-08-10
updated: 2026-09-27
retrospective: true
---
# FEAT-006 — λ biases

Fixed linear + variable types 6/8/10 as one `CustomExternalForce` with tunable coefficient globals.
Follow-up: analytic derivatives ([[TASK-041 Analytic bias derivatives|TASK-041]]).

