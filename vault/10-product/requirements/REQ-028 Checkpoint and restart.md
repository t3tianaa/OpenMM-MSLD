---
id: REQ-028
type: requirement
title: Checkpoint and restart
area: engine
priority: should
status: proposed
derives_from: ["[[G-4 Production performance|G-4]]"]
satisfied_by: ["[[FEAT-046 Checkpoint and restart|FEAT-046]]"]
created: 2026-09-27
updated: 2026-09-27
---
# REQ-028 — Checkpoint and restart

**Statement.** Save and restore the complete state (positions, velocities, box, θ, θ velocities,
bias coefficients, RNG state) so long runs can be split into chunks, as BLaDE does (`fnmcpi`,
`fnmcpo`).

