---
title: Test catalog
type: verification
status: active
updated: 2026-09-27
---
# Test catalog

33 self-running test files (`tests/test_*.py`), all passing on 2026-09-26 (OpenMM 8.5.2, ~40 s).
Run: `for t in tests/test_*.py; do python "$t"; done` in the `msld` env. Mostly Reference platform.

## Engine
| test | checks | requirements |
|---|---|---|
| `test_master` | λ = 1 ≡ base, energy and forces (~1e-13) | [[REQ-023 Lambda one reproduces the base system\|REQ-023]] |
| `test_model` | model invariants, classifiers, softmax | [[REQ-001 Represent sites, blocks and environment\|REQ-001]], [[REQ-002 Lambda from theta with implicit constraints\|REQ-002]] |
| `test_builder` | bonded scaling + dU/dλ (analytic vs FD vs OpenMM deriv) | [[REQ-003 Scale bonded terms by block lambdas\|REQ-003]] |
| `test_angles_torsions` | angle/torsion single- and product-λ | [[REQ-003 Scale bonded terms by block lambdas\|REQ-003]] |
| `test_charmm_terms` | CHARMM impropers + UB, λ = 1 ≡ base | [[REQ-003 Scale bonded terms by block lambdas\|REQ-003]] |
| `test_electrostatics` | charge offsets, same-site exclusion, λ = 1 ≡ base | [[REQ-005 Nonbonded pair scaling rules\|REQ-005]], [[REQ-006 Same-site pairs never interact\|REQ-006]], [[REQ-007 PME electrostatics at partial lambda\|REQ-007]] |
| `test_within_block_elec` | within-block linear (NoCutoff exact, PME erfc exact) | [[REQ-005 Nonbonded pair scaling rules\|REQ-005]] |
| `test_grill` | same-site PME cancellation; dU/dλ sums across forces | [[REQ-006 Same-site pairs never interact\|REQ-006]], [[REQ-007 PME electrostatics at partial lambda\|REQ-007]] |
| `test_lj` | grouped LJ, analytic dU/dλ | [[REQ-008 LJ scaling including NBFIX\|REQ-008]] |
| `test_charmm_nbfix_lj` | CHARMM tabulated LJ scaled, λ = 1 ≡ base | [[REQ-008 LJ scaling including NBFIX\|REQ-008]] |
| `test_exceptions` | 1-4 exception offsets | [[REQ-009 1-4 pair scaling\|REQ-009]] |
| `test_biases` | fixed + variable 6/8/10 biases, removescaling flags | [[REQ-012 Fixed and variable lambda biases\|REQ-012]], [[REQ-004 Configurable bonded scaling per term type\|REQ-004]] |
| `test_restraints` | restraint force = centroid formula (not the group semantics!) | [[REQ-014 Atom restraints between substituents\|REQ-014]] |
| `test_constraints` | SHAKE/RATTLE with moving λ | [[REQ-018 Holonomic constraints and virtual sites\|REQ-018]] |
| `test_integrator` | θ-force = FD; stable dynamics; T_θ sanity | [[REQ-016 Canonical sampling of atoms and theta\|REQ-016]], [[REQ-002 Lambda from theta with implicit constraints\|REQ-002]] |
| `test_analytic_dudl` | Tier-0 hybrid dU/dλ = full FD; group split; biases not dropped | [[REQ-020 Accurate dU-dlambda for every term\|REQ-020]] |
| `test_minimize` | minimize relaxes a clash; identical exclusion sets | [[REQ-026 Energy minimization at fixed lambda\|REQ-026]], [[REQ-021 Runs on Reference, CPU, OpenCL, CUDA\|REQ-021]] |
| `test_io` | CSV + DCD reporters, populations, trajectory PDB CONECT | [[REQ-027 Trajectory, lambda and energy output\|REQ-027]] |
| `test_alf` | heuristic ALF P1–P3 on toys | [[REQ-030 Adaptive landscape flattening\|REQ-030]] |

## Preparation
| test | checks | requirements |
|---|---|---|
| `test_ingest` | all ingest routes + error messages | [[REQ-040 Ingest Amber, CHARMM, PDB and SDF inputs\|REQ-040]], [[REQ-041 Lossless parameters including NBFIX\|REQ-041]] |
| `test_mapping_core` | CoreMapping (+ JSON), HybridBlueprint, Mapper base | [[REQ-044 Multiple sites per system\|REQ-044]] |
| `test_backbone_mapper` | name + LJ core, backbone-mutation flag | [[REQ-042 Map amino-acid mutation sites\|REQ-042]] |
| `test_mcs` | MCS assembly/graph, buffer atoms | [[REQ-043 Map ligand R-group sites\|REQ-043]] |
| `test_prep_mapping` | ManualMapper, model_from_mappings | [[REQ-001 Represent sites, blocks and environment\|REQ-001]] |
| `test_aligner` | Kabsch, BackboneAligner, IdentityAligner | [[REQ-045 Place variant coordinates in the shared frame\|REQ-045]] |
| `test_hybrid_builder` | **gate**: WT-on = original MDM2 peptide energy (3e-15, ff14SB) | [[REQ-042 Map amino-acid mutation sites\|REQ-042]], [[REQ-045 Place variant coordinates in the shared frame\|REQ-045]] |
| `test_renorm` | ChargeRenormalization spread/proportional/buffer | [[REQ-046 Consistent charges across variants\|REQ-046]] |
| `test_prep_charges` | iso-charge guard, renormalize, Amber averaging | [[REQ-046 Consistent charges across variants\|REQ-046]] |
| `test_prep_cross_variant` | find/assert/delete cross-variant terms | [[REQ-048 No bonded term between same-site blocks\|REQ-048]] |
| `test_prep_solvate` | Amber + CHARMM solvation, ions, ion–water NBFIX | [[REQ-047 Solvate and neutralize consistently\|REQ-047]], [[REQ-041 Lossless parameters including NBFIX\|REQ-041]] |
| `test_hybrid_system` | assembler hub, bundle save, solvated PME | [[REQ-049 Prep hands off a plain System and a model\|REQ-049]] |
| `test_hybrid_output` | merged HYB PDB, CONECT, CRYST1, TER, FF XML | [[REQ-050 Inspectable prep artifacts\|REQ-050]] |
| `test_build` | façade, per-part FF, monomer variants | [[REQ-049 Prep hands off a plain System and a model\|REQ-049]] |

## Missing (see [[Verification strategy]])
Partial-λ oracle ([[TASK-067 NumPy partial-lambda oracle tests|TASK-067]]); BLaDE cross-check ([[TASK-043 BLaDE fixed-lambda cross-check|TASK-043]]); CHARMM exclusion parity
([[TASK-034 Add same-site exclusions to CHARMM LJ copies|TASK-034]]); dispersion-on master test ([[TASK-036 Preserve env-env dispersion correction|TASK-036]]); cutoff-method refusal ([[TASK-038 Refuse reaction-field cutoff methods|TASK-038]]);
restraint group semantics ([[TASK-031 Rebuild atom restraint groups|TASK-031]]); λ distribution in a real system.

