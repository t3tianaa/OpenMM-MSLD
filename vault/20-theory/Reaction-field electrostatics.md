---
title: Reaction-field electrostatics
type: theory
status: reviewed
related: ["[[Ewald summation and PME]]", "[[OpenMM NonbondedForce]]"]
updated: 2026-09-27
---
# Reaction-field electrostatics

**In one sentence.** A cutoff Coulomb in which the medium beyond r_c is a dielectric continuum;
OpenMM uses it for `CutoffNonPeriodic` and `CutoffPeriodic`.

```
 E_ij = k q_i q_j ( 1/r + k_rf r² − c_rf )          (r < r_c; 0 beyond)
 k_rf = (ε_solv − 1) / ((2 ε_solv + 1) r_c³)
 c_rf = 1/r_c + k_rf r_c²
```

(OpenMM `NonbondedForce` documentation; ε_solv = `reactionFieldDielectric`, default 78.3.)

Why it matters: any correction force that re-computes "the Coulomb energy of a pair" must use the
**same** functional form as the force it corrects. Our within-block correction used plain 1/r and
erfc(αr)/r instead → wrong by up to 49 kJ/mol at λ = 0.5 ([[EXP-003 Within-block linearity per nonbonded method|EXP-003]], [[ISS-003 Within-block correction wrong for cutoff methods|ISS-003]]).

