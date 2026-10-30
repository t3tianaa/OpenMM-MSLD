---
id: ISS-025
type: issue
title: NBFIX recovery assumes the OpenMM table convention
status: open
kind: risk
severity: low
confidence: source
affects: ["[[Ingest component]]"]
requirements: ["[[REQ-041 Lossless parameters including NBFIX|REQ-041]]"]
fixed_by: ["[[TASK-040 Audit the preparation layer|TASK-040]]"]
found: 2026-09-27
updated: 2026-09-27
---
# ISS-025 — `recover_charmm_lj` assumes OpenMM's A/B table convention

OpenMM `ForceField` writes `acoef = 4εσ¹²` with `acoef/r^12 − bcoef/r^6`; ParmEd `createSystem` writes
`a = √ε·Rmin⁶` with `(a/r6)^2 − b/r6` ([[ParmEd round trips and NBFIX loss]]). `recover_charmm_lj`
inverts A/B. Correct where used today (after OpenMM ForceField), but it would silently produce wrong
LJ on a ParmEd-built System. Fix: check the energy expression before inverting, raise otherwise.
