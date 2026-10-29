---
id: FEAT-031
type: feature
title: Soft-core
status: in-progress
milestone: M7
implements: ["[[REQ-011 Soft-core for alchemical nonbonded|REQ-011]]"]
components: ["[[Production plugin architecture]]"]
decisions: ["[[ADR-0025 Soft-core off in the first version|ADR-0025]]", "[[ADR-0026 Tier 2 plugin with scope S0 to S4|ADR-0026]]"]
tasks: ["[[TASK-050 Soft-core design spike|TASK-050]]", "[[TASK-062 Plugin S4 soft-core|TASK-062]]"]
issues: ["[[ISS-013 Soft-core off while BLaDE examples use it|ISS-013]]"]
created: 2026-09-01
updated: 2026-10-29
---
# FEAT-031 — Soft-core

BLaDE-form soft-core for LJ and Coulomb. LJ possible in custom forces now; electrostatics under PME
needs the plugin (S4). Design spike first ([[TASK-050 Soft-core design spike|TASK-050]]).

**2026-10-29.** LJ + direct-space Coulomb soft-core implemented with custom forces ([[ADR-0043 Soft-core on by default for overlap-prone pairs|ADR-0043]]); remaining: CHARMM/NBFIX tabulated LJ, plugin S4.
