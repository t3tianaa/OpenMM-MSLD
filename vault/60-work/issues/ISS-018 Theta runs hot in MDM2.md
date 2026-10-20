---
id: ISS-018
type: issue
title: Theta runs hot in MDM2
status: investigating
kind: bug
severity: high
confidence: confirmed
source: "[[EXP-006 MDM2 theta-parameter sweep|EXP-006]]"
affects: ["[[Lambda dynamics integrator component]]"]
requirements: ["[[REQ-016 Canonical sampling of atoms and theta|REQ-016]]"]
fixed_by: ["[[TASK-032 Resolve BLaDE theta units|TASK-032]]", "[[TASK-033 Rerun MDM2 with reference theta parameters|TASK-033]]"]
found: 2026-09-16
updated: 2026-09-27
---
# ISS-018 — θ runs hot (1 400–8 000 K) in MDM2 runs

θ kinetic temperature ≈ 8 000 K at friction 2, 2 400 K at 10, 1 400 K at 20 ps⁻¹, independent of
mass (5–40), FD step and dt in the tested ranges; it looks cold only after λ collapses to an end
state (cos θ → 0) ([[EXP-006 MDM2 theta-parameter sweep|EXP-006]]). Earlier conclusion: "needs the analytic plugin". The audit shows the
integrator itself thermostats θ exactly on a toy ([[EXP-001 Theta samples the exact Boltzmann distribution on a toy|EXP-001]]), so the cause is parameters/stiffness
([[ISS-002 Theta mass convention differs from BLaDE|ISS-002]]) and/or FD noise ([[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]), not the integrator code.

