---
id: ADR-0025
type: adr
title: Soft-core off in the first version
status: accepted
date: 2026-08-05
deciders: [Tetiana]
affects: ["[[Lennard-Jones scaling module]]", "[[Electrostatics scaling module]]"]
requirements: ["[[REQ-011 Soft-core for alchemical nonbonded|REQ-011]]"]
retrospective: true
---
# ADR-0025 — Soft-core off in the first version

## Decision
Build the first correct λ-scaling without soft-core (simplest; U linear in λ keeps dU/dλ bounded).

## Consequences
- Energy function differs from BLaDE's examples, which run `softcore on` ([[ISS-013 Soft-core off while BLaDE examples use it|ISS-013]]); the
  cross-check must start with soft-core off in BLaDE too.
- Soft-core in OpenMM custom forces is possible for LJ but not for PME electrostatics without a
  plugin → planned as plugin stage S4 ([[FEAT-031 Soft-core|FEAT-031]]). Revisit after M5.

