---
id: ADR-0008
type: adr
title: LJ scaled by grouped CustomNonbondedForces
status: accepted
date: 2026-08-05
deciders: [Tetiana]
affects: ["[[Lennard-Jones scaling module]]"]
requirements: ["[[REQ-005 Nonbonded pair scaling rules|REQ-005]]", "[[REQ-008 LJ scaling including NBFIX|REQ-008]]"]
retrospective: true
---
# ADR-0008 — LJ scaled by grouped `CustomNonbondedForce`s

## Context
LJ pairs need factors λ_b or λ_bλ_c; ε offsets in `NonbondedForce` combine as √(λ_iλ_j).

## Options
1. **One CustomNonbondedForce per scaling category with interaction groups** — exact `deriv()`,
   simple. 2. One force with a per-particle block id and a `Discrete2DFunction` of λ factors
   (scales to many sites; tables must be updated every step or expressed via globals).

## Decision
Option 1 now; option 2 as the fallback when many sites make the force count a problem (old notes:
"measure early, keep the Discrete1DFunction table as fallback").

## Consequences
- Analytic LJ dU/dλ; LB combining rule hard-coded (fine for Amber/CHARMM, wrong for OPLS).
- CHARMM NBFIX needs a separate path copying the tabulated force.
- Each new force must carry the full exclusion set ([[OpenMM exclusion parity across nonbonded forces]]).

