---
id: ADR-0001
type: adr
title: Build MSLD natively in OpenMM
status: accepted
date: 2026-07-14
deciders: [Tetiana]
affects: ["[[Architecture overview]]", "[[Simulation subsystem]]"]
requirements: ["[[REQ-029 Production performance on GPU|REQ-029]]"]
retrospective: true
---
# ADR-0001 — Build MSLD natively in OpenMM

## Context
MSLD exists in CHARMM (BLOCK) and BLaDE, both CHARMM-only. The team works in the OpenMM ecosystem
and wants Amber force fields, Python scripting and GPU platforms. OpenMM has alchemical FEP/TI tools
but no λ-dynamics.

## Options
1. **Use BLaDE/CHARMM** for all MSLD work — proven, fast; but CHARMM inputs/FFs only, a separate
   ecosystem, no Amber.
2. **Wrap BLaDE** behind a Python front end — still CHARMM FFs only.
3. **Implement MSLD in OpenMM** from scratch, using BLaDE as the reference.

## Decision
Option 3: a native implementation in OpenMM, "from scratch", mirroring BLaDE's conventions.

## Consequences
- Access to Amber/OpenFF force fields and OpenMM's platforms and ecosystem.
- We must re-derive and validate every convention (large effort; see [[ADR-0002 BLaDE is the reference and validation oracle|ADR-0002]], [[REQ-070 Agree with BLaDE on a shared CHARMM system|REQ-070]]).
- Missing OpenMM capabilities (electrostatic dU/dλ, λ integrator) require workarounds or a plugin
  ([[ADR-0012 Python driver integrator instead of CustomIntegrator|ADR-0012]], [[ADR-0026 Tier 2 plugin with scope S0 to S4|ADR-0026]]).

