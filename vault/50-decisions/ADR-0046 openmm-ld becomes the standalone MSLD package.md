---
id: ADR-0046
type: adr
title: openmm-ld becomes the standalone MSLD package
status: accepted
date: 2026-11-09
deciders: [Tetiana]
affects: ["[[Production plugin architecture]]"]
requirements: ["[[REQ-029 Production performance on GPU|REQ-029]]"]
supersedes: []
superseded_by: []
retrospective: false
---
# ADR-0046 — openmm-ld becomes the standalone MSLD package

## Context
[[ADR-0026 Tier 2 plugin with scope S0 to S4|ADR-0026]] and [[Production plugin architecture]] kept prep and
`MSLDModel` in Python in this repository, with the plugin as a component used by the engine here. After
`use_plugin` the plugin's force runs only through this engine: `msld/integrator.py`, `model.py`,
`forces.py`, `alf.py`, `io.py` and `prep/` are all still here. Tetiana wants one tool that covers everything
from system preparation to production, without this repository.

Python itself is not the obstacle: prep depends on ParmEd, RDKit and OpenMM's force-field loader, and a C++
rewrite would bring no scientific gain.

## Decision
One package, [t3tianaa/openmm-ld](https://github.com/t3tianaa/openmm-ld): a C++ core (forces and integrator) plus
a Python layer inside it for the λ model, bonded/bias/restraint setup, ALF, output, prep and a command line.
This repository becomes the reference implementation while the port runs, and then retires.

This replaces only the "prep and model stay in Python *here*" part of ADR-0026. Its force and integrator
scope stands, and bonded terms stay stock OpenMM custom forces.

## Rules
- A module retires here only after its port in openmm-ld is checked against it on the same inputs.
- Matching this engine is not validation of the physics: the energy spec was written from this engine.
  Independent checks (Ewald sum, BLaDE) stay required.

## Consequences
- Work order: S2 GPU and S3 `MSLDIntegrator` in C++; P1 Python layer (model, forces, ALF, io); P2 prep; P3 command
  line ([[Production plugin architecture]]). The order of S2 and S3 relative to P1–P3 is not fixed by this ADR.
- `use_plugin` (`msld/plugin.py`) is a bridge for comparing the two during the port, not the final design.
- New engine features should go to openmm-ld once their module is ported, so the two do not diverge.
