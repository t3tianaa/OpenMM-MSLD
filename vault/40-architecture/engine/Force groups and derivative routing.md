---
title: Force groups and derivative routing
type: component
subsystem: "[[Simulation subsystem]]"
layer: L3
status: as-built
code: [msld/builder.py, msld/integrator.py]
requirements: ["[[REQ-020 Accurate dU-dlambda for every term|REQ-020]]"]
decisions: ["[[ADR-0013 Tier 0 analytic dU-dlambda via force groups|ADR-0013]]"]
issues: ["[[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]"]
updated: 2026-09-27
---
# Force groups and derivative routing (Tier 0)

`builder._split_force_groups`: every force with `getNumEnergyParameterDerivatives() > 0` →
`ANALYTIC_FORCE_GROUP = 1`; all other forces → `FD_FORCE_GROUP = 0` (the NonbondedForce with charge
offsets, the bias force, zeroed base bonded forces, env-only forces, anything injected later).

`LambdaDynamics.dUdlambda`:
```
 analytic = getState(getForces, getParameterDerivatives)   (one evaluation; merged with the atom forces)
 for each moving block b:
     e = [E_group0(λ_b + h) − E_group0(λ_b − h)] / 2h        (h = fd_step, default 1e-4)
     dU/dλ_b = analytic[lambda_b] + e
```
Cost per step: 1 full evaluation + 2·n_blocks group-0 evaluations (each including full PME).
Accuracy: exact in double precision; noisy in fp32 ([[Finite differences and floating-point precision]]).
Verified equal to the old full-energy FD to ~5e-9 on a toy ([[EXP-008 Tier-0 derivative exactness|EXP-008]]).

Improvement path: (1) analytic biases ([[TASK-041 Analytic bias derivatives|TASK-041]]); (2) move env-only forces out of group 0 into
a third group so the FD does not re-evaluate them (**Inferred** saving; PME still dominates);
(3) analytic electrostatics in the plugin ([[FEAT-033 Analytic nonbonded plugin force|FEAT-033]]).

