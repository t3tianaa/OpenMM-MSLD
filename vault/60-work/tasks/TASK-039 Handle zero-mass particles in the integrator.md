---
id: TASK-039
type: task
title: Handle zero-mass particles in the integrator
status: todo
kind: fix
priority: P2
milestone: M4
feature: "[[FEAT-047 Engine hardening|FEAT-047]]"
issues: ["[[ISS-017 Zero-mass particles break the integrator|ISS-017]]"]
created: 2026-09-27
updated: 2026-09-27
---
# TASK-039 — Handle zero-mass particles (virtual sites) in `LambdaDynamics`

Skip m = 0 in kicks and thermostat; place virtual sites via the Context; test with a TIP4P box.

