---
title: BLaDE PME reciprocal space and exclusions
type: reference
status: verified
system: blade
version: c677277
related: ["[[PME with lambda-scaled charges]]", "[[Electrostatics scaling module]]"]
updated: 2026-09-27
---
# BLaDE PME: reciprocal space, self term and exclusions

Sources: `src/nbrecip/nbrecip.cu`, `src/bonded/pair.cu`, `Msld::nbex_scaling` (`msld.cu:623-668`).

## Reciprocal space
1. **Spread** (`getforce_ewald_spread_kernel`, `nbrecip.cu:83-217`): each charge is multiplied by
   its block's λ before B-spline spreading: `q̂ = λ_b q`.
2. **Convolution** (`nbrecip.cu:221-260`) with the Ewald kernel after FFT.
3. **Gather** (`getforce_ewald_gather_kernel`, `nbrecip.cu:263-480`): atom forces scaled by
   `λ_b q`, and the λ force `lambdaForce[b] += 2·q·(energy share)` (`nbrecip.cu:451`) = Σ_{i∈b}
   q_i φ_i.
4. **Self** (`getforce_ewaldself_kernel`, `nbrecip.cu:19-54`): `E = −(β/√π)k Σ (λ_b q_i)²`,
   `∂E/∂λ_b = 2λ_b·(per-atom self energy / λ²)` (line 45).

Figures from the original notes (PME pipeline and pair classification):
![[Pasted image 20260723131026.png|600]]
![[Pasted image 20260723134417.png|600]]

## Exclusion correction — `msldEwaldType` (`msld.cu:623-668`)
Excluded pairs (1-2, 1-3, and 1-4 real-space remainder) get a `−k q_i q_j erf(βr)/r` correction
computed in `pair.cu` (`getforce_nbexT`, lines 356-380), scaled by the λ's of the two blocks after
`nbex_scaling` has possibly changed them:

| type | same block | same site, different blocks |
|---|---|---|
| 1 "on" | second block set to 0 → factor **λ_b** | not included (no correction) |
| **2 "ex" (default)** | factor **λ_b²** (consistent with the grid) | not included |
| 3 "nn" | λ_b² | included → factor λ_b λ_c |

"Not included" means the pair's reciprocal interaction (which the grid always contains) is left
in. So in BLaDE's default, **same-site alternatives keep a reciprocal-space cross-talk
λ_b λ_c q q erf(βr)/r**. Note that only *excluded* pairs appear in this list; same-site pairs that are
not bonded neighbours are not in the exclusion list at all in BLaDE — they are removed from direct
space by the pair rule, and their reciprocal part is simply kept.

The code comment says "2=normal scaling squared self interactions"; the CHARMM keyword equivalent is
`pmel ex` (comment in `test/HSP90/cb7.inp`).

## Consequence for the cross-check
OpenMM excludes our same-site pairs, so the exclusion correction removes their reciprocal term:
our energy differs from BLaDE default by exactly Σ_same-site λ_bλ_c q q erf(βr)/r. Either account
for it analytically, run BLaDE with `msld ewaldtype 3`, or match BLaDE ([[ADR-0036 Same-site reciprocal-space convention|ADR-0036]], [[ISS-006 Same-site PME differs from BLaDE and docs are backwards|ISS-006]]).

