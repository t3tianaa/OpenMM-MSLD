---
title: OpenMM exclusion parity across nonbonded forces
type: reference
status: verified
system: openmm
version: 8.5.2
related: ["[[OpenMM CustomNonbondedForce]]", "[[OpenMM NonbondedForce]]"]
updated: 2026-09-27
---
# OpenMM exclusion parity across nonbonded forces

**Rule (Verified, 2026-09-15 and 2026-09-26):** on the CPU, OpenCL and CUDA platforms, every
nonbonded force in a System (`NonbondedForce` and every `CustomNonbondedForce`) must have
**identical exclusion lists**, otherwise Context creation fails with
`OpenMMException: All Forces must have identical exclusions`. The Reference platform tolerates
mismatches, and so does OpenCL in some code paths but `LocalEnergyMinimizer` on OpenCL then fails.

Consequences for us:
- every scaled LJ force and every within-block correction force carries the same-site exclusions
  (zero-energy for them) — [[ADR-0010 Same-site pairs excluded in every nonbonded force|ADR-0010]];
- the CHARMM LJ copies still miss them → CPU failure ([[ISS-004 CHARMM NBFIX systems fail on CPU|ISS-004]]);
- a test must check exclusion parity for every force the builder creates
  (`test_minimize::test_scaled_forces_share_one_exclusion_set`).

