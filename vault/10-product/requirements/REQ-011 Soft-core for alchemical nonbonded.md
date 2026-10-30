---
id: REQ-011
type: requirement
title: Soft-core for alchemical nonbonded
area: engine
priority: should
status: deferred
derives_from: ["[[G-2 Physically correct MSLD|G-2]]", "[[G-4 Production performance|G-4]]"]
satisfied_by: ["[[FEAT-031 Soft-core|FEAT-031]]"]
decisions: ["[[ADR-0025 Soft-core off in the first version|ADR-0025]]"]
created: 2026-08-05
updated: 2026-09-27
retrospective: true
---
# REQ-011 — Soft-core for alchemical nonbonded

**Statement.** Optionally apply BLaDE's soft-core (effective distance
`r_eff = r_s·(½ + (r/r_s)³(1 − ½·r/r_s))` for `r < r_s = 0.4 nm·(1 − λ-factor)`, to both LJ and
Coulomb in direct space) with correct forces and dU/dλ ([[Soft-core potentials]],
[[BLaDE nonbonded direct space]]).

**Rationale.** BLaDE's examples run with `msld softcore on` ([[ISS-013 Soft-core off while BLaDE examples use it|ISS-013]]).

## Acceptance criteria
- [ ] AC1 — energy, forces and dU/dλ match BLaDE with soft-core on.
- [ ] AC2 — master invariant unchanged (soft-core vanishes at λ-factor = 1).

