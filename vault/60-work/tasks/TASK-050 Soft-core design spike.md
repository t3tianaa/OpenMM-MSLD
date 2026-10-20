---
id: TASK-050
type: task
title: Soft-core design spike
status: todo
kind: research
priority: P2
milestone: M7
feature: "[[FEAT-031 Soft-core|FEAT-031]]"
issues: ["[[ISS-013 Soft-core off while BLaDE examples use it|ISS-013]]"]
refs: ["[[Soft-core potentials]]", "[[BLaDE nonbonded direct space]]"]
created: 2026-09-27
updated: 2026-09-27
---
# TASK-050 — Soft-core design spike

Can BLaDE's r_eff soft-core be done for LJ + real-space Coulomb in CustomNonbondedForces while PME
reciprocal stays unsoftened (as in BLaDE)? Would require removing charged alchemical pairs' real-space
part from NonbondedForce. Write up options → ADR.

