---
id: ADR-0036
type: adr
title: Same-site reciprocal-space convention
status: proposed
date: 2026-09-27
deciders: [Tetiana]
affects: ["[[Electrostatics scaling module]]", "[[BLaDE cross-validation harness]]"]
requirements: ["[[REQ-006 Same-site pairs never interact|REQ-006]]", "[[REQ-007 PME electrostatics at partial lambda|REQ-007]]", "[[REQ-070 Agree with BLaDE on a shared CHARMM system|REQ-070]]"]
retrospective: false
---
# ADR-0036 — Same-site reciprocal-space convention (proposed, open)

## Context
Our same-site exclusions remove the reciprocal cross-talk λ_bλ_c q q erf(βr)/r between competing
substituents; BLaDE's default (`ewaldtype 2`) keeps it; BLaDE `ewaldtype 3` removes it (and also uses
λ² for within-block exclusions, like ours) ([[PME with lambda-scaled charges]], [[BLaDE PME reciprocal space and exclusions]]).
Our docs described this backwards ([[ISS-006 Same-site PME differs from BLaDE and docs are backwards|ISS-006]]).

## Options
1. **Keep OpenMM's behaviour** (cleaner physics: alternatives never interact), and compare with
   BLaDE run with `msld ewaldtype 3`.
2. Match BLaDE's default: add back Σ λ_bλ_c q q erf(βr)/r for same-site pairs with a correction force
   (analytic in a CustomNonbondedForce with an erf kernel, same-site interaction groups).
3. Make it a user option mirroring BLaDE's 1/2/3.

## Proposed decision
Option 3 with default = BLaDE default (2) for validation fidelity, **or** option 1 if the owner prefers
cleaner physics — **needs the owner's choice**. Either way, quantify the energy difference on
MDM2/T4L at λ = 0.5.

