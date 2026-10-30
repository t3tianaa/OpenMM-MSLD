---
id: REQ-018
type: requirement
title: Holonomic constraints and virtual sites
area: engine
priority: must
status: partial
derives_from: ["[[G-4 Production performance|G-4]]"]
satisfied_by: ["[[FEAT-008 Lambda-dynamics integrator|FEAT-008]]"]
verified_by: ["test_constraints"]
created: 2026-08-10
updated: 2026-09-27
retrospective: true
---
# REQ-018 — Holonomic constraints and virtual sites

**Statement.** Support SHAKE/RATTLE (H-bond constraints, rigid water) for atoms (θ never
constrained), and particles with zero mass (virtual sites, e.g. TIP4P/OPC 4-site water).

## Acceptance criteria
- [x] AC1 — rigid bonds stay rigid while λ moves (`test_constraints`).
- [ ] AC2 — zero-mass particles handled (today: division by zero, [[ISS-017 Zero-mass particles break the integrator|ISS-017]]).

