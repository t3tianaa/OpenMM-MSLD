---
id: ADR-0032
type: adr
title: Three subsystems preparation simulation analysis
status: accepted
date: 2026-09-27
deciders: [Tetiana]
affects: ["[[Architecture overview]]", "[[Preparation subsystem]]", "[[Simulation subsystem]]", "[[Analysis subsystem]]"]
requirements: ["[[REQ-049 Prep hands off a plain System and a model|REQ-049]]", "[[REQ-060 Free energy per variant with uncertainty|REQ-060]]"]
retrospective: false
---
# ADR-0032 — Three subsystems: preparation, simulation, analysis

## Context
The main goal ([[G-1 Free energies for many variants at once|G-1]]) is free energies for many variants. The owner specified (2026-09-26) that
the architecture should arise from that goal: a subsystem to prepare the system, one to run MSLD,
and one to analyse results (the last specified briefly for now).

## Decision
L1 architecture = Preparation · Simulation · Analysis, with explicit data contracts between them
([[HybridSystemBundle]], [[Lambda trajectory format]]). ALF flattening belongs to Simulation (it
drives the engine); free-energy estimation belongs to Analysis. Validation is cross-cutting.

## Consequences
- The existing code maps cleanly: `msld/prep/` = Preparation; `model/builder/forces/integrator/io/alf`
  = Simulation; analysis is almost empty ([[Analysis subsystem]]).
- `alf.estimate_ddg` belongs in Analysis long-term.

