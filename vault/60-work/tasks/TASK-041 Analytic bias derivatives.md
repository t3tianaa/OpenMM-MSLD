---
id: TASK-041
type: task
title: Analytic bias derivatives
status: todo
kind: impl
priority: P2
milestone: M4
feature: "[[FEAT-006 Lambda biases|FEAT-006]]"
issues: ["[[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]"]
refs: ["[[Bias module]]", "[[OpenMM custom forces and parameter derivatives]]"]
created: 2026-09-27
updated: 2026-09-27
---
# TASK-041 — Analytic bias derivatives

Either compute bias dU/dλ in Python from closed forms (as BLaDE does) and add it to the analytic
part, or host the biases on a force class with `addEnergyParameterDerivative` (e.g. `CustomCVForce`),
moving them to group 1. Test vs FD.

