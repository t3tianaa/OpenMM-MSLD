---
id: ADR-0044
type: adr
title: Own SHAKE in the Python driver
status: accepted
date: 2026-10-29
deciders: [Tetiana]
affects: ["[[Lambda dynamics integrator component]]"]
requirements: ["[[REQ-016 Canonical sampling of atoms and theta|REQ-016]]"]
supersedes: []
superseded_by: []
retrospective: false
---
# ADR-0044 — Own SHAKE in the Python driver

## Context
`LambdaDynamics._drift_x` used `Context.applyConstraints`, which projects the predicted positions
using themselves as the reference. That is not SHAKE: not time-reversible, and it drains kinetic
energy each drift. Rigid water ran at 267–271 K for a 300 K bath at γ = 1 ps⁻¹ on Reference, CPU and
OpenCL, ~291 K at γ = 5 ([[ISS-026 Constrained atoms run below the bath temperature|ISS-026]]).

## Decision
A vectorized SHAKE in numpy with the pre-drift positions as the reference directions, constraints
split into colors (no atom twice per color) and swept Gauss–Seidel. Velocities keep OpenMM's
`applyVelocityConstraints` (RATTLE). Initial velocities are projected at construction.

## Consequences
- Rigid water returns to 300.7 ± 1.2 K at γ = 1 ps⁻¹, dt = 1 fs; 299.8 K at γ = 5, dt = 2 fs
  ([[Test catalog]]: test_shake).
- CPU cost scales with the number of constraints; small next to the FD energy evaluations.
- Goes away with a real Integrator (plugin S3 / [[FEAT-034 Fused MSLD integrator plugin|FEAT-034]]).
