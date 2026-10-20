---
id: REQ-020
type: requirement
title: Accurate dU/dlambda for every term
area: engine
priority: must
status: partial
derives_from: ["[[G-2 Physically correct MSLD|G-2]]", "[[G-4 Production performance|G-4]]"]
satisfied_by: ["[[FEAT-009 Tier-0 analytic dU-dlambda|FEAT-009]]", "[[FEAT-033 Analytic nonbonded plugin force|FEAT-033]]"]
verified_by: ["test_analytic_dudl", "[[EXP-008 Tier-0 derivative exactness|EXP-008]]"]
decisions: ["[[ADR-0013 Tier 0 analytic dU-dlambda via force groups|ADR-0013]]", "[[ADR-0026 Tier 2 plugin with scope S0 to S4|ADR-0026]]"]
created: 2026-08-10
updated: 2026-09-27
retrospective: true
---
# REQ-020 — Accurate dU/dλ for every term

**Statement.** ∂U/∂λ_b shall be computed analytically (or to a documented accuracy far below the
thermal noise) for every energy term, on every platform, in single precision too.

## Acceptance criteria
- [x] AC1 — bonded, LJ, within-block correction analytic ([[FEAT-009 Tier-0 analytic dU-dlambda|FEAT-009]]).
- [ ] AC2 — biases analytic ([[TASK-041 Analytic bias derivatives|TASK-041]]).
- [ ] AC3 — electrostatics (direct + PME + 1-4) analytic ([[FEAT-033 Analytic nonbonded plugin force|FEAT-033]]); FD noise on fp32 GPUs is
  estimated at hundreds of kJ/mol ([[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]).

