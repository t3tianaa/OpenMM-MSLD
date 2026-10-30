---
id: REQ-019
type: requirement
title: NPT ensemble
area: engine
priority: must
status: proposed
derives_from: ["[[G-4 Production performance|G-4]]"]
satisfied_by: ["[[FEAT-032 NPT ensemble|FEAT-032]]"]
created: 2026-09-01
updated: 2026-09-27
retrospective: true
---
# REQ-019 — NPT ensemble

**Statement.** Production runs shall support constant pressure (Monte Carlo barostat) together with
λ-dynamics, as BLaDE does (`freqnpt`, [[BLaDE pressure coupling]]).

Status: impossible with the Python driver ([[ISS-009 NPT impossible with the Python driver|ISS-009]]).

