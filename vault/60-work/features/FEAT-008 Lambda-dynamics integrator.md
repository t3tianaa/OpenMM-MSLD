---
id: FEAT-008
type: feature
title: Lambda-dynamics integrator
status: done
milestone: M2
implements: ["[[REQ-016 Canonical sampling of atoms and theta|REQ-016]]", "[[REQ-017 Per-block theta mass, friction and fixing|REQ-017]]", "[[REQ-018 Holonomic constraints and virtual sites|REQ-018]]", "[[REQ-002 Lambda from theta with implicit constraints|REQ-002]]"]
components: ["[[Lambda dynamics integrator component]]"]
decisions: ["[[ADR-0012 Python driver integrator instead of CustomIntegrator|ADR-0012]]", "[[ADR-0038 Theta units and default theta mass|ADR-0038]]"]
tasks: ["[[TASK-006 Implement the lambda-dynamics integrator|TASK-006]]", "[[TASK-007 Add biases, restraints and constraints|TASK-007]]", "[[TASK-021 Make the MDM2 run work end to end|TASK-021]]", "[[TASK-039 Handle zero-mass particles in the integrator|TASK-039]]", "[[TASK-056 Fixed-block semantics like BLaDE|TASK-056]]"]
issues: ["[[ISS-009 NPT impossible with the Python driver|ISS-009]]", "[[ISS-017 Zero-mass particles break the integrator|ISS-017]]", "[[ISS-018 Theta runs hot in MDM2|ISS-018]]", "[[ISS-019 Fixed-block lambda semantics differ from BLaDE|ISS-019]]", "[[ISS-002 Theta mass convention differs from BLaDE|ISS-002]]"]
created: 2026-08-10
updated: 2026-09-27
retrospective: true
---
# FEAT-008 — λ-dynamics integrator

`LambdaDynamics`: combined VRORV over atoms + θ, chain rule, SHAKE/RATTLE, minimization, run with
reporters. Samples exactly on a toy ([[EXP-001 Theta samples the exact Boltzmann distribution on a toy|EXP-001]]). Open: θ units/parameters ([[ISS-002 Theta mass convention differs from BLaDE|ISS-002]]), hot θ in
real systems ([[ISS-018 Theta runs hot in MDM2|ISS-018]]), zero-mass particles ([[ISS-017 Zero-mass particles break the integrator|ISS-017]]), fixed-block semantics ([[ISS-019 Fixed-block lambda semantics differ from BLaDE|ISS-019]]),
NPT ([[FEAT-032 NPT ensemble|FEAT-032]]).

