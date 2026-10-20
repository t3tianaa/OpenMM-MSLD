---
id: ADR-0012
type: adr
title: Python driver integrator instead of CustomIntegrator
status: accepted
date: 2026-08-10
deciders: [Tetiana]
affects: ["[[Lambda dynamics integrator component]]"]
requirements: ["[[REQ-016 Canonical sampling of atoms and theta|REQ-016]]", "[[REQ-019 NPT ensemble|REQ-019]]"]
retrospective: true
---
# ADR-0012 — A Python driver integrator instead of a `CustomIntegrator`

## Context
The old plan was a `CustomIntegrator` reading `deriv(energy, lambda_b)`. But the electrostatic
dU/dλ is not available through `deriv()` ([[OpenMM CustomIntegrator]]).

## Options
1. CustomIntegrator + no electrostatic λ-force (wrong physics). 2. **Python loop: OpenMM computes
forces/energies; Python does θ, chain rule, VRORV for atoms and θ, and FD for the missing
derivative.** 3. Plugin integrator (later).

## Decision
Option 2 (`LambdaDynamics`).

## Consequences
- Correct physics, any platform, easy to debug.
- Very slow (Python per step, host↔device copies); **NPT impossible** because `Integrator.step()`
  never runs ([[ISS-009 NPT impossible with the Python driver|ISS-009]]); RNG and state live in Python (no OpenMM checkpoints).
- Revisit when all λ-derivatives are analytic: a CustomIntegrator or the plugin integrator
  ([[FEAT-034 Fused MSLD integrator plugin|FEAT-034]]).

