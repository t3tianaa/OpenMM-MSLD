---
title: Lennard-Jones scaling module
type: component
subsystem: "[[Simulation subsystem]]"
layer: L3
status: partial
code: [msld/forces.py]
requirements: ["[[REQ-005 Nonbonded pair scaling rules|REQ-005]]", "[[REQ-008 LJ scaling including NBFIX|REQ-008]]", "[[REQ-024 Dispersion correction preserved|REQ-024]]"]
decisions: ["[[ADR-0008 LJ scaled by grouped CustomNonbondedForces|ADR-0008]]", "[[ADR-0039 Dispersion correction handling|ADR-0039]]"]
issues: ["[[ISS-004 CHARMM NBFIX systems fail on CPU|ISS-004]]", "[[ISS-007 Dispersion correction removed for the whole system|ISS-007]]"]
updated: 2026-09-27
---
# Lennard-Jones scaling module

## Amber path — `add_scaled_lj`
- Capture every particle's (σ, ε); set ε = 0 for alchemical atoms in the `NonbondedForce` (charges
  and σ kept); env–env LJ stays there.
- One `CustomNonbondedForce` "MSLDLJ_b" per alchemical block: `lambda_b*4*epsilon*((sigma/r)^12−(sigma/r)^6)`
  with LB combining, interaction groups (env, block b) and (block b, block b).
- One "MSLDLJ_b_c" per pair of blocks at **different** sites: prefactor `lambda_b*lambda_c`,
  group (block b, block c). Same-site pairs are in no group.
- Method, cutoff and potential switching copied from the `NonbondedForce`; exclusions copied
  (1-2, 1-3, 1-4 and same-site); long-range correction off.
- `nbf.setUseDispersionCorrection(False)` — **removes the correction for the whole system**
  ([[ISS-007 Dispersion correction removed for the whole system|ISS-007]]).

## CHARMM path — `add_scaled_charmm_lj`
When NBFIX exists, all LJ lives in one tabulated `CustomNonbondedForce` (see
[[Lennard-Jones, combining rules and NBFIX]]). The module restricts the original to env–env and
creates λ-prefixed copies of its expression + `acoef/bcoef` tables with the same grouping.
**Bug:** copies the original exclusions but not the same-site exclusions → CPU platform rejects the
System ([[ISS-004 CHARMM NBFIX systems fail on CPU|ISS-004]]).

## Why not NonbondedForce offsets for LJ
A product λ_iλ_j on ε cannot be expressed through combining rules (gives √(λ_iλ_j)) → [[ADR-0008 LJ scaled by grouped CustomNonbondedForces|ADR-0008]].

## Scaling concern
Forces grow as (#blocks + #cross-site block pairs). Fine for a few sites; for many sites use one
force with a block-index per particle and a `Discrete2DFunction` of λ factors ([[TASK-069 Scalable LJ grouping for many sites|TASK-069]]).

