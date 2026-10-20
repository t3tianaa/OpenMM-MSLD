---
id: FEAT-032
type: feature
title: NPT ensemble
status: planned
milestone: M7
implements: ["[[REQ-019 NPT ensemble|REQ-019]]"]
components: ["[[Lambda dynamics integrator component]]", "[[Production plugin architecture]]"]
tasks: ["[[TASK-049 Interim NPT in the Python driver|TASK-049]]", "[[TASK-061 Plugin S3 fused integrator|TASK-061]]"]
issues: ["[[ISS-009 NPT impossible with the Python driver|ISS-009]]"]
created: 2026-09-01
updated: 2026-09-27
---
# FEAT-032 — NPT ensemble

Interim: a Python MC volume move in `LambdaDynamics` (like BLaDE's `pressure_coupling`) — possible,
needs care with PME grid and molecule-centre scaling. Final: plugin integrator (barostat for free).

