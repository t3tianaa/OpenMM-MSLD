---
id: ISS-008
type: issue
title: PME alpha recomputed from the tolerance
status: open
kind: bug
severity: low
confidence: confirmed
source: "[[AUD-001 Engine audit of the local working copy|AUD-001]]"
affects: ["[[Electrostatics scaling module]]"]
requirements: ["[[REQ-007 PME electrostatics at partial lambda|REQ-007]]"]
fixed_by: ["[[TASK-037 Read PME alpha from the force|TASK-037]]"]
found: 2026-09-26
updated: 2026-09-27
---
# ISS-008 — PME α recomputed from the tolerance (audit F8)

The within-block correction derives α from `getEwaldErrorTolerance()` and ignores
`setPMEParameters`. With a user-set α, λ = 1 is still exact but partial-λ energies are off (toy:
−59.674 vs −59.680 kJ/mol) ([[EXP-004 User-set PME alpha|EXP-004]]). Fix: read `getPMEParameters()` / `getPMEParametersInContext`.

