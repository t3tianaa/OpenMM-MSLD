---
id: ADR-0035
type: adr
title: Gate plugin work
status: proposed
date: 2026-09-27
deciders: [Tetiana]
affects: ["[[Production plugin architecture]]", "[[Roadmap]]"]
requirements: ["[[REQ-029 Production performance on GPU|REQ-029]]", "[[REQ-070 Agree with BLaDE on a shared CHARMM system|REQ-070]]"]
retrospective: false
---
# ADR-0035 — Gate plugin work behind the θ-unit check and a BLaDE cross-check (proposed)

## Context
The plugin was motivated partly by "θ cannot reach 300 K with the FD engine". The audit found that
our θ mass may differ from BLaDE's effective mass by a large factor (units, [[ISS-002 Theta mass convention differs from BLaDE|ISS-002]]), which alone
could explain hot θ. And the partial-λ energy function has never been validated ([[ISS-012 No validation at partial lambda|ISS-012]]).

## Proposed decision
Start plugin S0 only after (a) [[TASK-032 Resolve BLaDE theta units|TASK-032]]/[[TASK-033 Rerun MDM2 with reference theta parameters|TASK-033]] settle θ units and show whether θ
thermalizes with reference-equivalent parameters, and (b) the first BLaDE fixed-λ cross-check
([[TASK-043 BLaDE fixed-lambda cross-check|TASK-043]]) or at least the NumPy oracle ([[FEAT-045 Independent partial-lambda oracle tests|FEAT-045]]) passes at partial λ.

## Consequences
- Months of C++ work are spent on a validated target.
- The plugin's motivation list may shrink to performance + NPT + analytic PME.


## Status of the gate (2026-10-31)
(a) θ units settled — [[ADR-0038 Theta units and default theta mass|ADR-0038]] accepted, θ thermalizes on MDM2 ([[EXP-011 MDM2 theta mass and friction screen|EXP-011]]). (b) The NumPy oracle
passes at partial λ ([[TASK-067 NumPy partial-lambda oracle tests|TASK-067]]). Both conditions are met; the BLaDE cross-check moves to the
plugin stage (Tetiana, 2026-10-31). Plugin S1 must reproduce `tests/data/oracle_toy.json`.
