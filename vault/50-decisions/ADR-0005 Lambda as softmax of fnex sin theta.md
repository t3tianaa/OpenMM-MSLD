---
id: ADR-0005
type: adr
title: Lambda as softmax of fnex sin theta
status: accepted
date: 2026-07-27
deciders: [Tetiana]
affects: ["[[MSLD model component]]", "[[Lambda dynamics integrator component]]"]
requirements: ["[[REQ-002 Lambda from theta with implicit constraints|REQ-002]]"]
retrospective: true
---
# ADR-0005 — λ = softmax of fnex·sin θ

## Context
λ must stay on the simplex per site. Options in the literature: explicit constraints, the
Knight–Brooks fnex implicit constraint, BLaDE's newer piecewise/Newton constraint.

## Decision
Use the fnex softmax exactly as BLaDE's default (`λ_i = e^{fnex sin θ_i}/Σ e^{fnex sin θ_j}`,
fnex = 5.5), integrate θ ([[Implicit constraints and the softmax of sin theta]]).

## Consequences
- Constraints hold for free; chain rule is simple ([[Theta force by the chain rule]]).
- θ units/mass must match BLaDE's `ANGSTROM` convention to compare dynamics — not yet done
  ([[ADR-0038 Theta units and default theta mass|ADR-0038]]).
- The piecewise constraint is not supported.

