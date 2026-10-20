---
id: REQ-025
type: requirement
title: Supported nonbonded methods are correct
area: engine
priority: must
status: partial
derives_from: ["[[G-2 Physically correct MSLD|G-2]]"]
satisfied_by: ["[[FEAT-047 Engine hardening|FEAT-047]]"]
decisions: ["[[ADR-0040 Supported nonbonded methods|ADR-0040]]"]
created: 2026-09-26
updated: 2026-09-27
---
# REQ-025 — Supported nonbonded methods are correct

**Statement.** For every nonbonded method the engine accepts (NoCutoff, PME, and possibly
CutoffPeriodic / CutoffNonPeriodic with reaction field), partial-λ energies shall follow the
scaling rules; unsupported methods shall be refused.

Evidence: within-block correction is wrong by up to 49 kJ/mol for reaction-field cutoffs
([[EXP-003 Within-block linearity per nonbonded method|EXP-003]], [[ISS-003 Within-block correction wrong for cutoff methods|ISS-003]]).

