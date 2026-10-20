---
id: ADR-0040
type: adr
title: Supported nonbonded methods
status: proposed
date: 2026-09-27
deciders: [Tetiana]
affects: ["[[Electrostatics scaling module]]"]
requirements: ["[[REQ-025 Supported nonbonded methods are correct|REQ-025]]"]
retrospective: false
---
# ADR-0040 — Supported nonbonded methods: PME and NoCutoff only (proposed)

## Context
The within-block correction is wrong for reaction-field cutoffs ([[ISS-003 Within-block correction wrong for cutoff methods|ISS-003]]). BLaDE supports only
PME. MSLD production is PME.

## Proposed decision
Support `PME` (and `Ewald` for tiny tests) and `NoCutoff` (for toys and oracles). Refuse
`CutoffPeriodic`, `CutoffNonPeriodic` and `LJPME` with a clear error. Revisit only if a use case
appears (then implement the reaction-field kernel).

