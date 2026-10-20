---
title: OpenMM CustomNonbondedForce
type: reference
status: verified
system: openmm
version: 8.5.2
related: ["[[Lennard-Jones scaling module]]", "[[OpenMM exclusion parity across nonbonded forces]]"]
updated: 2026-09-27
---
# OpenMM `CustomNonbondedForce`

Header: `CustomNonbondedForce.h`. **Verified** by reading.

- Pair energy expression with per-particle parameters (`sigma1`, `sigma2`, …), global parameters,
  tabulated functions (`Discrete2DFunction` for CHARMM `acoef(type1, type2)` tables), computed
  values.
- **Interaction groups** (`addInteractionGroup(set1, set2)`, line ~129): only pairs with one atom
  in set1 and one in set2 are computed. We use one force per λ-scaling category, each with its
  groups ([[ADR-0008 LJ scaled by grouped CustomNonbondedForces|ADR-0008]]). Exclusions still apply inside groups.
- Nonbonded method, cutoff and **potential switching** copied from `NonbondedForce` by our code.
- **Long-range correction** (`setUseLongRangeCorrection`, line 153): off by default; its
  precomputation "must be repeated every time a global parameter changes", so with λ changing every
  step it would be very slow (header lines 155-158). Relevant to [[ADR-0039 Dispersion correction handling|ADR-0039]].
- Supports `addEnergyParameterDerivative`.
- Must carry **the same exclusions** as every other nonbonded force on CPU/OpenCL/CUDA
  ([[OpenMM exclusion parity across nonbonded forces]]).

Scaling problem: the number of forces grows with the number of scaling categories (one per block
and per cross-site pair). For many sites a single force with a per-particle block index and a
`Discrete2DFunction` of λ factors is the alternative ([[TASK-069 Scalable LJ grouping for many sites|TASK-069]]).

