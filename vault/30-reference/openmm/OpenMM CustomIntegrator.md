---
title: OpenMM CustomIntegrator
type: reference
status: verified
system: openmm
version: 8.5.2
related: ["[[Lambda dynamics integrator component]]", "[[ADR-0012 Python driver integrator instead of CustomIntegrator|ADR-0012]]"]
updated: 2026-09-27
---
# OpenMM `CustomIntegrator`

A programmable integrator: a list of computation steps with global and per-DOF variables
(`addGlobalVariable`, `addPerDofVariable`, `addComputeGlobal`, `addComputePerDof`,
`addConstrainPositions`, `addConstrainVelocities`, `addUpdateContextState`, conditionals, loops).

- `deriv(energy, lambda)` gives the derivative of the energy with respect to a global parameter,
  for parameters registered with `addEnergyParameterDerivative` (header lines 335-339, **Verified**).
- `energy0`, `energy1` … restrict to a force group.
- Runs entirely on the platform (GPU) → fast; `addUpdateContextState` lets barostats fire.

Why we did not use it (yet): the electrostatic dU/dλ is not available through `deriv()` (no
derivative in `NonbondedForce`), so the θ-force cannot be computed inside the integrator
([[ADR-0012 Python driver integrator instead of CustomIntegrator|ADR-0012]]). Once every term exposes analytic derivatives, a `CustomIntegrator` (or a plugin
integrator) becomes possible and gives NPT for free.

