---
title: Scope
type: product
status: active
updated: 2026-09-27
---
# Scope

## In scope

- MSLD energy function on OpenMM `System`s: bonded, LJ, PME electrostatics, 1-4, biases,
  restraints; soft-core; CMAP (later).
- λ-dynamics integration of atoms + θ with Langevin thermostat; constraints; NPT (later).
- Bias flattening (ALF) and production runs.
- Preparation from Amber, CHARMM, PDB+ffxml, SDF+GAFF/OpenFF inputs; amino-acid and ligand
  R-group sites; multiple sites; solvation.
- Analysis: populations → ΔG → ΔΔG, uncertainties, diagnostics.
- Validation against BLaDE (CHARMM) and conventional FEP/TI (Amber).
- A C++/GPU OpenMM plugin for production speed.

## Out of scope (for now)

- Charge-changing perturbations (need charge restraints / co-alchemical ions) — deferred
  ([[FEAT-037 Charge-changing perturbations|FEAT-037]]).
- Ring-editing / core-hopping transformations (MSLD assumes pendant substituents).
- Polarizable force fields, implicit solvent (GB) — the engine refuses them ([[REQ-022 Refuse unsupported input loudly|REQ-022]]).
- Replacing BLaDE; we use it as a reference.
- A GUI.

## Assumptions

- Variants at a site have the same net charge.
- The environment is identical for all variants (only block atoms differ).
- Production force field is Amber (ff14SB/ff19SB + TIP3P/OPC; GAFF/OpenFF for ligands).
  CHARMM36 is used for BLaDE validation.

## Constraints

- Development machine: Apple M4, OpenCL single precision only; no CUDA ([[Dependencies]]).
  Production: a CUDA cluster.
- Two laptops and several agents may work in parallel → git branches, one task per branch.
- Resource etiquette on laptops: limit threads; ask before heavy runs.

