---
id: ADR-0045
type: adr
title: Analytic biases and a large FD step
status: accepted
date: 2026-10-29
deciders: [Tetiana]
affects: ["[[Force groups and derivative routing]]", "[[Bias module]]"]
requirements: ["[[REQ-020 Accurate dU-dlambda for every term|REQ-020]]"]
supersedes: []
superseded_by: []
retrospective: false
---
# ADR-0045 — Analytic biases and a large FD step

## Context
The group-0 finite difference is pure roundoff, ∝ 1/h: on Apple OpenCL (fp32 only) 3.4, 6.4 and
17.7 kJ/mol rms at h = 1e-4 for 2.7k, 8.8k and 27k atoms; 0.03–0.24 at h = 1e-2
([[AUD-003 Theta and lambda-dynamics integration review|AUD-003]]). The NonbondedForce energy is exactly
quadratic in each λ, so a central difference has no truncation error at any h. Only the bias types 8
and 10 (rational, exponential) in the same group were not quadratic.

## Decision
The bias force becomes a one-particle `CustomCompoundBondForce` with `addEnergyParameterDerivative`
(analytic group), and the default `fd_step` rises from 1e-4 to 1e-2.

## Consequences
- ~75× less FD noise at no cost; bias gradients exact.
- A caller-injected group-0 force that is not quadratic in λ gets an O(h²) error; pass a smaller
  `fd_step` in that case.
- Closes [[TASK-041 Analytic bias derivatives|TASK-041]]; [[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]] mitigated.
