---
title: OpenMM force groups and State queries
type: reference
status: verified
system: openmm
version: 8.5.2
related: ["[[Force groups and derivative routing]]"]
updated: 2026-09-27
---
# OpenMM force groups and State queries

- Every force has a group 0–31 (`force.setForceGroup(g)`).
- `context.getState(getEnergy=True, groups={0})` or a bitmask evaluates **only** those groups —
  cheaper than the full energy when the other groups are expensive.
- Parameter derivatives in a State are the sum over the forces in the requested groups.
- One `getState` call can return forces, energy and parameter derivatives together (one force
  evaluation).

Our use: analytic-derivative forces in group 1 (`ANALYTIC_FORCE_GROUP`), everything else λ-dependent
in group 0 (`FD_FORCE_GROUP`), so finite differences touch only group 0
([[Force groups and derivative routing]]). Caveat: PME lives in group 0 together with the whole
env–env nonbonded energy, so each FD evaluation still pays a full PME ([[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]).

