---
title: Project timeline
type: history
status: active
updated: 2026-09-27
---
# Project timeline

Reconstructed from git history, file dates, earlier Claude session memory and the audit.

| date | event | links |
|---|---|---|
| 2026-07-10…20 | Environment, OpenMM study; phase plan (M0–M5) written in the old vault | [[TASK-001 Set up the environment and study OpenMM\|TASK-001]] |
| 2026-07-14…08-12 | BLaDE internals studied (λ/θ, integrator, scaling, PME, T4L input) | [[TASK-002 Study BLaDE internals\|TASK-002]] |
| 2026-07-27 | First commit: data model | [[TASK-003 Implement the MSLD data model\|TASK-003]] |
| 2026-07-31 | Bonded scaling + builder | [[TASK-004 Implement bonded term scaling\|TASK-004]] |
| 2026-08-05 | Nonbonded scaling (charges, LJ, 1-4, same-site) | [[TASK-005 Implement nonbonded scaling\|TASK-005]] |
| 2026-08-10 | Integrator; biases, restraints, constraints ("physics complete") | [[TASK-006 Implement the lambda-dynamics integrator\|TASK-006]], [[TASK-007 Add biases, restraints and constraints\|TASK-007]] |
| 2026-08-12…14 | Prep v1: mapping, charges, ParmEd merge, cross-variant check, CHARMM impropers — **last commit pushed (7863097)** | [[TASK-008 Site mapping data model\|TASK-008]]…[[TASK-011 Cross-variant check and CHARMM impropers\|TASK-011]] |
| 2026-08-15…17 | CHARMM NBFIX LJ, solvation, within-block linear electrostatics | [[TASK-012 Scale CHARMM NBFIX LJ\|TASK-012]]…[[TASK-014 Make within-block electrostatics linear\|TASK-014]] |
| 2026-08-18…19 | Prep redesign phases A–J, sub-packages | [[TASK-015 Prep redesign phases A to I\|TASK-015]]…[[TASK-017 Reorganize prep into sub-packages\|TASK-017]] |
| 2026-08-21 | RDKit hard dependency; MDM2 inputs added | [[TASK-016 MCS ligand mapper and RDKit\|TASK-016]] |
| 2026-09-01 | Docs consolidated (GUIDE/DEFERRED/README); monomer variants; façade | [[TASK-018 Consolidate the documentation\|TASK-018]]…[[TASK-020 Prep facade build_msld_system\|TASK-020]] |
| 2026-09-15 | MDM2 end-to-end; OpenCL; exclusion parity; minimize; reporters; output fixes | [[TASK-021 Make the MDM2 run work end to end\|TASK-021]], [[TASK-022 Fix hybrid output artifacts\|TASK-022]], [[TASK-025 Trajectory and lambda reporters\|TASK-025]], [[EXP-007 MDM2 first end-to-end run and benchmark\|EXP-007]] |
| 2026-09-16 | θ sweep; ALF P1–P3 | [[EXP-006 MDM2 theta-parameter sweep\|EXP-006]], [[TASK-024 ALF phases 1 to 3\|TASK-024]] |
| 2026-09-17 | Tier 0 analytic dU/dλ | [[TASK-026 Tier 0 analytic dU-dlambda\|TASK-026]] |
| 2026-09-21 | Separate C++ course project `msld-cl` started (not part of this repo) | — |
| 2026-09-23 | Plugin plan S0–S4; toolchain verified | [[TASK-027 Scope the C++ plugin\|TASK-027]] |
| 2026-09-26 | Claude Project created; two laptops linked; full audit of the engine | [[TASK-028 Audit the local working copy\|TASK-028]], [[AUD-001 Engine audit of the local working copy\|AUD-001]] |
| 2026-09-27 | Knowledge vault built; retrospective ADRs; issues and tasks | [[TASK-029 Build the project knowledge vault\|TASK-029]], [[ADR-0031 Project knowledge system in an Obsidian vault\|ADR-0031]] |

