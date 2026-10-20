---
id: FEAT-033
type: feature
title: Analytic nonbonded plugin force
status: planned
milestone: M7
implements: ["[[REQ-020 Accurate dU-dlambda for every term|REQ-020]]", "[[REQ-029 Production performance on GPU|REQ-029]]", "[[REQ-007 PME electrostatics at partial lambda|REQ-007]]"]
components: ["[[Production plugin architecture]]"]
decisions: ["[[ADR-0026 Tier 2 plugin with scope S0 to S4|ADR-0026]]", "[[ADR-0027 Plugin technology choices|ADR-0027]]", "[[ADR-0035 Gate plugin work|ADR-0035]]"]
tasks: ["[[TASK-058 Plugin S0 skeleton|TASK-058]]", "[[TASK-059 Plugin S1 Reference nonbonded force|TASK-059]]", "[[TASK-060 Plugin S2 GPU kernels|TASK-060]]", "[[TASK-075 Study OpenMM nonbonded kernels for the plugin|TASK-075]]"]
created: 2026-09-23
updated: 2026-09-27
---
# FEAT-033 — Analytic nonbonded plugin force (`MSLDNonbondedForce`)

Plugin stages S0–S2: λ-scaled LJ + PME with analytic dU/dλ_b, Reference first, then common/GPU.

