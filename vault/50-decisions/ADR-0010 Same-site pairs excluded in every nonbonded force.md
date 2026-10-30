---
id: ADR-0010
type: adr
title: Same-site pairs excluded in every nonbonded force
status: accepted
date: 2026-08-05
deciders: [Tetiana]
affects: ["[[Electrostatics scaling module]]", "[[Lennard-Jones scaling module]]"]
requirements: ["[[REQ-006 Same-site pairs never interact|REQ-006]]", "[[REQ-021 Runs on Reference, CPU, OpenCL, CUDA|REQ-021]]"]
retrospective: true
---
# ADR-0010 — Same-site pairs are exclusions in every nonbonded force

## Context
Different blocks of one site must never interact. In direct space the options are "exclude" or
"put in no interaction group". The optimized platforms require identical exclusions across all
nonbonded forces (found 2026-09-15).

## Decision
Add every same-site pair as a full exclusion to the `NonbondedForce`, and copy the same exclusions
into every MSLD `CustomNonbondedForce` (zero-energy there) so all exclusion sets are identical.

## Consequences
- Direct space: exact (0 at every λ). Runs on CPU/OpenCL/CUDA; `LocalEnergyMinimizer` works.
- Reciprocal space: OpenMM's exclusion correction **removes** the same-site cross-talk, unlike BLaDE's
  default which keeps it — a convention difference now reopened in [[ADR-0036 Same-site reciprocal-space convention|ADR-0036]].
- The exclusion lists grow as O(Σ n_b·n_c) per site (small for side chains).

