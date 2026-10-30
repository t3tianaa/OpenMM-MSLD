---
title: PME with lambda-scaled charges
type: theory
status: reviewed
related: ["[[Ewald summation and PME]]", "[[Alchemical scaling rules in MSLD]]", "[[BLaDE PME reciprocal space and exclusions]]", "[[Electrostatics scaling module]]"]
updated: 2026-09-27
---
# PME with λ-scaled charges

**In one sentence.** MSLD puts charges `q̂_i = λ_b(i) q_i` on the PME grid; this is exact for
env–block and cross-site pairs but gives within-block pairs λ² and same-site pairs λ_b λ_c, which
must be handled by convention.

## What each pair gets from the grid

```
 E_recip(λ) = ½ Σ_ij λ_i λ_j q_i q_j A_ij

 pair type            MSLD wants    grid gives     defect
 env–env              1             1              —
 env–block b          λ_b           λ_b            —
 block b–block c      λ_b λ_c       λ_b λ_c        —      (different sites)
 within block b       λ_b           λ_b²           λ_b − λ_b²
 same site, b ≠ c     0             λ_b λ_c        spurious; A_ij is LARGE (atoms overlap)
 self (i = i)         —             λ_b² (self term scales as λ²)
```

The last row is "the PME problem": two overlapping alternatives interact through the grid, and
because their atoms nearly coincide, A_ij ≈ 2α/√π is large — a short-range artefact, not a small
far-field leak.

## The conventions (BLaDE `msldEwaldType`, [[BLaDE PME reciprocal space and exclusions]])

The exclusion-correction term (which subtracts `λ_i λ_j q_i q_j erf(αr)/r` for listed pairs) is the
place where conventions differ:

| type | name | within-block excluded pairs (1-2, 1-3) | same-site cross-block pairs |
|---|---|---|---|
| 1 | "on" | corrected with **one** λ | not in the correction → reciprocal cross-talk λ_bλ_c remains |
| **2 (default)** | "ex" | corrected with λ² (consistent with the grid) | not corrected → cross-talk remains |
| 3 | "nn" | corrected with λ_i λ_j always | corrected → cross-talk removed |

Direct space is separate: BLaDE's direct kernel uses **λ_b** for within-block pairs (linear) and 0
for same-site pairs. So BLaDE's default is: within-block **real space λ, reciprocal λ²**; same-site
**real space 0, reciprocal λ_bλ_c**.

## What OpenMM does with charge offsets
OpenMM `NonbondedForce` with charge offsets scales charges on the grid; exclusions remove their
reciprocal contribution exactly (exclusion correction with the *current* charges). Our engine
excludes same-site pairs → their reciprocal cross-talk is **removed** (like BLaDE type 3 for those
pairs), while BLaDE's default keeps it. Within-block real space is corrected to λ by an extra force.
See [[ISS-006 Same-site PME differs from BLaDE and docs are backwards|ISS-006]], [[ADR-0009 Within-block real-space electrostatics linear|ADR-0009]], [[ADR-0036 Same-site reciprocal-space convention|ADR-0036]].

## ∂E/∂λ_b in reciprocal space

```
 E_recip = ½ Σ_i q̂_i φ_i,        φ_i = Σ_j q̂_j A_ij   (potential at atom i from the λ-scaled grid)
 ∂E_recip/∂λ_b = Σ_{i∈b} q_i φ_i                     (one gather gives every block's derivative)
 ∂E_self/∂λ_b  = −2 (α/√π) k λ_b Σ_{i∈b} q_i²
```

BLaDE accumulates exactly this during the gather step (`nbrecip.cu:451`) and in the self kernel
(`nbrecip.cu:45`). One reciprocal pass gives all λ derivatives — the basis of the planned plugin
([[Production plugin architecture]]).

