---
title: Lennard-Jones, combining rules and NBFIX
type: theory
status: reviewed
related: ["[[Force field functional forms]]", "[[ParmEd round trips and NBFIX loss]]", "[[Lennard-Jones scaling module]]"]
updated: 2026-09-27
---
# Lennard-Jones, combining rules and NBFIX

```
 E_LJ = 4ε [ (σ/r)¹² − (σ/r)⁶ ]  =  A/r¹² − B/r⁶,     A = 4εσ¹², B = 4εσ⁶
 inverse:  σ = (A/B)^{1/6},   ε = B²/(4A)
```

- **Lorentz–Berthelot** combining rule: σ_ij = (σ_i + σ_j)/2, ε_ij = √(ε_i ε_j). Used by Amber and
  CHARMM. (OPLS uses geometric σ — our LJ expression hard-codes LB, so OPLS would be wrong.)
- CHARMM parameters are written as `Rmin/2` and a negative ε: σ = 2·(Rmin/2)/2^{1/6}.
- **NBFIX** (CHARMM): explicit (Rmin, ε) for specific atom-type pairs overriding the combining rule
  — famously ion–water and ion–carboxylate. Essential for ion behaviour.
- OpenMM representation: without NBFIX, LJ lives in `NonbondedForce` (per-particle σ, ε, LB).
  With NBFIX, OpenMM (and ParmEd's `createSystem`) moves all LJ to a `CustomNonbondedForce` with
  per-type-pair tables `acoef`/`bcoef` and zeroes ε in `NonbondedForce` ([[OpenMM CustomNonbondedForce]]).

Why it matters for MSLD: `NonbondedForce` cannot express a λ_i λ_j product on ε (scaling ε by λ
would give √(λ_i λ_j) through the combining rule) → alchemical LJ must go to
`CustomNonbondedForce` ([[ADR-0008 LJ scaled by grouped CustomNonbondedForces|ADR-0008]]).

