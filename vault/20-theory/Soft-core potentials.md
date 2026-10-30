---
title: Soft-core potentials
type: theory
status: reviewed
related: ["[[BLaDE nonbonded direct space]]", "[[Alchemical free energy basics]]"]
sources: [Beutler et al 1994, BLaDE nbdirect]
updated: 2026-09-27
---
# Soft-core potentials

**In one sentence.** Near λ → 0 a vanishing atom lets others overlap it; soft-core replaces the
distance r by a larger effective distance at small λ so energies and forces stay finite.

## The classic form (Beutler et al. 1994)

```
 E_LJ(λ, r) = λ · 4ε [ 1/(α(1−λ) + (r/σ)⁶)² − 1/(α(1−λ) + (r/σ)⁶) ]
```

## BLaDE's form (what we must match)

BLaDE uses one effective radius for both LJ and Coulomb in direct space (`nbdirect.cu:256-275`):

```
 s   = pair scale factor (λ_b, or λ_b·λ_c)
 r_s = R_soft · (1 − s)              R_soft = 4 Å = 0.4 nm (SOFTCORERADIUS, defines.h:48/74)
 if r < r_s:  x = r/r_s
              r_eff = r_s · ( ½ + x³ (1 − ½ x) )        (r_eff(0) = r_s/2, smooth at r = r_s)
 else         r_eff = r
 energy uses r_eff; force = dE/dr_eff · dr_eff/dr; the λ-force gets an extra dr_eff/ds term
```

- At s = 1 (fully present) r_s = 0 → no soft-core → the master invariant still holds.
- Applied only to pairs involving at least one alchemical atom. 1-4 soft-core is a separate switch
  (`softcore14`, usually off). Exclusion corrections never use soft-core.
- BLaDE examples use `msld softcore on` ([[BLaDE T4L and HSP90 examples]]).

## Why it matters
With U linear in λ, dU/dλ stays bounded even without soft-core — the MDM2 instability was not an
end-point singularity ([[EXP-007 MDM2 first end-to-end run and benchmark|EXP-007]]). Soft-core still matters: it keeps transient overlaps of a
barely present variant from producing huge forces and θ-forces, and it is part of the reference
energy function we must match ([[REQ-011 Soft-core for alchemical nonbonded|REQ-011]], [[ISS-013 Soft-core off while BLaDE examples use it|ISS-013]]).

## Sources
- Beutler, T. C. et al. *Chem. Phys. Lett.* 222, 529 (1994).
- Zacharias, M.; Straatsma, T. P.; McCammon, J. A. *J. Chem. Phys.* 100, 9025 (1994).

