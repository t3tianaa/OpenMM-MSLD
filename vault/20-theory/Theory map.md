---
title: Theory map
type: theory
status: reviewed
updated: 2026-09-27
---
# Theory map

Ground-truth knowledge: what the methods **are**, independent of any code. Architecture notes and
tasks link here instead of re-explaining physics.

```
                      Alchemical free energy basics
                     ┌────────────┴─────────────┐
      Thermodynamic cycles              Lambda dynamics
                                              │
                                  Multisite lambda dynamics ──── Hybrid and multiple topologies
               ┌──────────────┬───────────────┼───────────────────┬──────────────────┐
  Implicit constraints   Theta force by   Alchemical scaling   Biasing potentials   Free energies from
  (softmax of sin θ)     the chain rule   rules in MSLD        in MSLD              lambda populations
                                              │                     │                    │
                          ┌───────────────────┼──────────┐  Adaptive landscape   Free energy
                  Bonded terms and     PME with λ-scaled  Soft-core  flattening        estimators
                  dummy atoms          charges            potentials
                          │                   │
                  Atom restraints      Ewald summation and PME · Reaction-field electrostatics
                  between substituents Lennard-Jones, NBFIX · Cutoffs, switching, dispersion
```

## Alchemy and free energies
- [[Alchemical free energy basics]] — λ paths, FEP, TI, why alchemy works.
- [[Thermodynamic cycles for relative free energies]] — ΔΔG from two legs.
- [[Free energy estimators]] — exponential averaging, TI, BAR/MBAR, WHAM.
- [[Net charge changes in alchemical calculations]]

## λ-dynamics and MSLD
- [[Lambda dynamics]] — λ as a dynamic particle (extended Lagrangian).
- [[Multisite lambda dynamics]] — sites, blocks, the MSLD energy function.
- [[Implicit constraints and the softmax of sin theta]] — θ → λ.
- [[Theta force by the chain rule]] — ∂U/∂θ from ∂U/∂λ.
- [[Alchemical scaling rules in MSLD]] — which λ multiplies which term.
- [[Free energies from lambda populations]] — end-state populations → G, FPL.
- [[Biasing potentials in MSLD]] — fixed, pairwise (types 6/8/10), θ biases.
- [[Adaptive landscape flattening]] — ALF.
- [[Hybrid and multiple topologies]]
- [[Atom restraints between substituents]]
- [[Bonded terms and dummy atoms in alchemy]]
- [[Soft-core potentials]]

## Molecular mechanics
- [[Force field functional forms]] — Amber vs CHARMM terms.
- [[Lennard-Jones, combining rules and NBFIX]]
- [[Cutoffs, switching and dispersion correction]]
- [[Ewald summation and PME]] · [[PME with lambda-scaled charges]] · [[Reaction-field electrostatics]]

## Dynamics and numerics
- [[Langevin dynamics and BAOAB splitting]]
- [[Constraints SHAKE RATTLE SETTLE]]
- [[Pressure control and the Monte Carlo barostat]]
- [[Finite differences and floating-point precision]]

## Preparation
- [[Maximum common substructure mapping]] · [[Kabsch superposition]]

