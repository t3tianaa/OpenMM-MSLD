---
id: ADR-0034
type: adr
title: Adopt published ALF and two-leg ddG
status: proposed
date: 2026-09-27
deciders: [Tetiana]
affects: ["[[ALF flattening component]]", "[[Free energy estimation component]]"]
requirements: ["[[REQ-030 Adaptive landscape flattening|REQ-030]]", "[[REQ-060 Free energy per variant with uncertainty|REQ-060]]", "[[REQ-061 Relative ddG from two legs|REQ-061]]"]
supersedes: ["[[ADR-0024 Home-grown ALF heuristic|ADR-0024]]"]
retrospective: false
---
# ADR-0034 — Adopt the published ALF and a two-leg ΔΔG analysis (proposed)

## Options
1. Keep and extend the heuristic. 2. **Re-implement ALF's algorithm in our code** (b, c, x, s;
histogram likelihood update; schedule) with ALF as the reference. 3. **Drive the official ALF
package** with our engine as the MD backend (write BLaDE-compatible λ files, read its bias
variables).

## Proposed decision
Study ALF first ([[TASK-074 Study the ALF package|TASK-074]]); prefer option 3 if its interfaces allow (least new code, exact
algorithm), else option 2 validated against ALF on the same λ data. Free energies: ALF's production
estimator + our two-leg cycle ([[REQ-061 Relative ddG from two legs|REQ-061]]).

## Evidence still needed
ALF source layout, its dependencies on CHARMM/BLaDE file formats, licence.

