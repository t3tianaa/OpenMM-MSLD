---
id: REQ-030
type: requirement
title: Adaptive landscape flattening
area: run
priority: must
status: partial
derives_from: ["[[G-1 Free energies for many variants at once|G-1]]", "[[G-5 Meaningful analysis|G-5]]"]
satisfied_by: ["[[FEAT-012 ALF flattening heuristic|FEAT-012]]", "[[FEAT-035 Standard ALF|FEAT-035]]"]
verified_by: ["test_alf", "[[EXP-009 Heuristic ALF on toys|EXP-009]]"]
decisions: ["[[ADR-0024 Home-grown ALF heuristic|ADR-0024]]", "[[ADR-0034 Adopt published ALF and two-leg ddG|ADR-0034]]"]
created: 2026-09-16
updated: 2026-09-27
retrospective: true
---
# REQ-030 — Adaptive landscape flattening

**Statement.** Provide the published ALF procedure: iterate short simulations, histogram λ, fit the
fixed (b), quadratic (c, type 6), skew (x, type 10, l0 = −5.56) and end-point (s, type 8,
l0 = 0.017) coefficients by likelihood maximization, until the landscape is flat
([[Adaptive landscape flattening]]).

## Acceptance criteria
- [x] AC1 — bias coefficients can be tuned live.
- [ ] AC2 — the standard ALF fit (not the home-grown heuristic, [[ISS-011 ALF is a heuristic and ddG is single-leg|ISS-011]]).
- [ ] AC3 — reproduces ALF-converged biases for a BLaDE example within noise.

