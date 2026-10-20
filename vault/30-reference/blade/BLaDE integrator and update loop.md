---
title: BLaDE integrator and update loop
type: reference
status: verified
system: blade
version: c677277
related: ["[[Langevin dynamics and BAOAB splitting]]", "[[Lambda dynamics integrator component]]"]
updated: 2026-09-27
---
# BLaDE integrator and update loop

Source: `src/update/update.cu:39-305`, `src/system/state.h:24-60`, `state.cxx:152, 289-297`.

- **One array, one integrator.** Spatial DOFs occupy `[0, N1)`, θ DOFs `[N1, N)` of the same
  `LeapState` arrays (position, velocity, force, `ism = 1/√m`, random). θ moves on the same clock
  as atoms (`state.cxx:152`).
- **VRORV** (Sivak, Chodera & Crooks 2014, cited at `update.cu:244`), with two optimisations:
  1. the closing V of one step and the opening V of the next are merged (`update_VV…`) — both use
     the same force;
  2. on energy-output steps they are split so the kinetic energy is measured on-step
     (`update.cu:251-262`).
- Order in `State::update` (`update.cu:233-305`): MC barostat (if due) → θ force from λ force →
  V(V) + backup positions + R → SHAKE → O + R → SHAKE → λ from θ.
- **θ-aware details:** separate friction for θ (`lambdaLeapParms2`); fixed θ via mass 0
  (non-finite `ism` → skipped by every kernel, `isfinite(ism)` guards); θ never constrained.
- **Sign:** BLaDE's force array holds +∂U/∂x, so the kick is `v -= ½dt·ism²·f`. OpenMM uses
  −∂U/∂x: flip when porting.

Figures from the original study notes (state struct, parameters, O kernel, step order):

![[Pasted image 20260718000908.png|600]]
![[Pasted image 20260718001029.png|350]]
![[Pasted image 20260721131555.png|700]]
![[Pasted image 20260721140115.png]]
![[Pasted image 20260721140314.png|600]]
![[Pasted image 20260721140953.png]]
![[Pasted image 20260721142601.png]]
![[Pasted image 20260721143225.png|600]]

