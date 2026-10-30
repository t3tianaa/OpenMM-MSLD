---
id: REQ-070
type: requirement
title: Agree with BLaDE on a shared CHARMM system
area: validation
priority: must
status: proposed
derives_from: ["[[G-2 Physically correct MSLD|G-2]]", "[[UC-3 Validate the engine against BLaDE|UC-3]]"]
satisfied_by: ["[[FEAT-030 BLaDE cross-validation harness|FEAT-030]]"]
created: 2026-09-01
updated: 2026-09-27
retrospective: true
---
# REQ-070 — Agree with BLaDE on a shared CHARMM system

**Statement.** For a small CHARMM system with ≥ 2 sites (one with ≥ 3 blocks), at a grid of fixed
λ vectors including partial λ:
- every energy term (bonded, direct, reciprocal, self, exclusion, 1-4, biases, restraints) agrees
  with BLaDE to ≤ 1e-4 relative (double precision) or a justified tolerance;
- every ∂U/∂λ_b agrees likewise;
- differences due to documented conventions (same-site PME [[ADR-0036 Same-site reciprocal-space convention|ADR-0036]], switching functions)
  are quantified and explained.
Then short dynamics: λ histograms and ⟨∂U/∂λ⟩ agree within statistical error.

