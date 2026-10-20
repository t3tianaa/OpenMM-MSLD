---
title: Electrostatics scaling module
type: component
subsystem: "[[Simulation subsystem]]"
layer: L3
status: partial
code: [msld/forces.py]
requirements: ["[[REQ-005 Nonbonded pair scaling rules|REQ-005]]", "[[REQ-006 Same-site pairs never interact|REQ-006]]", "[[REQ-007 PME electrostatics at partial lambda|REQ-007]]", "[[REQ-025 Supported nonbonded methods are correct|REQ-025]]"]
decisions: ["[[ADR-0007 Charges scaled by NonbondedForce offsets|ADR-0007]]", "[[ADR-0009 Within-block real-space electrostatics linear|ADR-0009]]", "[[ADR-0010 Same-site pairs excluded in every nonbonded force|ADR-0010]]", "[[ADR-0036 Same-site reciprocal-space convention|ADR-0036]]", "[[ADR-0040 Supported nonbonded methods|ADR-0040]]"]
issues: ["[[ISS-003 Within-block correction wrong for cutoff methods|ISS-003]]", "[[ISS-006 Same-site PME differs from BLaDE and docs are backwards|ISS-006]]", "[[ISS-008 PME alpha recomputed from the tolerance|ISS-008]]", "[[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]"]
updated: 2026-09-27
---
# Electrostatics scaling module

## Design
1. **Charge offsets** (`add_scaled_electrostatics`): for every alchemical atom i in block b, set the
   base charge to 0 and add `addParticleParameterOffset("lambda_b", i, q_i, 0, 0)` → effective
   charge λ_b q_i. OpenMM then computes direct space, PME reciprocal, self and exclusion terms with
   the scaled charges — native PME kept ([[ADR-0007 Charges scaled by NonbondedForce offsets|ADR-0007]]).
2. **Same-site exclusions** (`add_same_site_exclusions`): every pair of atoms in different blocks
   of one site becomes a full exclusion → no direct interaction, and OpenMM's exclusion correction
   also removes their reciprocal interaction ([[ADR-0010 Same-site pairs excluded in every nonbonded force|ADR-0010]]; differs from BLaDE default, [[ADR-0036 Same-site reciprocal-space convention|ADR-0036]]).
3. **Within-block correction** (`add_within_block_elec_correction`, runs first): charge offsets
   give λ_b² to within-block pairs; BLaDE's direct space uses λ_b. One `CustomNonbondedForce` per
   block with ≥ 1 non-excluded internal pair adds `(λ_b − λ_b²)·k q_i q_j·S(r)` over
   `addInteractionGroup(block, block)`, where S(r) is the direct-space kernel ([[ADR-0009 Within-block real-space electrostatics linear|ADR-0009]]).

```
 pair type          charge offsets give   + correction      = total (direct)   reciprocal
 env–block b        λ_b                   —                 λ_b                λ_b
 within block b     λ_b²                  λ_b − λ_b²        λ_b                λ_b²   (BLaDE: same)
 cross-site b–c     λ_b λ_c               —                 λ_b λ_c            λ_b λ_c
 same site b≠c      excluded              —                 0                  0      (BLaDE default: λ_bλ_c)
```

## ∂U/∂λ
Charge offsets expose no derivative → the NonbondedForce stays in group 0 and is
finite-differenced; the correction forces are analytic ([[Force groups and derivative routing]]).

## As-built problems
- S(r) = `1/r` for CutoffNonPeriodic and `erfc(αr)/r` for CutoffPeriodic — both wrong, OpenMM uses
  reaction field there ([[ISS-003 Within-block correction wrong for cutoff methods|ISS-003]], [[EXP-003 Within-block linearity per nonbonded method|EXP-003]]); decision on supported methods [[ADR-0040 Supported nonbonded methods|ADR-0040]].
- α computed from `ewaldErrorTolerance`, ignoring `setPMEParameters` ([[ISS-008 PME alpha recomputed from the tolerance|ISS-008]]).
- FD of the whole group-0 energy (incl. env–env PME) → noisy on fp32 ([[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]).
Theory: [[PME with lambda-scaled charges]], [[Reaction-field electrostatics]].

