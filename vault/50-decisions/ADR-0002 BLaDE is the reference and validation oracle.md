---
id: ADR-0002
type: adr
title: BLaDE is the reference and validation oracle
status: accepted
date: 2026-07-14
deciders: [Tetiana]
affects: ["[[Simulation subsystem]]", "[[BLaDE cross-validation harness]]"]
requirements: ["[[REQ-070 Agree with BLaDE on a shared CHARMM system|REQ-070]]"]
retrospective: true
---
# ADR-0002 — BLaDE is the reference and validation oracle

## Context
MSLD has many conventions (within-block linear scaling, same-site exclusion, PME treatment, bias
forms, θ parametrization) that papers describe only partly. We need one authoritative source.

## Options
1. Papers only. 2. CHARMM BLOCK source. 3. **BLaDE source** (modern, compact, GPU, same author
group as ALF).

## Decision
BLaDE (github.com/RyanLeeHayes/BLaDE) is the specification: its code decides conventions; any
deliberate deviation needs an ADR. BLaDE runs on the same CHARMM system are the validation oracle.

## Consequences
- Reference notes must cite BLaDE file:line at a pinned commit ([[BLaDE overview]]).
- Validation needs a CUDA machine (BLaDE is CUDA-only) and CHARMM systems.
- BLaDE cannot validate the Amber path → [[REQ-071 Agree with FEP or TI on Amber|REQ-071]].
- Lesson (2026-09-26): read BLaDE's *code*, not feature names — the restraint and PME conventions
  were both misread ([[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]], [[ISS-006 Same-site PME differs from BLaDE and docs are backwards|ISS-006]]).

