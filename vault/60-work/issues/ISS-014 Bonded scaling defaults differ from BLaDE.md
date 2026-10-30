---
id: ISS-014
type: issue
title: Bonded scaling defaults differ from BLaDE
status: open
kind: divergence
severity: medium
confidence: source
source: "[[AUD-001 Engine audit of the local working copy|AUD-001]]"
affects: ["[[Bonded scaling module]]"]
requirements: ["[[REQ-004 Configurable bonded scaling per term type|REQ-004]]"]
fixed_by: ["[[TASK-057 BLaDE-style bonded scaling switches|TASK-057]]"]
found: 2026-09-26
updated: 2026-09-27
---
# ISS-014 — Bonded scaling defaults differ from BLaDE practice (audit F12)

Engine default scales bonds, angles, torsions, impropers; BLaDE examples remove bond, urey, angle
(and impr, sometimes dihe). The MDM2 script turns bond/angle off but still scales torsions and
impropers. Plan: [[ADR-0041 Default bonded scaling follows BLaDE practice|ADR-0041]].

