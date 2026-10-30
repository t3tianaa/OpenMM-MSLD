---
id: ADR-0007
type: adr
title: Charges scaled by NonbondedForce offsets
status: accepted
date: 2026-08-05
deciders: [Tetiana]
affects: ["[[Electrostatics scaling module]]", "[[1-4 exception scaling module]]"]
requirements: ["[[REQ-007 PME electrostatics at partial lambda|REQ-007]]", "[[REQ-009 1-4 pair scaling|REQ-009]]", "[[REQ-020 Accurate dU-dlambda for every term|REQ-020]]"]
retrospective: true
---
# ADR-0007 — Scale charges with `NonbondedForce` parameter offsets

## Context
Electrostatics must stay on OpenMM's native PME; BLaDE scales charges before spreading on the grid
([[BLaDE PME reciprocal space and exclusions]]).

## Options
1. Reimplement PME in custom forces — not possible with stock OpenMM.
2. **Particle and exception parameter offsets**: charge = 0 + λ_b·q_i (linear in λ) — PME, self and
   exclusion terms follow automatically.
3. A plugin with λ-aware PME (later, [[ADR-0026 Tier 2 plugin with scope S0 to S4|ADR-0026]]).

## Decision
Option 2 for Tier 1.

## Consequences
- Native, fast PME; λ = 1 exact.
- Within-block pairs get λ² in direct space → needs a correction ([[ADR-0009 Within-block real-space electrostatics linear|ADR-0009]]).
- **No analytic dU/dλ** from `NonbondedForce` → finite differences ([[ADR-0013 Tier 0 analytic dU-dlambda via force groups|ADR-0013]], [[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]).
- Same-site handling follows from exclusions ([[ADR-0010 Same-site pairs excluded in every nonbonded force|ADR-0010]]).

