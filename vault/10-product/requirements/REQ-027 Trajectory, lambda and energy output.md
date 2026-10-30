---
id: REQ-027
type: requirement
title: Trajectory, lambda and energy output
area: engine
priority: must
status: partial
derives_from: ["[[G-5 Meaningful analysis|G-5]]"]
satisfied_by: ["[[FEAT-011 Trajectory and lambda output|FEAT-011]]"]
verified_by: ["test_io"]
created: 2026-09-15
updated: 2026-09-27
retrospective: true
---
# REQ-027 — Trajectory, λ and energy output

**Statement.** Write per-block λ (and θ) at a chosen interval, energies, and coordinates (DCD +
topology), in formats the analysis subsystem and BLaDE-style tools can read ([[Lambda trajectory format]]).

Gap: no θ output, no BLaDE `.lmd`-compatible writer, λ written at 100-step intervals by default
while BLaDE examples use 10.

