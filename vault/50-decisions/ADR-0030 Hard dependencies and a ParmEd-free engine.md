---
id: ADR-0030
type: adr
title: Hard dependencies and a ParmEd-free engine
status: accepted
date: 2026-08-21
deciders: [Tetiana]
affects: ["[[Simulation subsystem]]", "[[Preparation subsystem]]"]
requirements: ["[[REQ-074 Engine free of prep dependencies|REQ-074]]"]
retrospective: true
---
# ADR-0030 — Hard dependencies; the engine stays ParmEd-free

## Decision
- A package the code needs is added to `env/environment.yml` and installed; no "optional import
  with install hint" fallbacks (they hide bugs in untested paths — RDKit's did).
- Lazy imports allowed only for start-up speed (openff/openmmforcefields, ~1.5 s).
- Engine modules import only openmm + numpy; `msld.prep` may import ParmEd, RDKit, SciPy.

## Consequences
- Running MSLD on an existing System needs only OpenMM.
- The env is the single source of dependency truth ([[Dependencies]]).

