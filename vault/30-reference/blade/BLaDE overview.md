---
title: BLaDE overview
type: reference
status: verified
system: blade
version: c677277
related: ["[[BLaDE input script language]]", "[[BLaDE MSLD data model]]", "[[Multisite lambda dynamics]]"]
updated: 2026-09-27
---
# BLaDE overview

**BLaDE** — "Basic Lambda Dynamics Engine": a standalone GPU (CUDA) MD engine specialised for
multi-site λ-dynamics, by R. L. Hayes, J. Buckner, C. L. Brooks III (JCTC 17, 6799, 2021). It is
also compiled into CHARMM. It reads **only CHARMM** inputs (PSF + parameter files). It is our
**reference implementation and validation oracle** ([[ADR-0002 BLaDE is the reference and validation oracle|ADR-0002]]).

Pinned: github.com/RyanLeeHayes/BLaDE, commit `c677277` (2026-07-28). A clone was made in the audit
session's scratchpad (temporary); re-clone for new work.

## Source tree (what lives where)

```
 src/main/       blade.cxx (entry), defines.h (units, constants)
 src/io/         script parser, variables, control flow
 src/system/     System, Structure (PSF), Parameters, Coordinates, Selections, State, Potential
 src/msld/       msld.h/.cu — ALL λ-dynamics logic: data model, θ→λ, θ force, biases,
                 θ biases, atom restraints, charge restraints, term-scaling classifiers
 src/bonded/     bonded.cu (bonds, angles, dihedrals, impropers, CMAP, UB); pair.cu (1-4, exclusions)
 src/nbdirect/   direct-space LJ + electrostatics with λ scaling and soft-core
 src/nbrecip/    PME: self, spread (λ-scaled charges), convolution, gather (+ λ forces)
 src/update/     update.cu (VRORV integrator), pressure.cu (MC barostat), minimize, lbfgs, rex
 src/holonomic/  SHAKE/RATTLE, virtual sites
 src/domdec/     domain decomposition / neighbour lists (multi-GPU)
 src/restrain/   non-MSLD restraints
 test/           example systems (HSP90, T4L, T4L_peptide, RNaseH, …) — see [[BLaDE T4L and HSP90 examples]]
 doc/MAIN.txt    user documentation of the script language
```

## One MD step in BLaDE (simplified)

```
 1. forces: bonded, 1-4/exclusions, direct, reciprocal, biases, θ biases, restraints
            → atom forces f = +∂U/∂x  and  lambdaForce[b] = ∂U/∂λ_b
 2. calc_thetaForce_from_lambdaForce: chain rule → thetaForce (stored after the atoms)
 3. VRORV update of atoms AND θ in one array; SHAKE/RATTLE on atoms only
 4. calc_lambda_from_theta: new λ for the next step
 5. every freqnpt steps: Monte Carlo volume move
```
Details: [[BLaDE integrator and update loop]].

## Where to look for each topic
| topic | note |
|---|---|
| script / inputs | [[BLaDE input script language]] |
| data structures | [[BLaDE MSLD data model]] |
| θ ↔ λ | [[BLaDE lambda from theta and theta force]] |
| bonded scaling, removescaling | [[BLaDE bonded term scaling]] |
| direct-space nonbonded, soft-core | [[BLaDE nonbonded direct space]] |
| PME and exclusions | [[BLaDE PME reciprocal space and exclusions]] |
| biases | [[BLaDE biases and theta biases]] |
| restraints | [[BLaDE atom restraints and soft bonds]], [[BLaDE charge restraints]] |
| NPT | [[BLaDE pressure coupling]] |
| units, θ mass | [[BLaDE units and theta mass]] |

