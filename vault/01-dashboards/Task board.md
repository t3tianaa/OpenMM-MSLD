---
title: Task board
type: dashboard
status: active
updated: 2026-09-27
---
# Task board

## Open tasks by priority (Dataview)
```dataview
TABLE title, status, priority, milestone, feature
FROM "60-work/tasks"
WHERE type = "task" AND status != "done" AND status != "cancelled"
SORT priority ASC, id ASC
```

## Static index (generated)
<!-- BEGIN GENERATED -->
### review (1)

| task | title | priority | milestone | feature |
|---|---|---|---|---|
| [[TASK-029 Build the project knowledge vault\|TASK-029]] | Build the project knowledge vault | P0 | M4 | [[FEAT-044 Knowledge vault and process\|FEAT-044]] |

### todo (45)

| task | title | priority | milestone | feature |
|---|---|---|---|---|
| [[TASK-030 Commit and push the local state to a branch\|TASK-030]] | Commit and push the local state to a branch | P0 | M4 | [[FEAT-044 Knowledge vault and process\|FEAT-044]] |
| [[TASK-031 Rebuild atom restraint groups\|TASK-031]] | Rebuild atom restraint groups | P0 | M4 | [[FEAT-007 Atom restraints\|FEAT-007]] |
| [[TASK-034 Add same-site exclusions to CHARMM LJ copies\|TASK-034]] | Add same-site exclusions to CHARMM LJ copies | P1 | M4 | [[FEAT-047 Engine hardening\|FEAT-047]] |
| [[TASK-035 Whitelist force types\|TASK-035]] | Whitelist force types | P1 | M4 | [[FEAT-047 Engine hardening\|FEAT-047]] |
| [[TASK-036 Preserve env-env dispersion correction\|TASK-036]] | Preserve env-env dispersion correction | P1 | M4 | [[FEAT-047 Engine hardening\|FEAT-047]] |
| [[TASK-038 Refuse reaction-field cutoff methods\|TASK-038]] | Refuse reaction-field cutoff methods | P1 | M4 | [[FEAT-047 Engine hardening\|FEAT-047]] |
| [[TASK-040 Audit the preparation layer\|TASK-040]] | Audit the preparation layer | P1 | M4 | [[FEAT-013 Ingest pipeline\|FEAT-013]] |
| [[TASK-042 Get BLaDE running with reference data\|TASK-042]] | Get BLaDE running with reference data | P1 | M5 | [[FEAT-030 BLaDE cross-validation harness\|FEAT-030]] |
| [[TASK-043 BLaDE fixed-lambda cross-check\|TASK-043]] | BLaDE fixed-lambda cross-check | P1 | M5 | [[FEAT-030 BLaDE cross-validation harness\|FEAT-030]] |
| [[TASK-044 Decide the same-site PME convention\|TASK-044]] | Decide the same-site PME convention | P1 | M5 | [[FEAT-003 Electrostatics scaling\|FEAT-003]] |
| [[TASK-045 Import BLaDE MSLD setups\|TASK-045]] | Import BLaDE MSLD setups | P1 | M5 | [[FEAT-030 BLaDE cross-validation harness\|FEAT-030]] |
| [[TASK-070 CHARMM force switching for the cross-check\|TASK-070]] | CHARMM force switching for the cross-check | P1 | M5 | [[FEAT-030 BLaDE cross-validation harness\|FEAT-030]] |
| [[TASK-072 Point agents to the vault via CLAUDE.md\|TASK-072]] | Point agents to the vault via CLAUDE.md | P1 | M4 | [[FEAT-044 Knowledge vault and process\|FEAT-044]] |
| [[TASK-078 Fixed-lambda replica-exchange cross-check\|TASK-078]] | Fixed-lambda replica-exchange cross-check | P1 | M5 | [[FEAT-041 Amber validation vs FEP or TI\|FEAT-041]] |
| [[TASK-037 Read PME alpha from the force\|TASK-037]] | Read PME alpha from the force | P2 | M4 | [[FEAT-047 Engine hardening\|FEAT-047]] |
| [[TASK-039 Handle zero-mass particles in the integrator\|TASK-039]] | Handle zero-mass particles in the integrator | P2 | M4 | [[FEAT-047 Engine hardening\|FEAT-047]] |
| [[TASK-041 Analytic bias derivatives\|TASK-041]] | Analytic bias derivatives | P2 | M4 | [[FEAT-006 Lambda biases\|FEAT-006]] |
| [[TASK-046 Implement or adopt standard ALF\|TASK-046]] | Implement or adopt standard ALF | P2 | M6 | [[FEAT-035 Standard ALF\|FEAT-035]] |
| [[TASK-047 Two-leg ddG estimator\|TASK-047]] | Two-leg ddG estimator | P2 | M6 | [[FEAT-040 Free-energy analysis subsystem\|FEAT-040]] |
| [[TASK-048 Sampling diagnostics\|TASK-048]] | Sampling diagnostics | P2 | M6 | [[FEAT-040 Free-energy analysis subsystem\|FEAT-040]] |
| [[TASK-049 Interim NPT in the Python driver\|TASK-049]] | Interim NPT in the Python driver | P2 | M7 | [[FEAT-032 NPT ensemble\|FEAT-032]] |
| [[TASK-050 Soft-core design spike\|TASK-050]] | Soft-core design spike | P2 | M7 | [[FEAT-031 Soft-core\|FEAT-031]] |
| [[TASK-055 Validate input geometry\|TASK-055]] | Validate input geometry | P2 | M4 | [[FEAT-043 Input geometry validation\|FEAT-043]] |
| [[TASK-057 BLaDE-style bonded scaling switches\|TASK-057]] | BLaDE-style bonded scaling switches | P2 | M4 | [[FEAT-002 Bonded term scaling\|FEAT-002]] |
| [[TASK-058 Plugin S0 skeleton\|TASK-058]] | Plugin S0 skeleton | P2 | M7 | [[FEAT-033 Analytic nonbonded plugin force\|FEAT-033]] |
| [[TASK-059 Plugin S1 Reference nonbonded force\|TASK-059]] | Plugin S1 Reference nonbonded force | P2 | M7 | [[FEAT-033 Analytic nonbonded plugin force\|FEAT-033]] |
| [[TASK-071 Checkpoint and restart\|TASK-071]] | Checkpoint and restart | P2 | M6 | [[FEAT-046 Checkpoint and restart\|FEAT-046]] |
| [[TASK-074 Study the ALF package\|TASK-074]] | Study the ALF package | P2 | M6 | [[FEAT-035 Standard ALF\|FEAT-035]] |
| [[TASK-075 Study OpenMM nonbonded kernels for the plugin\|TASK-075]] | Study OpenMM nonbonded kernels for the plugin | P2 | M7 | [[FEAT-033 Analytic nonbonded plugin force\|FEAT-033]] |
| [[TASK-051 Implement theta biases\|TASK-051]] | Implement theta biases | P3 | M6 | [[FEAT-038 Theta biases\|FEAT-038]] |
| [[TASK-052 Cross-site 1-4 scaling\|TASK-052]] | Cross-site 1-4 scaling | P3 | M8 | [[FEAT-039 Cross-site 1-4 scaling\|FEAT-039]] |
| [[TASK-053 CMAP scaling spike\|TASK-053]] | CMAP scaling spike | P3 | M8 | [[FEAT-036 CMAP scaling\|FEAT-036]] |
| [[TASK-054 Charge-changing perturbations\|TASK-054]] | Charge-changing perturbations | P3 | M8 | [[FEAT-037 Charge-changing perturbations\|FEAT-037]] |
| [[TASK-056 Fixed-block semantics like BLaDE\|TASK-056]] | Fixed-block semantics like BLaDE | P3 | M5 | [[FEAT-008 Lambda-dynamics integrator\|FEAT-008]] |
| [[TASK-060 Plugin S2 GPU kernels\|TASK-060]] | Plugin S2 GPU kernels | P3 | M7 | [[FEAT-033 Analytic nonbonded plugin force\|FEAT-033]] |
| [[TASK-061 Plugin S3 fused integrator\|TASK-061]] | Plugin S3 fused integrator | P3 | M7 | [[FEAT-034 Fused MSLD integrator plugin\|FEAT-034]] |
| [[TASK-062 Plugin S4 soft-core\|TASK-062]] | Plugin S4 soft-core | P3 | M7 | [[FEAT-031 Soft-core\|FEAT-031]] |
| [[TASK-063 CUDA validation run on the cluster\|TASK-063]] | CUDA validation run on the cluster | P3 | M7 | [[FEAT-010 Multi-platform support\|FEAT-010]] |
| [[TASK-064 Amber FEP or TI comparison\|TASK-064]] | Amber FEP or TI comparison | P3 | M8 | [[FEAT-041 Amber validation vs FEP or TI\|FEAT-041]] |
| [[TASK-065 GROMACS and frcmod ingest routes\|TASK-065]] | GROMACS and frcmod ingest routes | P3 | M8 | [[FEAT-042 Additional ingest routes\|FEAT-042]] |
| [[TASK-066 Consider a pytest-compatible test layout\|TASK-066]] | Consider a pytest-compatible test layout | P3 | M4 | [[FEAT-044 Knowledge vault and process\|FEAT-044]] |
| [[TASK-068 Buffer atom duplication\|TASK-068]] | Buffer atom duplication | P3 | M8 | [[FEAT-018 Charge renormalization\|FEAT-018]] |
| [[TASK-069 Scalable LJ grouping for many sites\|TASK-069]] | Scalable LJ grouping for many sites | P3 | M7 | [[FEAT-004 Lennard-Jones scaling\|FEAT-004]] |
| [[TASK-076 Pin literature citations\|TASK-076]] | Pin literature citations | P3 | M4 | [[FEAT-044 Knowledge vault and process\|FEAT-044]] |
| [[TASK-077 Mine earlier sessions for decision history\|TASK-077]] | Mine earlier sessions for decision history | P3 | M4 | [[FEAT-044 Knowledge vault and process\|FEAT-044]] |

### done (33)

| task | title | priority | milestone | feature |
|---|---|---|---|---|
| [[TASK-001 Set up the environment and study OpenMM\|TASK-001]] | Set up the environment and study OpenMM | P1 | M0 | [[FEAT-001 MSLD data model\|FEAT-001]] |
| [[TASK-002 Study BLaDE internals\|TASK-002]] | Study BLaDE internals | P1 | M0 | [[FEAT-001 MSLD data model\|FEAT-001]] |
| [[TASK-003 Implement the MSLD data model\|TASK-003]] | Implement the MSLD data model | P1 | M1 | [[FEAT-001 MSLD data model\|FEAT-001]] |
| [[TASK-004 Implement bonded term scaling\|TASK-004]] | Implement bonded term scaling | P1 | M1 | [[FEAT-002 Bonded term scaling\|FEAT-002]] |
| [[TASK-005 Implement nonbonded scaling\|TASK-005]] | Implement nonbonded scaling | P1 | M1 | [[FEAT-003 Electrostatics scaling\|FEAT-003]] |
| [[TASK-006 Implement the lambda-dynamics integrator\|TASK-006]] | Implement the lambda-dynamics integrator | P1 | M2 | [[FEAT-008 Lambda-dynamics integrator\|FEAT-008]] |
| [[TASK-007 Add biases, restraints and constraints\|TASK-007]] | Add biases, restraints and constraints | P1 | M2 | [[FEAT-006 Lambda biases\|FEAT-006]] |
| [[TASK-008 Site mapping data model\|TASK-008]] | Site mapping data model | P1 | M3 | [[FEAT-015 Peptide backbone mapper\|FEAT-015]] |
| [[TASK-009 Partial-charge policy and Amber averaging\|TASK-009]] | Partial-charge policy and Amber averaging | P1 | M3 | [[FEAT-018 Charge renormalization\|FEAT-018]] |
| [[TASK-010 Merge per-variant topologies with ParmEd\|TASK-010]] | Merge per-variant topologies with ParmEd | P1 | M3 | [[FEAT-017 Hybrid structure grafting\|FEAT-017]] |
| [[TASK-011 Cross-variant check and CHARMM impropers\|TASK-011]] | Cross-variant check and CHARMM impropers | P1 | M3 | [[FEAT-002 Bonded term scaling\|FEAT-002]] |
| [[TASK-012 Scale CHARMM NBFIX LJ\|TASK-012]] | Scale CHARMM NBFIX LJ | P1 | M3 | [[FEAT-004 Lennard-Jones scaling\|FEAT-004]] |
| [[TASK-013 Solvation by overlay\|TASK-013]] | Solvation by overlay | P1 | M3 | [[FEAT-019 Solvation and ions\|FEAT-019]] |
| [[TASK-014 Make within-block electrostatics linear\|TASK-014]] | Make within-block electrostatics linear | P1 | M1 | [[FEAT-003 Electrostatics scaling\|FEAT-003]] |
| [[TASK-015 Prep redesign phases A to I\|TASK-015]] | Prep redesign phases A to I | P1 | M3 | [[FEAT-013 Ingest pipeline\|FEAT-013]] |
| [[TASK-016 MCS ligand mapper and RDKit\|TASK-016]] | MCS ligand mapper and RDKit | P1 | M3 | [[FEAT-016 Ligand MCS mapper\|FEAT-016]] |
| [[TASK-017 Reorganize prep into sub-packages\|TASK-017]] | Reorganize prep into sub-packages | P2 | M3 | [[FEAT-013 Ingest pipeline\|FEAT-013]] |
| [[TASK-018 Consolidate the documentation\|TASK-018]] | Consolidate the documentation | P2 | M3 | [[FEAT-044 Knowledge vault and process\|FEAT-044]] |
| [[TASK-019 Monomer variants via ignoreExternalBonds\|TASK-019]] | Monomer variants via ignoreExternalBonds | P1 | M3 | [[FEAT-021 Prep facade\|FEAT-021]] |
| [[TASK-020 Prep facade build_msld_system\|TASK-020]] | Prep facade build_msld_system | P1 | M3 | [[FEAT-021 Prep facade\|FEAT-021]] |
| [[TASK-021 Make the MDM2 run work end to end\|TASK-021]] | Make the MDM2 run work end to end | P0 | M3 | [[FEAT-022 MDM2 test system\|FEAT-022]] |
| [[TASK-022 Fix hybrid output artifacts\|TASK-022]] | Fix hybrid output artifacts | P2 | M3 | [[FEAT-020 System build and bundle outputs\|FEAT-020]] |
| [[TASK-023 Theta-stability sweep on MDM2\|TASK-023]] | Theta-stability sweep on MDM2 | P1 | M3 | [[FEAT-022 MDM2 test system\|FEAT-022]] |
| [[TASK-024 ALF phases 1 to 3\|TASK-024]] | ALF phases 1 to 3 | P1 | M6 | [[FEAT-012 ALF flattening heuristic\|FEAT-012]] |
| [[TASK-025 Trajectory and lambda reporters\|TASK-025]] | Trajectory and lambda reporters | P1 | M3 | [[FEAT-011 Trajectory and lambda output\|FEAT-011]] |
| [[TASK-026 Tier 0 analytic dU-dlambda\|TASK-026]] | Tier 0 analytic dU/dlambda | P1 | M2 | [[FEAT-009 Tier-0 analytic dU-dlambda\|FEAT-009]] |
| [[TASK-027 Scope the C++ plugin\|TASK-027]] | Scope the C++ plugin | P2 | M7 | [[FEAT-033 Analytic nonbonded plugin force\|FEAT-033]] |
| [[TASK-028 Audit the local working copy\|TASK-028]] | Audit the local working copy | P0 | M4 | [[FEAT-047 Engine hardening\|FEAT-047]] |
| [[TASK-032 Resolve BLaDE theta units\|TASK-032]] | Resolve BLaDE theta units | P0 | M4 | [[FEAT-008 Lambda-dynamics integrator\|FEAT-008]] |
| [[TASK-033 Rerun MDM2 with reference theta parameters\|TASK-033]] | Rerun MDM2 with reference theta parameters | P0 | M4 | [[FEAT-022 MDM2 test system\|FEAT-022]] |
| [[TASK-067 NumPy partial-lambda oracle tests\|TASK-067]] | NumPy partial-lambda oracle tests | P1 | M4 | [[FEAT-045 Independent partial-lambda oracle tests\|FEAT-045]] |
| [[TASK-073 Retire the legacy documents\|TASK-073]] | Retire the legacy documents | P2 | M4 | [[FEAT-044 Knowledge vault and process\|FEAT-044]] |
| [[TASK-079 Update the Mac env to OpenMM 8.6.1\|TASK-079]] | Update the Mac env to OpenMM 8.6.1 | P1 | M4 | [[FEAT-047 Engine hardening\|FEAT-047]] |
<!-- END GENERATED -->

