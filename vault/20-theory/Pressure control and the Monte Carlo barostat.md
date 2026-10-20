---
title: Pressure control and the Monte Carlo barostat
type: theory
status: reviewed
related: ["[[BLaDE pressure coupling]]", "[[OpenMM barostat mechanics]]"]
updated: 2026-09-27
---
# Pressure control and the Monte Carlo barostat

A Monte Carlo barostat samples volume: every n steps, propose V → V' (scaling molecular centres or
atoms), compute the new potential energy, accept with probability

```
 min(1, exp(−ΔW/kT)),   ΔW = ΔU + P·ΔV − N kT ln(V'/V)
```

(N = number of molecules if centres are scaled.) It needs only energies — no virial — and works
with any potential, including λ-dependent ones: θ is not changed by the move; U includes biases.
BLaDE uses exactly this (`pressure.cu:114-180`, with N = atoms minus constraints); OpenMM's
`MonteCarloBarostat` does it inside `Integrator.step()` ([[OpenMM barostat mechanics]]).

Why it matters: MSLD production runs are NPT; our Python driver never calls `Integrator.step()`,
so an OpenMM barostat never fires ([[ISS-009 NPT impossible with the Python driver|ISS-009]]).

