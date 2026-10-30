---
title: Force scaling component
type: component
subsystem: "[[Simulation subsystem]]"
layer: L2
status: partial
code: [msld/builder.py, msld/forces.py]
requirements: ["[[REQ-003 Scale bonded terms by block lambdas|REQ-003]]", "[[REQ-005 Nonbonded pair scaling rules|REQ-005]]", "[[REQ-006 Same-site pairs never interact|REQ-006]]", "[[REQ-007 PME electrostatics at partial lambda|REQ-007]]", "[[REQ-008 LJ scaling including NBFIX|REQ-008]]", "[[REQ-009 1-4 pair scaling|REQ-009]]", "[[REQ-012 Fixed and variable lambda biases|REQ-012]]", "[[REQ-014 Atom restraints between substituents|REQ-014]]", "[[REQ-020 Accurate dU-dlambda for every term|REQ-020]]", "[[REQ-022 Refuse unsupported input loudly|REQ-022]]", "[[REQ-023 Lambda one reproduces the base system|REQ-023]]"]
decisions: ["[[ADR-0006 Bonded scaling via grouped custom forces|ADR-0006]]", "[[ADR-0007 Charges scaled by NonbondedForce offsets|ADR-0007]]", "[[ADR-0008 LJ scaled by grouped CustomNonbondedForces|ADR-0008]]", "[[ADR-0009 Within-block real-space electrostatics linear|ADR-0009]]", "[[ADR-0010 Same-site pairs excluded in every nonbonded force|ADR-0010]]", "[[ADR-0011 Master invariant as the primary gate|ADR-0011]]", "[[ADR-0013 Tier 0 analytic dU-dlambda via force groups|ADR-0013]]", "[[ADR-0028 Refuse what cannot be scaled|ADR-0028]]"]
issues: ["[[ISS-003 Within-block correction wrong for cutoff methods|ISS-003]]", "[[ISS-004 CHARMM NBFIX systems fail on CPU|ISS-004]]", "[[ISS-005 Unsupported force types silently unscaled|ISS-005]]", "[[ISS-006 Same-site PME differs from BLaDE and docs are backwards|ISS-006]]", "[[ISS-007 Dispersion correction removed for the whole system|ISS-007]]", "[[ISS-008 PME alpha recomputed from the tolerance|ISS-008]]", "[[ISS-015 Cross-site 1-4 and CMAP are refused|ISS-015]]"]
updated: 2026-09-27
---
# Force scaling component — `builder.py` + `forces.py`

## Purpose
Rewrite an OpenMM System in place so its energy equals the MSLD energy function
([[Multisite lambda dynamics]]) as a function of Context globals `lambda{b}`, while λ = 1 for every
block reproduces the base System exactly (master invariant, [[Invariants]]).

## The core trick
OpenMM's built-in forces have fixed formulas; custom forces take formulas. For every term a λ
should scale: take it **out** of the built-in force (zero its constant, keep the term so indices
stay valid) and put it **into** a custom force whose expression carries the λ prefactor.

## Orchestration — `scale_msld_system(system, model)` (order matters)

```
 1. add_scaled_bonds / angles / torsions / impropers     (if model.scale_*)    [[Bonded scaling module]]
 2. add_within_block_elec_correction   BEFORE step 3 (needs raw charges)      [[Electrostatics scaling module]]
 3. add_scaled_electrostatics          charge offsets + same-site exclusions
 4. add_scaled_lj                      Amber LJ → grouped CustomNonbondedForces [[Lennard-Jones scaling module]]
 5. add_scaled_charmm_lj               CHARMM tabulated LJ (no-op on Amber)
 6. add_scaled_14_exceptions           exception offsets                        [[1-4 exception scaling module]]
 7. add_biases                         one CustomExternalForce                  [[Bias module]]
 8. add_atom_restraints                CustomBondForce                          [[Atom restraint module]]
 9. _split_force_groups                analytic → group 1, rest → group 0       [[Force groups and derivative routing]]
10. _check_unhandled                   raises on alchemical CMAP (only)         [[ADR-0028 Refuse what cannot be scaled|ADR-0028]]
```
Returns an info dict of created forces. `set_lambdas(context, λ)` and `set_biases(context, model)`
push run-time values.

## Resulting force layout (Amber, one site with blocks 1, 2)

```
 group 0 (FD):       HarmonicBond/Angle/PeriodicTorsion (env terms + zeroed alchemical terms)
                     NonbondedForce  (charges: λ offsets; alchemical ε = 0; exclusions incl. same-site;
                                      dispersion correction OFF)
                     MSLDBias (CustomExternalForce)      MSLDAtomRestraint (CustomBondForce)
 group 1 (analytic): CustomBond/Angle/Torsion  "lambda1*…"  "lambda2*…"
                     MSLDLJ_1, MSLDLJ_2  (env↔b and b↔b groups)   [MSLDLJ_b_c for cross-site]
                     MSLDWBElec_b (within-block real-space correction)
```

## Invariants it must keep
I1, I5, I6, I8, I10 in [[Invariants]].

## As-built status
Tests: `test_master`, `test_builder`, `test_angles_torsions`, `test_charmm_terms`,
`test_electrostatics`, `test_within_block_elec`, `test_lj`, `test_charmm_nbfix_lj`,
`test_exceptions`, `test_biases`, `test_restraints`, `test_grill`, `test_analytic_dudl`,
`test_minimize`.
Issues: reaction-field cutoffs wrong ([[ISS-003 Within-block correction wrong for cutoff methods|ISS-003]]); CHARMM LJ exclusions on CPU ([[ISS-004 CHARMM NBFIX systems fail on CPU|ISS-004]]);
unknown forces left unscaled ([[ISS-005 Unsupported force types silently unscaled|ISS-005]]); same-site PME convention ([[ISS-006 Same-site PME differs from BLaDE and docs are backwards|ISS-006]]); dispersion
correction dropped globally ([[ISS-007 Dispersion correction removed for the whole system|ISS-007]]); PME α ([[ISS-008 PME alpha recomputed from the tolerance|ISS-008]]); cross-site 1-4 and CMAP refused
([[ISS-015 Cross-site 1-4 and CMAP are refused|ISS-015]]); no soft-core ([[ISS-013 Soft-core off while BLaDE examples use it|ISS-013]]).

