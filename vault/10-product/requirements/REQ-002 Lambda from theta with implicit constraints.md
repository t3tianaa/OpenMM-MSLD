---
id: REQ-002
type: requirement
title: Lambda from theta with implicit constraints
area: engine
priority: must
status: implemented
derives_from: ["[[G-2 Physically correct MSLD|G-2]]"]
satisfied_by: ["[[FEAT-001 MSLD data model|FEAT-001]]", "[[FEAT-008 Lambda-dynamics integrator|FEAT-008]]"]
verified_by: ["test_model", "test_integrator", "[[EXP-001 Theta samples the exact Boltzmann distribution on a toy|EXP-001]]"]
decisions: ["[[ADR-0005 Lambda as softmax of fnex sin theta|ADR-0005]]"]
created: 2026-07-27
updated: 2026-09-27
retrospective: true
---
# REQ-002 — λ from θ with implicit constraints

**Statement.** λ shall be computed per site as `λ_i = exp(fnex·sin θ_i) / Σ_j exp(fnex·sin θ_j)`
with `fnex` configurable (default 5.5), so that `λ ∈ (0,1)` and `Σ λ = 1` hold for any θ.

## Acceptance criteria
- [x] AC1 — identical formula to BLaDE `calc_lambda_from_theta_kernel` ([[BLaDE lambda from theta and theta force]]).
- [x] AC2 — θ-force from the chain rule matches finite differences (`test_integrator`).
- [ ] AC3 — θ angle convention (radians vs BLaDE's `θ·ANGSTROM`) documented and matched — open,
  see [[ISS-002 Theta mass convention differs from BLaDE|ISS-002]].

