---
id: EXP-004
type: experiment
title: User-set PME alpha
status: done
date: 2026-09-26
requirements: ["[[REQ-007 PME electrostatics at partial lambda|REQ-007]]"]
issues: ["[[ISS-008 PME alpha recomputed from the tolerance|ISS-008]]"]
related: ["[[AUD-001 Engine audit of the local working copy|AUD-001]]"]
---
# EXP-004 — User-set PME α (audit E4)

With `setPMEParameters(α, …)`, λ = 1 stays exact; partial λ differs slightly (toy: −59.674 vs −59.680
kJ/mol) because the correction force uses the tolerance-derived α.

