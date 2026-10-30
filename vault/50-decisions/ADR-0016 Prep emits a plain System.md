---
id: ADR-0016
type: adr
title: Prep emits a plain System
status: accepted
date: 2026-08-18
deciders: [Tetiana]
affects: ["[[Plain System builder]]", "[[Force scaling component]]"]
requirements: ["[[REQ-049 Prep hands off a plain System and a model|REQ-049]]", "[[REQ-023 Lambda one reproduces the base system|REQ-023]]"]
retrospective: true
---
# ADR-0016 — Prep emits a plain System; the engine applies every MSLD change

## Decision
The System from prep has correct parameters but no λ scaling and **no same-site exclusions**; the
engine (`scale_msld_system`) adds exclusions, offsets, custom forces, biases and restraints.

## Why
- The master invariant (λ = 1 ≡ base) needs an untouched base System to compare against.
- The engine can then be applied to any OpenMM System, not only prep's output.

## Consequences
- Minimizing or simulating the plain System directly would make overlapping variants clash — always
  scale first (documented in `LambdaDynamics.minimize`).

