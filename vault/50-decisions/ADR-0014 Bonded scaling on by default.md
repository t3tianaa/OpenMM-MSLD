---
id: ADR-0014
type: adr
title: Bonded scaling on by default
status: accepted
date: 2026-09-15
deciders: [Tetiana]
affects: ["[[Bonded scaling module]]", "[[MSLD model component]]"]
requirements: ["[[REQ-004 Configurable bonded scaling per term type|REQ-004]]"]
superseded_by: []
retrospective: true
---
# ADR-0014 — Bonded scaling on by default; production scripts turn bond/angle off

## Context
With bond/angle scaling on, switched-off side chains drifted away in the MDM2 run (2.8 → 4.8 Å
from CB). BLaDE practice is `removescaling bond angle …`.

## Decision (as built)
Keep the engine default `scale_bond = scale_angle = scale_torsion = True` so scaling-machinery
tests exercise them; production scripts (`mdm2_run.py`) set bond/angle off.

## Consequences
- A user who forgets the flags gets the drifting behaviour; BLaDE examples also leave impropers,
  UB (and often dihedrals) unscaled, which our flags cannot express separately ([[ISS-014 Bonded scaling defaults differ from BLaDE|ISS-014]]).
- To be superseded by [[ADR-0041 Default bonded scaling follows BLaDE practice|ADR-0041]] (proposed: a safe default) once that is accepted.
