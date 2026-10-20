---
title: Glossary
type: meta
status: active
updated: 2026-09-27
---
# Glossary

| term | meaning | more |
|---|---|---|
| **MSLD / MSλD** | multi-site λ-dynamics: many chemical variants at several sites share one simulation; continuous λ variables decide which variant is present | [[Multisite lambda dynamics]] |
| **λ (lambda)** | coupling variable of one block, in [0,1]; per site the λ's sum to 1 | [[Lambda dynamics]] |
| **θ (theta)** | the unconstrained variable we integrate; λ is a softmax of sin θ | [[Implicit constraints and the softmax of sin theta]] |
| **fnex** | sharpness of the softmax (usually 5.5) | same |
| **site** | a place where variants compete; site 0 = environment | [[Multisite lambda dynamics]] |
| **block** | one variant's atoms + one θ; block 0 = environment | same |
| **substituent / variant** | one alternative at a site (a side chain, an R-group) | same |
| **environment (env)** | atoms shared by all variants, never scaled (λ ≡ 1) | same |
| **same-site pair** | two atoms in different blocks of the same site: never interact | [[Alchemical scaling rules in MSLD]] |
| **within-block pair** | two atoms in the same block | same |
| **dU/dλ** | derivative of the energy by one block's λ; the "λ force" | [[Theta force by the chain rule]] |
| **ALF** | Adaptive Landscape Flattening: iterative fitting of λ biases so all end states are sampled | [[Adaptive landscape flattening]] |
| **biases (types 6/8/10)** | pairwise λ bias shapes used by ALF: quadratic, end-point, skew | [[Biasing potentials in MSLD]] |
| **θ biases** | biases on θ (collective / independent) that raise the fraction of physical states | same |
| **FPL** | fraction of physical ligands: fraction of frames where every site has one λ > cutoff | [[Free energies from lambda populations]] |
| **soft-core** | a change of the distance at small λ so overlapping atoms do not blow up | [[Soft-core potentials]] |
| **PME** | particle-mesh Ewald: fast long-range electrostatics in reciprocal space | [[Ewald summation and PME]] |
| **exclusion correction** | term removing the reciprocal-space interaction of excluded pairs | same |
| **NBFIX** | CHARMM override of LJ for specific atom-type pairs | [[Lennard-Jones, combining rules and NBFIX]] |
| **CMAP** | CHARMM 2-D backbone φ/ψ correction map | [[Force field functional forms]] |
| **1-4 pair** | atoms three bonds apart; interact with scaled parameters | same |
| **CATS / atom restraints** | harmonic restraints holding equivalent atoms of different substituents together | [[Atom restraints between substituents]] |
| **removescaling** | BLaDE option: do not λ-scale some bonded term types | [[Bonded terms and dummy atoms in alchemy]] |
| **master invariant** | at λ = 1 everywhere our scaled System reproduces the base System exactly | [[Invariants]] |
| **Tier 0 / Tier 2** | our names: analytic dU/dλ in Python (Tier 0); C++/GPU plugin (Tier 2) | [[ADR-0013 Tier 0 analytic dU-dlambda via force groups\|ADR-0013]], [[ADR-0026 Tier 2 plugin with scope S0 to S4\|ADR-0026]] |
| **Mode A / Mode B** | ingest routes: apply a force field to a structure (A) or read a parametrized topology (B) | [[Ingest component]] |
| **CoreMapping** | our data object describing one site: env atoms vs blocks | [[CoreMapping and HybridBlueprint]] |
| **HybridSystemBundle** | output of prep: structure + plain System + mapping | [[HybridSystemBundle]] |
| **VRORV / BAOAB** | Langevin splitting: half-kick, half-drift, thermostat, half-drift, half-kick | [[Langevin dynamics and BAOAB splitting]] |
| **AKMA / NMPS** | BLaDE unit builds: CHARMM units (kcal/mol, Å, AKMA time) vs GROMACS units (kJ/mol, nm, ps) | [[BLaDE units and theta mass]] |
| **ΔG, ΔΔG** | free-energy difference; difference of two ΔG legs (bound − unbound) | [[Alchemical free energy basics]] |

