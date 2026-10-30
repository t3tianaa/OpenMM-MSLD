---
id: FEAT-038
type: feature
title: Theta biases
status: deferred
milestone: M6
implements: ["[[REQ-013 Theta biases|REQ-013]]"]
components: ["[[Bias module]]"]
tasks: ["[[TASK-051 Implement theta biases|TASK-051]]"]
issues: ["[[ISS-016 Theta biases and charge restraints missing|ISS-016]]"]
created: 2026-09-01
updated: 2026-09-27
---
# FEAT-038 — θ biases

Collective and independent θ biases (BLaDE `thetabias`) — act on θ directly, so they belong in the
integrator's θ-force, not in an OpenMM force.

