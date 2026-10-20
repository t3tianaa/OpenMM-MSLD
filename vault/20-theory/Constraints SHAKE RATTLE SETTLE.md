---
title: Constraints SHAKE RATTLE SETTLE
type: theory
status: reviewed
updated: 2026-09-27
---
# Constraints: SHAKE, RATTLE, SETTLE

- **Holonomic constraint**: a rigid geometric condition g(x) = 0, usually a fixed bond length to
  hydrogen, or a rigid water.
- **SHAKE** (Ryckaert, Ciccotti, Berendsen 1977) iteratively corrects positions after a drift so
  every constraint holds again.
- **RATTLE** (Andersen 1983) also removes velocity components along the constraints.
- **SETTLE** (Miyamoto & Kollman 1992) solves rigid 3-site water analytically.

Why: freezing X–H stretches allows 2 fs time steps. In MSLD only atoms are constrained; θ never is
(its constraint Σλ = 1 is implicit in the softmax). OpenMM exposes `Context.applyConstraints` and
`applyVelocityConstraints`, which our Python driver calls ([[Lambda dynamics integrator component]]).

Zero-mass particles (virtual sites) are positioned from real atoms, not integrated — any integrator
must skip them ([[ISS-017 Zero-mass particles break the integrator|ISS-017]]).

