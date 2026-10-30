---
title: BLaDE charge restraints
type: reference
status: verified
system: blade
version: c677277
related: ["[[Net charge changes in alchemical calculations]]"]
updated: 2026-09-27
---
# BLaDE charge restraints

Source: `msld.h:94-105`, kernels `msld.cu:1400-1545`. All act on the λ-weighted net charge
`Q(λ) = Σ_b λ_b · lambdaCharge[b]`.

| constant | meaning (from code comments) |
|---|---|
| `kChargeRestraint1` | linear discrete-solvent correction, −(2π/3)·k_e·γ·N_H2O·q/V (doi:10.1063/1.4826261) |
| `kChargeRestraint2` | quadratic net-charge neutralizing-background term, −(π/2)k_e q²/(V β²) — on/off (doi:10.1021/acs.jctc.6b00552) |
| `kChargeRestraint3` | flat-bottom harmonic restraint on Q around q0 with half-width w |

Needed only for charge-changing perturbations ([[REQ-015 Charge-changing perturbations|REQ-015]]). Not implemented in our engine.

