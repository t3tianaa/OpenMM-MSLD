---
id: ADR-0013
type: adr
title: Tier 0 analytic dU/dlambda via force groups
status: accepted
date: 2026-09-17
deciders: [Tetiana]
affects: ["[[Force groups and derivative routing]]"]
requirements: ["[[REQ-020 Accurate dU-dlambda for every term|REQ-020]]"]
retrospective: true
---
# ADR-0013 — Tier 0: analytic dU/dλ via force groups; FD only the remainder

## Context
Originally the whole energy was finite-differenced: 2·n_blocks + 1 full evaluations per step.
Most forces already expose analytic derivatives.

## Decision
Put every force with parameter derivatives in group 1; leave everything else in group 0; get
analytic derivatives from the same `getState` as the forces; finite-difference **only group 0**
(electrostatics, biases, anything injected — so nothing λ-dependent is dropped).

## Consequences
- 1 full evaluation per step instead of 2·n_b + 1; exact vs old FD (~5e-9, [[EXP-008 Tier-0 derivative exactness|EXP-008]]).
- Group 0 still contains the full NonbondedForce with PME → FD cost and fp32 noise remain
  ([[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]).
- Did **not** fix hot θ ([[ISS-018 Theta runs hot in MDM2|ISS-018]]).

