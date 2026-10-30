---
id: ADR-0038
type: adr
title: Theta units and default theta mass
status: proposed
date: 2026-09-27
deciders: [Tetiana]
affects: ["[[MSLD model component]]", "[[Lambda dynamics integrator component]]"]
requirements: ["[[REQ-017 Per-block theta mass, friction and fixing|REQ-017]]", "[[REQ-016 Canonical sampling of atoms and theta|REQ-016]]"]
retrospective: false
---
# ADR-0038 — θ units and default θ mass/friction equivalent to BLaDE (proposed)

## Context
We copy the numbers (mass 5, friction 1 ps⁻¹) but not the unit convention: BLaDE's effective θ
mass is ≈ 0.01·m (AKMA build) or 100·m (NMPS build) in our units ([[BLaDE units and theta mass]]).
MDM2 runs used mass 10, friction 20.

## Proposed decision
After [[TASK-032 Resolve BLaDE theta units|TASK-032]]: document θ in radians with mass in kJ/mol·ps² (amu·nm²), convert BLaDE input
masses explicitly (a helper `theta_mass_from_blade(m, units="AKMA")`), and set defaults equal to the
effective values of the build the BLaDE authors use in production. Also match the θ friction and the
atom friction (BLaDE examples: 1 ps⁻¹ for θ, 0.1 ps⁻¹ for atoms; ours 1 and 1).

