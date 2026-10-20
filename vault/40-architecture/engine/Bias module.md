---
title: Bias module
type: component
subsystem: "[[Simulation subsystem]]"
layer: L3
status: partial
code: [msld/forces.py]
requirements: ["[[REQ-012 Fixed and variable lambda biases|REQ-012]]", "[[REQ-013 Theta biases|REQ-013]]", "[[REQ-020 Accurate dU-dlambda for every term|REQ-020]]"]
decisions: ["[[ADR-0024 Home-grown ALF heuristic|ADR-0024]]"]
issues: ["[[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]", "[[ISS-016 Theta biases and charge restraints missing|ISS-016]]"]
updated: 2026-09-27
---
# Bias module — `add_biases`

One position-independent `CustomExternalForce` "MSLDBias" on a dummy particle 0 whose expression is
the sum of:
- fixed: `biascoef{b}*lambda{b}` (only non-zero ones, or all if `model.bias_flattening`);
- variable: type 6 `biask{m}*li*lj`, type 8 `biask{m}*li*lj/(li+l0)`, type 10
  `biask{m}*lj*(1-exp(l0*li))` (same formulas as BLaDE, [[BLaDE biases and theta biases]]).

Every coefficient is a Context global ([[Context parameter naming]]) so ALF can change it live with
`builder.set_biases(context, model)`.

dU/dλ: `CustomExternalForce` has no parameter derivatives → finite difference in group 0
([[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]). Cheap fix candidates: compute the closed-form derivatives in Python (as BLaDE does),
or host the biases on a force class that supports `addEnergyParameterDerivative`
([[OpenMM custom forces and parameter derivatives]], [[TASK-041 Analytic bias derivatives|TASK-041]]).

Not built: other BLaDE types; θ biases ([[ISS-016 Theta biases and charge restraints missing|ISS-016]], [[FEAT-038 Theta biases|FEAT-038]]).

