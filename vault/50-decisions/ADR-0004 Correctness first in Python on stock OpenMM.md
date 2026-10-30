---
id: ADR-0004
type: adr
title: Correctness first in Python on stock OpenMM
status: accepted
date: 2026-07-20
deciders: [Tetiana]
affects: ["[[Simulation subsystem]]", "[[Production plugin architecture]]"]
requirements: ["[[REQ-020 Accurate dU-dlambda for every term|REQ-020]]", "[[REQ-029 Production performance on GPU|REQ-029]]"]
retrospective: true
---
# ADR-0004 — Correctness first: a Python engine on stock OpenMM

## Context
A GPU plugin is months of C++/CUDA work; a wrong convention in it would be expensive to find. The
phase plan (old notes, "How BLaDE works") put validation gates before any plugin.

## Options
1. Write the plugin directly. 2. **Python engine on stock OpenMM (custom forces, parameter offsets,
Python integrator) first; plugin later, only where measured necessary.**

## Decision
Option 2 ("Tier 1"), with the plugin as "Tier 2" ([[ADR-0026 Tier 2 plugin with scope S0 to S4|ADR-0026]]).

## Consequences
- Fast iteration, runs on every platform, easy to test.
- Slow (Python loop, FD derivatives), NVT only — acceptable for a correctness tool, not production.
- Risk realised: the Python engine was declared "complete" before partial-λ validation
  ([[ISS-012 No validation at partial lambda|ISS-012]]). The phase gates must be enforced ([[ADR-0035 Gate plugin work|ADR-0035]]).

