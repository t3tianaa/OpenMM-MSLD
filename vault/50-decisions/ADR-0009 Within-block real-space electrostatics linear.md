---
id: ADR-0009
type: adr
title: Within-block real-space electrostatics linear
status: accepted
date: 2026-08-17
deciders: [Tetiana]
affects: ["[[Electrostatics scaling module]]"]
requirements: ["[[REQ-005 Nonbonded pair scaling rules|REQ-005]]", "[[REQ-007 PME electrostatics at partial lambda|REQ-007]]"]
retrospective: true
---
# ADR-0009 — Within-block real-space electrostatics is linear in λ; reciprocal stays λ²

## Context
Charge offsets make a within-block pair scale as λ². BLaDE's direct-space kernel uses λ_b (linear)
for same-block pairs, while its reciprocal space (scaled charges) gives λ² ([[BLaDE nonbonded direct space]]).

## Decision
Add, per block, a correction `CustomNonbondedForce` `(λ_b − λ_b²)·k q_i q_j S(r)` over non-excluded
within-block pairs, S = the direct-space Coulomb kernel. Reciprocal stays λ² as in BLaDE.

## Consequences
- Matches BLaDE's direct/reciprocal split; zero at λ = 1 (master invariant kept); analytic dU/dλ.
- "Within-block is linear" is only true in real space; under PME most of a close pair's energy is
  reciprocal (λ²) (audit F6).
- S must equal the force's actual kernel — wrong for reaction-field methods ([[ISS-003 Within-block correction wrong for cutoff methods|ISS-003]]) and α
  must be the force's real α ([[ISS-008 PME alpha recomputed from the tolerance|ISS-008]]).

