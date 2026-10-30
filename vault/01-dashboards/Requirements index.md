---
title: Requirements index
type: dashboard
status: active
updated: 2026-09-27
---
# Requirements index and traceability

```dataview
TABLE title, area, priority, status, satisfied_by, verified_by
FROM "10-product/requirements"
WHERE type = "requirement"
SORT id ASC
```

## Static index (generated)
<!-- BEGIN GENERATED -->
| req | title | area | priority | status | satisfied by | verified by |
|---|---|---|---|---|---|---|
| [[REQ-001 Represent sites, blocks and environment\|REQ-001]] | Represent sites, blocks and environment | engine | must | implemented | [[FEAT-001 MSLD data model\|FEAT-001]] | test_model |
| [[REQ-002 Lambda from theta with implicit constraints\|REQ-002]] | Lambda from theta with implicit constraints | engine | must | implemented | [[FEAT-001 MSLD data model\|FEAT-001]], [[FEAT-008 Lambda-dynamics integrator\|FEAT-008]] | test_model, test_integrator, [[EXP-001 Theta samples the exact Boltzmann distribution on a toy\|EXP-001]] |
| [[REQ-003 Scale bonded terms by block lambdas\|REQ-003]] | Scale bonded terms by block lambdas | engine | must | implemented | [[FEAT-002 Bonded term scaling\|FEAT-002]] | test_builder, test_angles_torsions, test_charmm_terms, test_master |
| [[REQ-004 Configurable bonded scaling per term type\|REQ-004]] | Configurable bonded scaling per term type | engine | must | partial | [[FEAT-002 Bonded term scaling\|FEAT-002]] | test_biases |
| [[REQ-005 Nonbonded pair scaling rules\|REQ-005]] | Nonbonded pair scaling rules | engine | must | implemented | [[FEAT-003 Electrostatics scaling\|FEAT-003]], [[FEAT-004 Lennard-Jones scaling\|FEAT-004]] | test_lj, test_electrostatics, test_within_block_elec, test_grill, test_master |
| [[REQ-006 Same-site pairs never interact\|REQ-006]] | Same-site pairs never interact | engine | must | implemented | [[FEAT-003 Electrostatics scaling\|FEAT-003]], [[FEAT-004 Lennard-Jones scaling\|FEAT-004]] | test_electrostatics, test_grill, test_minimize |
| [[REQ-007 PME electrostatics at partial lambda\|REQ-007]] | PME electrostatics at partial lambda | engine | must | partial | [[FEAT-003 Electrostatics scaling\|FEAT-003]] | test_electrostatics, test_grill |
| [[REQ-008 LJ scaling including NBFIX\|REQ-008]] | LJ scaling including NBFIX | engine | must | partial | [[FEAT-004 Lennard-Jones scaling\|FEAT-004]] | test_lj, test_charmm_nbfix_lj |
| [[REQ-009 1-4 pair scaling\|REQ-009]] | 1-4 pair scaling | engine | must | partial | [[FEAT-005 1-4 exception scaling\|FEAT-005]] | test_exceptions |
| [[REQ-010 CMAP scaling\|REQ-010]] | CMAP scaling | engine | should | deferred | [[FEAT-036 CMAP scaling\|FEAT-036]] | — |
| [[REQ-011 Soft-core for alchemical nonbonded\|REQ-011]] | Soft-core for alchemical nonbonded | engine | should | deferred | [[FEAT-031 Soft-core\|FEAT-031]] | — |
| [[REQ-012 Fixed and variable lambda biases\|REQ-012]] | Fixed and variable lambda biases | engine | must | implemented | [[FEAT-006 Lambda biases\|FEAT-006]] | test_biases, test_alf |
| [[REQ-013 Theta biases\|REQ-013]] | Theta biases | engine | could | deferred | [[FEAT-038 Theta biases\|FEAT-038]] | — |
| [[REQ-014 Atom restraints between substituents\|REQ-014]] | Atom restraints between substituents | engine | must | partial | [[FEAT-007 Atom restraints\|FEAT-007]] | test_restraints |
| [[REQ-015 Charge-changing perturbations\|REQ-015]] | Charge-changing perturbations | engine | could | deferred | [[FEAT-037 Charge-changing perturbations\|FEAT-037]] | — |
| [[REQ-016 Canonical sampling of atoms and theta\|REQ-016]] | Canonical sampling of atoms and theta | engine | must | partial | [[FEAT-008 Lambda-dynamics integrator\|FEAT-008]] | test_integrator, [[EXP-001 Theta samples the exact Boltzmann distribution on a toy\|EXP-001]] |
| [[REQ-017 Per-block theta mass, friction and fixing\|REQ-017]] | Per-block theta mass, friction and fixing | engine | must | partial | [[FEAT-008 Lambda-dynamics integrator\|FEAT-008]] | — |
| [[REQ-018 Holonomic constraints and virtual sites\|REQ-018]] | Holonomic constraints and virtual sites | engine | must | partial | [[FEAT-008 Lambda-dynamics integrator\|FEAT-008]] | test_constraints |
| [[REQ-019 NPT ensemble\|REQ-019]] | NPT ensemble | engine | must | proposed | [[FEAT-032 NPT ensemble\|FEAT-032]] | — |
| [[REQ-020 Accurate dU-dlambda for every term\|REQ-020]] | Accurate dU/dlambda for every term | engine | must | partial | [[FEAT-009 Tier-0 analytic dU-dlambda\|FEAT-009]], [[FEAT-033 Analytic nonbonded plugin force\|FEAT-033]] | test_analytic_dudl, [[EXP-008 Tier-0 derivative exactness\|EXP-008]] |
| [[REQ-021 Runs on Reference, CPU, OpenCL, CUDA\|REQ-021]] | Runs on Reference, CPU, OpenCL, CUDA | platform | must | partial | [[FEAT-010 Multi-platform support\|FEAT-010]] | test_minimize, [[EXP-002 Platform compatibility of scaled toys\|EXP-002]] |
| [[REQ-022 Refuse unsupported input loudly\|REQ-022]] | Refuse unsupported input loudly | engine | must | partial | [[FEAT-047 Engine hardening\|FEAT-047]] | — |
| [[REQ-023 Lambda one reproduces the base system\|REQ-023]] | Lambda one reproduces the base system | engine | must | verified | [[FEAT-002 Bonded term scaling\|FEAT-002]], [[FEAT-003 Electrostatics scaling\|FEAT-003]], [[FEAT-004 Lennard-Jones scaling\|FEAT-004]], [[FEAT-005 1-4 exception scaling\|FEAT-005]] | test_master |
| [[REQ-024 Dispersion correction preserved\|REQ-024]] | Dispersion correction preserved | engine | should | partial | [[FEAT-047 Engine hardening\|FEAT-047]] | — |
| [[REQ-025 Supported nonbonded methods are correct\|REQ-025]] | Supported nonbonded methods are correct | engine | must | partial | [[FEAT-047 Engine hardening\|FEAT-047]] | — |
| [[REQ-026 Energy minimization at fixed lambda\|REQ-026]] | Energy minimization at fixed lambda | engine | must | implemented | [[FEAT-023 Minimization at fixed lambda\|FEAT-023]] | test_minimize |
| [[REQ-027 Trajectory, lambda and energy output\|REQ-027]] | Trajectory, lambda and energy output | engine | must | partial | [[FEAT-011 Trajectory and lambda output\|FEAT-011]] | test_io |
| [[REQ-028 Checkpoint and restart\|REQ-028]] | Checkpoint and restart | engine | should | proposed | [[FEAT-046 Checkpoint and restart\|FEAT-046]] | — |
| [[REQ-029 Production performance on GPU\|REQ-029]] | Production performance on GPU | platform | must | proposed | [[FEAT-033 Analytic nonbonded plugin force\|FEAT-033]], [[FEAT-034 Fused MSLD integrator plugin\|FEAT-034]] | — |
| [[REQ-030 Adaptive landscape flattening\|REQ-030]] | Adaptive landscape flattening | run | must | partial | [[FEAT-012 ALF flattening heuristic\|FEAT-012]], [[FEAT-035 Standard ALF\|FEAT-035]] | test_alf, [[EXP-009 Heuristic ALF on toys\|EXP-009]] |
| [[REQ-031 Reproducible runs\|REQ-031]] | Reproducible runs | run | should | partial | — | — |
| [[REQ-040 Ingest Amber, CHARMM, PDB and SDF inputs\|REQ-040]] | Ingest Amber, CHARMM, PDB and SDF inputs | prep | must | implemented | [[FEAT-013 Ingest pipeline\|FEAT-013]] | test_ingest |
| [[REQ-041 Lossless parameters including NBFIX\|REQ-041]] | Lossless parameters including NBFIX | prep | must | implemented | [[FEAT-014 CHARMM NBFIX preservation\|FEAT-014]] | test_ingest, test_prep_solvate |
| [[REQ-042 Map amino-acid mutation sites\|REQ-042]] | Map amino-acid mutation sites | prep | must | implemented | [[FEAT-015 Peptide backbone mapper\|FEAT-015]] | test_backbone_mapper, test_hybrid_builder |
| [[REQ-043 Map ligand R-group sites\|REQ-043]] | Map ligand R-group sites | prep | must | partial | [[FEAT-016 Ligand MCS mapper\|FEAT-016]] | test_mcs |
| [[REQ-044 Multiple sites per system\|REQ-044]] | Multiple sites per system | prep | must | partial | [[FEAT-017 Hybrid structure grafting\|FEAT-017]] | test_mapping_core |
| [[REQ-045 Place variant coordinates in the shared frame\|REQ-045]] | Place variant coordinates in the shared frame | prep | must | implemented | [[FEAT-017 Hybrid structure grafting\|FEAT-017]] | test_aligner, test_hybrid_builder |
| [[REQ-046 Consistent charges across variants\|REQ-046]] | Consistent charges across variants | prep | must | implemented | [[FEAT-018 Charge renormalization\|FEAT-018]] | test_prep_charges, test_renorm |
| [[REQ-047 Solvate and neutralize consistently\|REQ-047]] | Solvate and neutralize consistently | prep | must | implemented | [[FEAT-019 Solvation and ions\|FEAT-019]] | test_prep_solvate, test_hybrid_system |
| [[REQ-048 No bonded term between same-site blocks\|REQ-048]] | No bonded term between same-site blocks | prep | must | implemented | [[FEAT-017 Hybrid structure grafting\|FEAT-017]] | test_prep_cross_variant |
| [[REQ-049 Prep hands off a plain System and a model\|REQ-049]] | Prep hands off a plain System and a model | prep | must | implemented | [[FEAT-020 System build and bundle outputs\|FEAT-020]] | test_hybrid_system, test_build |
| [[REQ-050 Inspectable prep artifacts\|REQ-050]] | Inspectable prep artifacts | prep | should | implemented | [[FEAT-020 System build and bundle outputs\|FEAT-020]] | test_hybrid_output |
| [[REQ-051 Validate input geometry\|REQ-051]] | Validate input geometry | prep | should | proposed | [[FEAT-043 Input geometry validation\|FEAT-043]] | — |
| [[REQ-052 Import a BLaDE or CHARMM MSLD setup\|REQ-052]] | Import a BLaDE or CHARMM MSLD setup | validation | must | proposed | [[FEAT-030 BLaDE cross-validation harness\|FEAT-030]] | — |
| [[REQ-060 Free energy per variant with uncertainty\|REQ-060]] | Free energy per variant with uncertainty | analysis | must | partial | [[FEAT-040 Free-energy analysis subsystem\|FEAT-040]] | — |
| [[REQ-061 Relative ddG from two legs\|REQ-061]] | Relative ddG from two legs | analysis | must | proposed | [[FEAT-040 Free-energy analysis subsystem\|FEAT-040]] | — |
| [[REQ-062 Sampling and convergence diagnostics\|REQ-062]] | Sampling and convergence diagnostics | analysis | must | proposed | [[FEAT-040 Free-energy analysis subsystem\|FEAT-040]] | — |
| [[REQ-063 Combinatorial multi-site free energies\|REQ-063]] | Combinatorial multi-site free energies | analysis | should | proposed | [[FEAT-040 Free-energy analysis subsystem\|FEAT-040]] | — |
| [[REQ-070 Agree with BLaDE on a shared CHARMM system\|REQ-070]] | Agree with BLaDE on a shared CHARMM system | validation | must | proposed | [[FEAT-030 BLaDE cross-validation harness\|FEAT-030]] | — |
| [[REQ-071 Agree with FEP or TI on Amber\|REQ-071]] | Agree with FEP or TI on Amber | validation | should | proposed | [[FEAT-041 Amber validation vs FEP or TI\|FEAT-041]] | — |
| [[REQ-072 Every feature has an automated test\|REQ-072]] | Every feature has an automated test | process | must | implemented | — | test_master |
| [[REQ-073 Documentation and traceability\|REQ-073]] | Documentation and traceability | process | must | implemented | [[FEAT-044 Knowledge vault and process\|FEAT-044]] | — |
| [[REQ-074 Engine free of prep dependencies\|REQ-074]] | Engine free of prep dependencies | process | should | implemented | — | — |
<!-- END GENERATED -->

