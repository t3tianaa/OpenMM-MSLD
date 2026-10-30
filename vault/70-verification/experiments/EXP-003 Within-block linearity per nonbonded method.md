---
id: EXP-003
type: experiment
title: Within-block linearity per nonbonded method
status: done
date: 2026-09-26
requirements: ["[[REQ-005 Nonbonded pair scaling rules|REQ-005]]", "[[REQ-025 Supported nonbonded methods are correct|REQ-025]]"]
issues: ["[[ISS-003 Within-block correction wrong for cutoff methods|ISS-003]]"]
related: ["[[AUD-001 Engine audit of the local working copy|AUD-001]]"]
---
# EXP-003 — Within-block linearity per nonbonded method (audit E3)

| method | E(λ=1) | E(0.5) | linear expectation | error |
|---|---|---|---|---|
| NoCutoff | −231.56 | −115.78 | −115.78 | 7e-7 |
| CutoffNonPeriodic | −35.12 | −66.67 | −17.56 | −49 kJ/mol |
| CutoffPeriodic | −35.12 | −9.55 | −17.56 | +8 kJ/mol |

PME unaffected by this bug (see [[ISS-006 Same-site PME differs from BLaDE and docs are backwards|ISS-006]] for PME's λ² reciprocal share).

