---
id: ISS-009
type: issue
title: NPT impossible with the Python driver
status: open
kind: gap
severity: medium
confidence: confirmed
source: "[[AUD-001 Engine audit of the local working copy|AUD-001]]"
affects: ["[[Lambda dynamics integrator component]]"]
requirements: ["[[REQ-019 NPT ensemble|REQ-019]]"]
fixed_by: ["[[TASK-049 Interim NPT in the Python driver|TASK-049]]", "[[TASK-061 Plugin S3 fused integrator|TASK-061]]"]
found: 2026-09-01
updated: 2026-09-27
---
# ISS-009 — NPT impossible with the Python driver (audit F9)

`LambdaDynamics` never calls `Integrator.step()`, so a `MonteCarloBarostat` never fires
([[OpenMM barostat mechanics]]). MSLD production is normally NPT (BLaDE examples: `freqnpt 100`).

