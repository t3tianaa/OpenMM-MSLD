---
title: BLaDE nonbonded direct space
type: reference
status: verified
system: blade
version: c677277
related: ["[[Alchemical scaling rules in MSLD]]", "[[Soft-core potentials]]", "[[Lennard-Jones scaling module]]", "[[Electrostatics scaling module]]"]
updated: 2026-09-27
---
# BLaDE nonbonded direct space

Source: `src/nbdirect/nbdirect.cu` (`getforce_nbdirect_kernel`, lines 83-490). **Verified.**

## λ factor per pair (`nbdirect.cu:244-253`)

```cpp
if (same SITE) {                 // bi, bj encode (site<<16 | block)
  if (same BLOCK) lixlj = λ_i;   // within block: LINEAR
  else            lixlj = 0;     // same site, different block: no interaction
} else            lixlj = λ_i·λ_j;   // different sites (env has λ ≡ 1)
fij *= lixlj;                    // both electrostatics (real-space erfc) and vdW
```

![[Pasted image 20260723124956.png|600]]

## λ force (`nbdirect.cu:399-417`)
For a pair with energy e: same block → `∂U/∂λ_i += e`; different sites → `∂U/∂λ_i += λ_j e`,
`∂U/∂λ_j += λ_i e`. With soft-core the energy term gains `f·∂r_eff/∂s`.

## Soft-core (`nbdirect.cu:256-275`)
`r_s = SOFTCORERADIUS·(1 − lixlj)`; if `r < r_s`, `r_eff = r_s(½ + x³(1 − x/2))`, `x = r/r_s`;
applies to electrostatics and vdW together when at least one atom is alchemical
([[Soft-core potentials]]).

## Functional forms
- electrostatics: PME real space `k q_i q_j erfc(βr)/r` (other methods in code: a switched form);
- vdW: CHARMM **force switching** (vfswitch) between `rswitch` and `rcut`.

## Where we match / differ
Our LJ and real-space Coulomb reproduce the λ factors exactly (within-block linear via a correction
force, [[ADR-0009 Within-block real-space electrostatics linear|ADR-0009]]). We do not have soft-core ([[ISS-013 Soft-core off while BLaDE examples use it|ISS-013]]) and use OpenMM's potential switching,
not vfswitch ([[TASK-070 CHARMM force switching for the cross-check|TASK-070]]).

