---
title: Langevin dynamics and BAOAB splitting
type: theory
status: reviewed
related: ["[[Lambda dynamics integrator component]]", "[[BLaDE integrator and update loop]]"]
updated: 2026-09-27
---
# Langevin dynamics and BAOAB (VRORV) splitting

**In one sentence.** Newton's equations plus friction and random kicks keep every degree of freedom
at temperature T; splitting the update into kick / drift / thermostat pieces gives an accurate,
simple integrator.

## Equation of motion (any coordinate q: an atom's x, or a θ)

```
   m q̈ = F(q) − m γ q̇ + √(2 m γ k_B T) · η(t)        F = −∂U/∂q,  η = white noise
```

force + drag + thermal kicks. Friction and noise are balanced so the temperature is T.

## The splitting

```
 V (B): v ← v + (dt/2)·F/m            half kick
 R (A): q ← q + (dt/2)·v              half drift
 O    : v ← a·v + √((1 − a²) kT/m)·ξ   exact Ornstein–Uhlenbeck step, a = e^{−γ dt}, ξ ~ N(0,1)
 R (A): q ← q + (dt/2)·v
 V (B): v ← v + (dt/2)·F/m            (force re-evaluated after the second R)

 one step = V R O R V   (= BAOAB)
```

BAOAB has very small configurational-sampling error for a given dt (Leimkuhler & Matthews), which
is why BLaDE and OpenMM's `LangevinMiddleIntegrator` use it.

## For MSLD
- θ uses the same scheme, glued to the atom array, with **its own mass and friction** (per block).
- Constraints (SHAKE/RATTLE) act after each R and V on atoms only; θ is never constrained.
- **Timescale mismatch**: if the θ "spring constant" (curvature of U in θ, ∝ (∂²U/∂θ²)) is large and
  the θ mass small, the θ oscillation period approaches dt → integration error heats θ. The cure is
  a heavier θ, a smaller dt, a multiple-time-step for θ, or smaller forces (soft-core, biases).
  This is the mechanism behind "hot θ" ([[ISS-018 Theta runs hot in MDM2|ISS-018]], [[BLaDE units and theta mass]]).

## Sources
- Leimkuhler, B.; Matthews, C. *J. Chem. Phys.* 138, 174102 (2013) — BAOAB.
- Sivak, D. A.; Chodera, J. D.; Crooks, G. E. *J. Phys. Chem. B* 118, 6466 (2014),
  doi:10.1021/jp411770f — VRORV naming; cited in BLaDE `update.cu:245`.
- Leimkuhler, B.; Matthews, C. *Proc. R. Soc. A* 472, 20160138 (2016) — gBAOAB with constraints.

