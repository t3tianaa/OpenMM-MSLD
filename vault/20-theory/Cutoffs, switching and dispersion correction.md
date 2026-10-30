---
title: Cutoffs, switching and dispersion correction
type: theory
status: reviewed
related: ["[[Lennard-Jones, combining rules and NBFIX]]", "[[OpenMM NonbondedForce]]"]
updated: 2026-09-27
---
# Cutoffs, switching and dispersion correction

- **Cutoff** r_c (≈ 1.0–1.2 nm): LJ beyond r_c is ignored.
- **Potential switching** (OpenMM `setUseSwitchingFunction`): multiply E by a smooth S(r) from
  r_switch to r_c. Changes both energy and force shape.
- **Force switching** (CHARMM `vfswitch`, BLaDE's only vdW method): modify the *force* smoothly to
  zero; the energy is shifted accordingly. Different functional form from potential switching →
  energies differ at the 0.1–1 kJ/mol level per system; matters for exact BLaDE comparison
  ([[TASK-070 CHARMM force switching for the cross-check|TASK-070]]).
- **Long-range dispersion correction**: adds the average LJ energy beyond r_c assuming uniform
  density, `E_disp ∝ N²/V · ⟨B⟩/r_c³` (with switching corrections). Volume dependent → matters for
  NPT density. In OpenMM, `NonbondedForce.setUseDispersionCorrection` (default on for PME) and
  `CustomNonbondedForce.setUseLongRangeCorrection` (computed numerically over particle classes).

MSLD question: the correction depends on the *composition*, which depends on λ. Options: keep it
for env–env only, include blocks with λ-weights, or compute at λ = 1 for one reference state. Our
engine currently turns it off for the whole system ([[ISS-007 Dispersion correction removed for the whole system|ISS-007]]); the choice is [[ADR-0039 Dispersion correction handling|ADR-0039]].

