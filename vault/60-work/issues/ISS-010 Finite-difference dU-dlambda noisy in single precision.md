---
id: ISS-010
type: issue
title: Finite-difference dU/dlambda noisy in single precision
status: investigating
kind: design-flaw
severity: medium
confidence: inferred
source: "[[AUD-001 Engine audit of the local working copy|AUD-001]]"
affects: ["[[Force groups and derivative routing]]", "[[Electrostatics scaling module]]", "[[Bias module]]"]
requirements: ["[[REQ-020 Accurate dU-dlambda for every term|REQ-020]]"]
fixed_by: ["[[TASK-041 Analytic bias derivatives|TASK-041]]", "[[TASK-059 Plugin S1 Reference nonbonded force|TASK-059]]"]
found: 2026-09-26
updated: 2026-10-29
---
# ISS-010 — Finite-difference dU/dλ of the whole group 0 is noisy in single precision (audit F10)

Group 0 contains the entire `NonbondedForce` incl. env–env PME (~10⁵–10⁶ kJ/mol for 26 k atoms). With
h = 1e-4 and fp32 round-off ~0.1 kJ/mol, the derivative noise is ~0.1/2e-4 ≈ 500 kJ/mol per
evaluation — a random θ force acting like heat ([[Finite differences and floating-point precision]]).
Reference (double) is exact, but MDM2 ran on Apple OpenCL (fp32 only). Each step also costs
1 + 2·n_blocks PME evaluations.

Cheap improvement: analytic bias derivatives ([[TASK-041 Analytic bias derivatives|TASK-041]]). Real fix: analytic electrostatics
([[FEAT-033 Analytic nonbonded plugin force|FEAT-033]]).

**Update 2026-10-29 (AUD-003).** Measured: roundoff ∝ 1/h, 17.7 kJ/mol rms at 27k atoms on fp32 OpenCL with h = 1e-4. Biases are now analytic and the default h is 1e-2 ([[ADR-0045 Analytic biases and a large FD step|ADR-0045]]): ~0.24 kJ/mol. Remaining: the FD itself (plugin).
