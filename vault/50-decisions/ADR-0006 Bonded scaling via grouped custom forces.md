---
id: ADR-0006
type: adr
title: Bonded scaling via grouped custom forces
status: accepted
date: 2026-07-31
deciders: [Tetiana]
affects: ["[[Bonded scaling module]]"]
requirements: ["[[REQ-003 Scale bonded terms by block lambdas|REQ-003]]"]
retrospective: true
---
# ADR-0006 — Bonded scaling by grouped custom forces

## Context
Built-in bonded forces have fixed formulas and cannot be multiplied by λ.

## Options
1. One custom force per term (too many forces). 2. One custom force with a per-term "scale
signature" parameter and λ lookup (complex expressions, no clean derivatives).
3. **Group terms by their λ signature; one custom force per signature with a constant λ prefactor.**

## Decision
Option 3. Move scaled terms out (zero their constant in the base force, keep the term), add them
to `Custom{Bond,Angle,Torsion}Force("lambda_b[*lambda_c]*<form>")`, register parameter derivatives.

## Consequences
- Exact analytic dU/dλ; λ = 1 ≡ base; few forces for few sites.
- Force count grows with the number of distinct signatures (fine so far).

