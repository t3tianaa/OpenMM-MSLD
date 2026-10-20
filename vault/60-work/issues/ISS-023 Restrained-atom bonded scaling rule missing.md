---
id: ISS-023
type: issue
title: Restrained-atom bonded scaling rule missing
status: open
kind: divergence
severity: low
confidence: source
affects: ["[[Bonded scaling module]]"]
requirements: ["[[REQ-004 Configurable bonded scaling per term type|REQ-004]]"]
fixed_by: ["[[TASK-057 BLaDE-style bonded scaling switches|TASK-057]]"]
found: 2026-09-27
updated: 2026-09-27
---
# ISS-023 — BLaDE keeps bonded terms of restrained atoms scaled; we do not

In BLaDE `bonded_scaling` (`msld.cu:509-555`), a term type under `removescaling` is still λ-scaled if
all of its same-block atoms are restrained atoms. Matters once equivalent-atom restraints exist for
duplicated backbones ([[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]]). Found while writing [[BLaDE bonded term scaling]].

