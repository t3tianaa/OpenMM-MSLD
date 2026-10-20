---
id: ISS-007
type: issue
title: Dispersion correction removed for the whole system
status: open
kind: bug
severity: medium
confidence: confirmed
source: "[[AUD-001 Engine audit of the local working copy|AUD-001]]"
affects: ["[[Lennard-Jones scaling module]]"]
requirements: ["[[REQ-024 Dispersion correction preserved|REQ-024]]", "[[REQ-023 Lambda one reproduces the base system|REQ-023]]"]
fixed_by: ["[[TASK-036 Preserve env-env dispersion correction|TASK-036]]"]
found: 2026-09-26
updated: 2026-09-27
---
# ISS-007 — Dispersion correction silently removed for the whole system (audit F7)

`add_scaled_lj` calls `nbf.setUseDispersionCorrection(False)`, dropping the env–env correction too.
With it on in the input, λ = 1 no longer reproduces the base (toy: 290.1636 vs 290.1659 kJ/mol; in a
solvated box hundreds of kJ/mol, volume dependent → NPT density) ([[EXP-005 Dispersion correction on|EXP-005]]). The master test runs
with it off, so this was untested. Decision: [[ADR-0039 Dispersion correction handling|ADR-0039]].

