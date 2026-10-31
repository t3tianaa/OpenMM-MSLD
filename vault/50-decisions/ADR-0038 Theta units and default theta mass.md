---
id: ADR-0038
type: adr
title: Theta units and default theta mass
status: accepted
date: 2026-09-27
deciders: [Tetiana]
affects: ["[[MSLD model component]]", "[[Lambda dynamics integrator component]]"]
requirements: ["[[REQ-017 Per-block theta mass, friction and fixing|REQ-017]]", "[[REQ-016 Canonical sampling of atoms and theta|REQ-016]]"]
retrospective: false
---
# ADR-0038 — θ units and default θ mass/friction equivalent to BLaDE (accepted 2026-10-31)

## Context
We copy the numbers (mass 5, friction 1 ps⁻¹) but not the unit convention: BLaDE's effective θ
mass is ≈ 0.01·m (AKMA build) or 100·m (NMPS build) in our units ([[BLaDE units and theta mass]]).
MDM2 runs used mass 10, friction 20.

## Proposed decision
After [[TASK-032 Resolve BLaDE theta units|TASK-032]]: document θ in radians with mass in kJ/mol·ps² (amu·nm²), convert BLaDE input
masses explicitly (a helper `theta_mass_from_blade(m, units="AKMA")`), and set defaults equal to the
effective values of the build the BLaDE authors use in production. Also match the θ friction and the
atom friction (BLaDE examples: 1 ps⁻¹ for θ, 0.1 ps⁻¹ for atoms; ours 1 and 1).


## Decision (2026-10-31)
θ is in radians, energies in kJ/mol, so the θ mass carries amu·nm². BLaDE's production build is
AKMA (CHARMM and ALF use it), where its θ mass is in amu·Å²: BLaDE's 5 = **0.05 amu·nm²** here.
Defaults are now `Block.theta_mass = 0.05`, `Block.theta_friction = 1.0 ps⁻¹`;
`msld.model.theta_mass_from_blade(m, units="AKMA"|"NMPS")` converts explicitly.

## Evidence
[[EXP-011 MDM2 theta mass and friction screen|EXP-011]]: on MDM2 (with the within-block soft-core, ADR-0043) 0.05 / 1 is
stable, keeps T_θ near 300 K and gives the most variant switching (58 leader changes vs 0 for the
old 10 / 20, whose diffusion D = kT/(mγ) ≈ 0.0125 rad²/ps is far too slow). The atom friction (BLaDE
0.1 ps⁻¹ vs our 1) and dt 2 fs were not tested; deferred to the plugin stage.
