---
id: TASK-032
type: task
title: Resolve BLaDE theta units
status: todo
kind: research
priority: P0
milestone: M4
feature: "[[FEAT-008 Lambda-dynamics integrator|FEAT-008]]"
issues: ["[[ISS-002 Theta mass convention differs from BLaDE|ISS-002]]", "[[ISS-018 Theta runs hot in MDM2|ISS-018]]"]
refs: ["[[BLaDE units and theta mass]]", "[[BLaDE lambda from theta and theta force]]", "[[Langevin dynamics and BAOAB splitting]]"]
created: 2026-09-27
updated: 2026-09-27
---
# TASK-032 — Resolve BLaDE's θ unit convention and the equivalent θ mass

## Acceptance criteria
- [ ] Determine which build (AKMA or NMPS) BLaDE's authors use for production MSLD (docs, ALF
      scripts, papers' SI, or ask).
- [ ] Derive the effective θ mass/friction in our units for both builds; check against a BLaDE toy
      run if a CUDA machine is available.
- [ ] Update [[BLaDE units and theta mass]] from draft to verified; propose defaults in [[ADR-0038 Theta units and default theta mass|ADR-0038]].

