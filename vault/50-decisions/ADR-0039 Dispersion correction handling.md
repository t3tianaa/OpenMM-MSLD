---
id: ADR-0039
type: adr
title: Dispersion correction handling
status: proposed
date: 2026-09-27
deciders: [Tetiana]
affects: ["[[Lennard-Jones scaling module]]"]
requirements: ["[[REQ-024 Dispersion correction preserved|REQ-024]]"]
retrospective: false
---
# ADR-0039 — Long-range dispersion correction (proposed, open)

## Context
`add_scaled_lj` turns off `NonbondedForce` dispersion correction for the whole system; an input with
it on no longer satisfies λ = 1 ≡ base, and env–env loses a volume-dependent term (hundreds of
kJ/mol in a solvated box) — matters for NPT ([[ISS-007 Dispersion correction removed for the whole system|ISS-007]]). `CustomNonbondedForce`'s long-range
correction is recomputed whenever a global parameter changes → too slow if λ changes every step
([[OpenMM CustomNonbondedForce]]). BLaDE: to be checked whether it applies a dispersion correction
at all (vfswitch, no LRC is common in CHARMM).

## Options
1. Keep the NonbondedForce correction for env–env only (it is computed from the particles' current
   ε; alchemical ε = 0 there → the env–env-only correction arises naturally if we simply do not turn
   it off — **Inferred**, to verify), no correction for alchemical LJ.
2. Add a λ-weighted analytic correction for blocks (small; composition-dependent).
3. Turn it off everywhere (as now) and require inputs without it.

## Proposed direction
Verify option 1's claim; if true, adopt option 1 (+ document that alchemical LJ tails are
omitted, as BLaDE likely does). Match BLaDE in the cross-check setup.

