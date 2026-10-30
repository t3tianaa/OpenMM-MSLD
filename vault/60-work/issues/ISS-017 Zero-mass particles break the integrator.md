---
id: ISS-017
type: issue
title: Zero-mass particles break the integrator
status: open
kind: bug
severity: medium
confidence: inferred
source: "[[AUD-001 Engine audit of the local working copy|AUD-001]]"
affects: ["[[Lambda dynamics integrator component]]"]
requirements: ["[[REQ-018 Holonomic constraints and virtual sites|REQ-018]]"]
fixed_by: ["[[TASK-039 Handle zero-mass particles in the integrator|TASK-039]]"]
found: 2026-09-26
updated: 2026-09-27
---
# ISS-017 — Zero-mass particles (virtual sites) divide by zero in the integrator (audit F12)

`LambdaDynamics` computes `sqrt(kT/m)` and `F/m` for every particle; virtual sites (TIP4P, OPC)
have m = 0. Needed for ff19SB + OPC. Fix: skip zero-mass particles in B/O steps and let
`context.computeVirtualSites()` / constraints place them.

