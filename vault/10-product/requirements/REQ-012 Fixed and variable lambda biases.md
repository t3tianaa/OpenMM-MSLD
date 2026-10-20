---
id: REQ-012
type: requirement
title: Fixed and variable lambda biases
area: engine
priority: must
status: implemented
derives_from: ["[[G-1 Free energies for many variants at once|G-1]]", "[[G-2 Physically correct MSLD|G-2]]"]
satisfied_by: ["[[FEAT-006 Lambda biases|FEAT-006]]"]
verified_by: ["test_biases", "test_alf"]
decisions: ["[[ADR-0024 Home-grown ALF heuristic|ADR-0024]]"]
created: 2026-08-10
updated: 2026-09-27
retrospective: true
---
# REQ-012 — Fixed and variable λ biases

**Statement.** The engine shall support a fixed linear bias `Σ b_i λ_i` and pairwise variable
biases of BLaDE types 6 (`k λ_i λ_j`), 8 (`k λ_i λ_j/(λ_i + l0)`) and 10 (`k λ_j (1 − e^{l0 λ_i})`),
with coefficients changeable at run time ([[Biasing potentials in MSLD]]).

## Acceptance criteria
- [x] AC1 — formulas identical to BLaDE `getforce_variableBias_kernel` ([[BLaDE biases and theta biases]]).
- [x] AC2 — coefficients are Context parameters (live update for ALF).
- [ ] AC3 — analytic dU/dλ (today finite difference, [[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]).
- [ ] AC4 — other BLaDE types (1–5, 7, 9, 11, 12) if needed — could.

