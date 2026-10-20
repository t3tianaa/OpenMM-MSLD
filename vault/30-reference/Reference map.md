---
title: Reference map
type: reference
status: verified
updated: 2026-09-27
---
# Reference map — how the existing codes work

Ground truth taken from **source code and official documentation** of the third-party software we
build on or compare against. Each note pins a version or commit and cites file:line, so tasks and
architecture notes can link here instead of re-reading the code.

| system | role for us | version pinned | notes |
|---|---|---|---|
| **OpenMM** | the engine we extend | 8.5.2 (conda env `msld`, headers `$CONDA_PREFIX/include/openmm`) | `30-reference/openmm` |
| **BLaDE** | reference MSLD implementation and validation oracle | commit `c677277` (2026-07-28), github.com/RyanLeeHayes/BLaDE | `30-reference/blade` |
| **ParmEd** | prep: common structure, readers, round trips | 4.3.1 | `30-reference/parmed` |
| **ALF** (Python package) | the bias-flattening algorithm we must reproduce | not yet studied | [[ALF package overview]] |
| **CHARMM BLOCK** | original MSLD implementation, BLaDE's parent | not studied | [[CHARMM BLOCK and MSLD]] |
| RDKit, openmmforcefields | ligand mapping and parametrization | RDKit 2025.09.6 | `30-reference/other` |

## OpenMM
- [[OpenMM object model]] — System, Force, Context, State, Integrator, Platform.
- [[OpenMM NonbondedForce]] — methods, exceptions, parameter offsets, PME, dispersion.
- [[OpenMM custom forces and parameter derivatives]] — expressions, globals, `addEnergyParameterDerivative`.
- [[OpenMM CustomNonbondedForce]] — interaction groups, tables, long-range correction.
- [[OpenMM force groups and State queries]]
- [[OpenMM exclusion parity across nonbonded forces]]
- [[OpenMM platforms and precision]]
- [[OpenMM CustomIntegrator]]
- [[OpenMM barostat mechanics]]
- [[OpenMM app layer ForceField and Modeller]]
- [[OpenMM plugin architecture]]

## BLaDE
- [[BLaDE overview]] · [[BLaDE input script language]] · [[BLaDE MSLD data model]]
- [[BLaDE lambda from theta and theta force]] · [[BLaDE integrator and update loop]]
- [[BLaDE bonded term scaling]] · [[BLaDE nonbonded direct space]] · [[BLaDE PME reciprocal space and exclusions]]
- [[BLaDE biases and theta biases]] · [[BLaDE atom restraints and soft bonds]] · [[BLaDE charge restraints]]
- [[BLaDE pressure coupling]] · [[BLaDE units and theta mass]] · [[BLaDE T4L and HSP90 examples]]

## ParmEd
- [[ParmEd Structure model]] · [[ParmEd readers for Amber and CHARMM]]
- [[ParmEd round trips and NBFIX loss]] · [[ParmEd createSystem mapping to OpenMM forces]]

## Others
- [[ALF package overview]] · [[CHARMM BLOCK and MSLD]] · [[RDKit MCS]] · [[openmmforcefields template generators]]

**Keeping these notes true.** When a pinned version changes (OpenMM upgrade, new BLaDE commit),
re-check every file:line cited and update `version:`. Mark claims: **Verified** (checked in source
or by running), **Doc** (from official docs), **Inferred**.

