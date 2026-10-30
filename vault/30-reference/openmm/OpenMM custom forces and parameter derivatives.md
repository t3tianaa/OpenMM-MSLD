---
title: OpenMM custom forces and parameter derivatives
type: reference
status: verified
system: openmm
version: 8.5.2
related: ["[[OpenMM object model]]", "[[Force groups and derivative routing]]", "[[Bonded scaling module]]"]
updated: 2026-09-27
---
# OpenMM custom forces and energy-parameter derivatives

## Custom forces
`CustomBondForce`, `CustomAngleForce`, `CustomTorsionForce`, `CustomNonbondedForce`,
`CustomExternalForce`, `CustomCompoundBondForce`, `CustomCentroidBondForce`, `CustomCVForce`,
`CustomGBForce`, `CustomHbondForce`, `CustomManyParticleForce`.

You give an **energy expression string**; OpenMM parses it, differentiates it symbolically for
forces, and compiles it for the platform.

- geometry variables supplied by OpenMM: `r` (bonds, nonbonded), `theta` (angles, torsions), `x,y,z`
  (external);
- **per-term parameters** (`addPerBondParameter("k")`, then values in `addBond(i, j, [..])`);
- **global parameters** (`addGlobalParameter("lambda1", 1.0)`) — one value per Context, settable
  at run time: our λ's;
- math functions, `step`, `select`, `min/max`, tabulated functions.

Example (bonded scaling): `CustomBondForce("lambda1*lambda4*0.5*k*(r-length)^2")`.

## Energy-parameter derivatives
`force.addEnergyParameterDerivative("lambda1")` asks OpenMM to also compute ∂E/∂lambda1 for that
force. Read it with `context.getState(getParameterDerivatives=True).getEnergyParameterDerivatives()`
→ a dict summed over all forces (in the requested groups) that registered that parameter.

Classes that support it (grep of headers, **Verified**): `CustomBondForce`, `CustomAngleForce`,
`CustomTorsionForce`, `CustomNonbondedForce`, `CustomCompoundBondForce`, `CustomCentroidBondForce`,
`CustomCVForce`, `CustomGBForce`, `ATMForce`, and `CustomIntegrator` (via `deriv()`).

**Not** supported: `NonbondedForce`, `CustomExternalForce`, `HarmonicBondForce` & other built-ins.

Consequences for us:
- all bonded + LJ + within-block correction forces are analytic ([[FEAT-009 Tier-0 analytic dU-dlambda|FEAT-009]]);
- biases on a `CustomExternalForce` are not → FD today. A position-independent bias could instead
  be a `CustomCVForce` or a `CustomCompoundBondForce` with a global-only expression, which *do*
  support derivatives (**Inferred**, to test in [[TASK-041 Analytic bias derivatives|TASK-041]]);
- electrostatics in `NonbondedForce` are not → FD or plugin.

