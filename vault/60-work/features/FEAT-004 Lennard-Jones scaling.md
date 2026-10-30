---
id: FEAT-004
type: feature
title: Lennard-Jones scaling
status: needs-rework
milestone: M1
implements: ["[[REQ-005 Nonbonded pair scaling rules|REQ-005]]", "[[REQ-008 LJ scaling including NBFIX|REQ-008]]", "[[REQ-024 Dispersion correction preserved|REQ-024]]"]
components: ["[[Lennard-Jones scaling module]]"]
decisions: ["[[ADR-0008 LJ scaled by grouped CustomNonbondedForces|ADR-0008]]", "[[ADR-0039 Dispersion correction handling|ADR-0039]]"]
tasks: ["[[TASK-005 Implement nonbonded scaling|TASK-005]]", "[[TASK-012 Scale CHARMM NBFIX LJ|TASK-012]]", "[[TASK-034 Add same-site exclusions to CHARMM LJ copies|TASK-034]]", "[[TASK-036 Preserve env-env dispersion correction|TASK-036]]"]
issues: ["[[ISS-004 CHARMM NBFIX systems fail on CPU|ISS-004]]", "[[ISS-007 Dispersion correction removed for the whole system|ISS-007]]"]
created: 2026-08-05
updated: 2026-09-27
retrospective: true
---
# FEAT-004 — Lennard-Jones scaling

Amber LJ via grouped `CustomNonbondedForce`s; CHARMM tabulated NBFIX LJ via copied tables. Rework:
CHARMM same-site exclusions on CPU ([[TASK-034 Add same-site exclusions to CHARMM LJ copies|TASK-034]]), dispersion correction ([[TASK-036 Preserve env-env dispersion correction|TASK-036]]).

