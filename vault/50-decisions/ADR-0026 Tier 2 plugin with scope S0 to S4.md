---
id: ADR-0026
type: adr
title: Tier 2 plugin with scope S0 to S4
status: accepted
date: 2026-09-23
deciders: [Tetiana]
affects: ["[[Production plugin architecture]]"]
requirements: ["[[REQ-011 Soft-core for alchemical nonbonded|REQ-011]]", "[[REQ-019 NPT ensemble|REQ-019]]", "[[REQ-020 Accurate dU-dlambda for every term|REQ-020]]", "[[REQ-029 Production performance on GPU|REQ-029]]"]
retrospective: true
---
# ADR-0026 — Tier 2: a C++ OpenMM plugin, scope S0–S4

## Context
After Tier 0 the remaining gaps (electrostatic dU/dλ, hot θ, NPT, soft-core, speed) all live in the
nonbonded kernel and the integrator.

## Decision
One plugin with `MSLDNonbondedForce` (λ-scaled LJ + PME, analytic dU/dλ_b, soft-core) and
`MSLDIntegrator` (fused θ + atoms, a real Integrator → barostat works). Stages S0 skeleton, S1
Reference, S2 GPU, S3 integrator, S4 soft-core ([[Production plugin architecture]]).

## Consequences
- 4–7 months part-time (estimate). Bonded terms, prep and model stay in Python.
- Start is gated by [[ADR-0035 Gate plugin work|ADR-0035]] (proposed).

