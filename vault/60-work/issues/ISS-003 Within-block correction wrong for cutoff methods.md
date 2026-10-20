---
id: ISS-003
type: issue
title: Within-block correction wrong for cutoff methods
status: open
kind: bug
severity: medium
confidence: confirmed
source: "[[AUD-001 Engine audit of the local working copy|AUD-001]]"
affects: ["[[Electrostatics scaling module]]"]
requirements: ["[[REQ-005 Nonbonded pair scaling rules|REQ-005]]", "[[REQ-025 Supported nonbonded methods are correct|REQ-025]]"]
fixed_by: ["[[TASK-038 Refuse reaction-field cutoff methods|TASK-038]]"]
found: 2026-09-26
updated: 2026-09-27
---
# ISS-003 — Within-block electrostatic correction is wrong for non-PME cutoff methods (audit F3)

`add_within_block_elec_correction` uses `erfc(αr)/r` for CutoffPeriodic and `1/r` for
CutoffNonPeriodic, but `NonbondedForce` uses **reaction field** for both. Within-block energy is then
not linear in λ: at λ = 0.5, CutoffNonPeriodic −66.67 vs expected −17.56 kJ/mol (error −49),
CutoffPeriodic −9.55 vs −17.56 (+8) ([[EXP-003 Within-block linearity per nonbonded method|EXP-003]]). NoCutoff and PME are correct.

Fix: refuse these methods ([[ADR-0040 Supported nonbonded methods|ADR-0040]]) or use the reaction-field kernel ([[Reaction-field electrostatics]]).

