---
title: OpenMM NonbondedForce
type: reference
status: verified
system: openmm
version: 8.5.2
related: ["[[Ewald summation and PME]]", "[[Reaction-field electrostatics]]", "[[Electrostatics scaling module]]"]
updated: 2026-09-27
---
# OpenMM `NonbondedForce`

Header: `include/openmm/NonbondedForce.h` (OpenMM 8.5.2). **Verified** by reading.

## Per-particle and per-pair data
- `addParticle(charge, sigma, epsilon)`; LJ uses Lorentz–Berthelot.
- **Exceptions** (`addException(i, j, chargeProd, sigma, epsilon)`) replace the interaction of a
  pair: chargeProd = ε = 0 → an *exclusion* (1-2, 1-3); non-zero → a scaled 1-4.
  `createExceptionsFromBonds(bonds, coulomb14Scale, lj14Scale)` builds them.

## Nonbonded methods
| method | electrostatics | notes |
|---|---|---|
| NoCutoff | plain Coulomb | non-periodic |
| CutoffNonPeriodic | **reaction field** | `k_rf`, `c_rf` from `reactionFieldDielectric` (header lines ~110-125) |
| CutoffPeriodic | **reaction field** | periodic |
| Ewald / PME / LJPME | Ewald split | `setEwaldErrorTolerance`, `setPMEParameters(α, nx, ny, nz)`, `getPMEParametersInContext` (line 293) |

Exclusions and exceptions remove the pair from direct space **and** subtract its reciprocal-space
contribution (exclusion correction) for Ewald/PME.

## Parameter offsets (lines 82-106, 451, 486)
```
 charge  = baseCharge  + param · chargeScale
 sigma   = baseSigma   + param · sigmaScale
 epsilon = baseEpsilon + param · epsilonScale
```
`addGlobalParameter(name, default)`, then `addParticleParameterOffset(name, i, cS, sS, eS)` /
`addExceptionParameterOffset(name, k, qqS, sS, eS)`. The whole PME machinery works with the
effective charges. This is how we scale charges by λ ([[ADR-0007 Charges scaled by NonbondedForce offsets|ADR-0007]]).

## What it does NOT have
- **No `addEnergyParameterDerivative`.** Only `Custom*Force`s (and `ATMForce`, `CustomCVForce`,
  `CustomIntegrator`) expose ∂E/∂(global parameter) (`grep addEnergyParameterDerivative *.h`).
  → electrostatic dU/dλ needs finite differences or a plugin ([[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]], [[FEAT-033 Analytic nonbonded plugin force|FEAT-033]]).
- No per-pair λ product for LJ (ε offsets combine through √(ε_i ε_j)).

## Other switches
- `setUseDispersionCorrection(bool)` — long-range LJ correction; on by default. Applies to the whole
  force (cannot be restricted to env–env) ([[ISS-007 Dispersion correction removed for the whole system|ISS-007]]).
- `setUseSwitchingFunction`, `setSwitchingDistance` — *potential* switching (not CHARMM force
  switching).

