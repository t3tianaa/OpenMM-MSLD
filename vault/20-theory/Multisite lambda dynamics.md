---
title: Multisite lambda dynamics
type: theory
status: reviewed
related: ["[[Lambda dynamics]]", "[[Alchemical scaling rules in MSLD]]", "[[Free energies from lambda populations]]"]
sources: [Knight and Brooks 2011, Hayes et al 2017]
updated: 2026-09-27
---
# Multi-site λ-dynamics (MSλD / MSLD)

**In one sentence.** Several **sites** on a shared scaffold, each with several competing
**substituents**, each substituent with its own λ; the λ's at one site sum to 1, sites are
independent, so one simulation samples every combination.

## Structure: sites and blocks

```
  environment (site 0, block 0, λ ≡ 1): protein, water, ions, shared scaffold
  site 1:  block 1 (Cl)   block 2 (F)   block 3 (H)        λ1 + λ2 + λ3 = 1
  site 2:  block 4 (OH)   block 5 (NH2)                     λ4 + λ5 = 1
  → 3 × 2 = 6 molecules in ONE simulation
```

- A **site** is a position where alternatives are tried. A **block** is one alternative
  (substituent) = a set of atoms + one λ.
- Different sites are independent → combinatorial: N sites with n substituents each cover nᴺ
  molecules at the cost of Σ n blocks.

## The MSLD energy function

```
 U = U_0
   + Σ_s Σ_i  λ_si · ( U_0,si + U_si,si )                       (block with env, and within block)
   + Σ_s Σ_{t>s} Σ_i Σ_j  λ_si · λ_tj · U_si,tj                  (blocks at DIFFERENT sites)
   + U_bias(λ)
```

- `U_0` — environment–environment, never scaled.
- `λ_si U_0,si` — substituent i of site s with the environment.
- `λ_si U_si,si` — within the substituent (bonded + internal nonbonded). **Linear** in λ.
- `λ_si λ_tj U_si,tj` — between substituents at different sites.
- **No term** between two substituents of the same site: they are mutually exclusive
  alternatives that overlap in space.
- `U_bias` — biasing potential ([[Biasing potentials in MSLD]]).
- Constraint: `Σ_i λ_si = 1` for every site, `λ ≥ 0` → realised by θ
  ([[Implicit constraints and the softmax of sin theta]]).

How each force-field term maps onto this formula: [[Alchemical scaling rules in MSLD]].

## Free energies

A frame counts as molecule *l* when **every** site has its substituent's λ above a cutoff
(λ_c = 0.99 or 0.8). G of each molecule follows from the fraction of such frames minus the bias
([[Free energies from lambda populations]]). Raw λ-dynamics gets stuck in one corner, so biases
are **learned** first by ALF ([[Adaptive landscape flattening]]).

## Why it matters for us
This formula is the specification of our energy function ([[REQ-005 Nonbonded pair scaling rules|REQ-005]], [[REQ-006 Same-site pairs never interact|REQ-006]]). Every
scaling rule in [[Force scaling component]] must reproduce it term by term.

## Sources
- Knight, J. L.; Brooks, C. L. III. "Multisite λ Dynamics for Simulated Structure–Activity
  Relationship Studies." *J. Chem. Theory Comput.* 7, 2728 (2011).
- Knight, J. L.; Brooks, C. L. III. "Applying efficient implicit nongeometric constraints in
  alchemical free energy simulations." *J. Comput. Chem.* 32, 3423 (2011).
- Hayes, R. L.; Armacost, K. A.; Vilseck, J. Z.; Brooks, C. L. III. "Adaptive Landscape
  Flattening Accelerates Sampling of Alchemical Space in Multisite λ Dynamics."
  *J. Phys. Chem. B* 121, 3626 (2017).
- Hayes, R. L.; Buckner, J.; Brooks, C. L. III. "BLaDE: A Basic Lambda Dynamics Engine for GPU
  Accelerated Molecular Dynamics Free Energy Calculations." *J. Chem. Theory Comput.* 17, 6799 (2021).

