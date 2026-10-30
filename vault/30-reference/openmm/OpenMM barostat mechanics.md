---
title: OpenMM barostat mechanics
type: reference
status: verified
system: openmm
version: 8.5.2
related: ["[[Pressure control and the Monte Carlo barostat]]", "[[BLaDE pressure coupling]]"]
updated: 2026-09-27
---
# OpenMM barostat mechanics

`MonteCarloBarostat(pressure, temperature, frequency=25)` (header line 75) is a `Force` with no
energy; it acts during `Integrator.step()` via the context-state update: every `frequency` steps it
scales **molecule centres**, re-evaluates the energy and accepts/rejects. Variants: anisotropic,
membrane, flexible barostats.

Consequence: any driver that never calls `Integrator.step()` (our Python `LambdaDynamics`) never
triggers the barostat → NVT only ([[ISS-009 NPT impossible with the Python driver|ISS-009]]). Options: call the barostat logic ourselves in
Python (re-implement the MC move), use a `CustomIntegrator` with `addUpdateContextState`, or the
plugin integrator ([[FEAT-032 NPT ensemble|FEAT-032]]).

