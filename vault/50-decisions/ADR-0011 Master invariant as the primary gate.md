---
id: ADR-0011
type: adr
title: Master invariant as the primary gate
status: accepted
date: 2026-08-05
deciders: [Tetiana]
affects: ["[[Force scaling component]]", "[[Invariants]]"]
requirements: ["[[REQ-023 Lambda one reproduces the base system|REQ-023]]"]
retrospective: true
---
# ADR-0011 — Master invariant (λ = 1 ≡ base) as the primary correctness gate

## Decision
Every engine change must keep: all λ = 1 ⇒ the scaled System reproduces the base System's energy
and forces to machine precision (`test_master`). Design choices serve this: zero terms instead of
deleting them, same-site exclusions only in the engine ([[ADR-0016 Prep emits a plain System|ADR-0016]]), corrections that vanish at
λ = 1.

## Consequences
- Catches bookkeeping errors (lost terms, double counting) immediately.
- Says nothing about partial λ — it was over-trusted ([[ISS-012 No validation at partial lambda|ISS-012]]). Complemented by
  [[Partial-lambda oracle tests]] and [[BLaDE cross-validation harness]].

