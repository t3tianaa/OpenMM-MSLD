---
title: OpenMM object model
type: reference
status: verified
system: openmm
version: 8.5.2
related: ["[[OpenMM custom forces and parameter derivatives]]", "[[OpenMM NonbondedForce]]"]
updated: 2026-09-27
---
# OpenMM object model

```
  System        particles (masses) + constraints + list of Force objects + box. No positions.
    │ Force      one energy contribution (bonds, nonbonded, …); each has a force group (0–31)
    ▼
  Context  =  System + Integrator + Platform + live state (positions, velocities, parameters)
    │
    ▼
  State         immutable snapshot: energy, forces, positions, parameters, parameter derivatives
```

- **System** is a recipe. Our engine *edits* a System (build time): moves terms from built-in
  forces into custom forces, adds exclusions, offsets, biases. Changes after a Context exists
  require `force.updateParametersInContext(context)` or a new Context (topology changes always
  need a new Context).
- **Context** holds **global parameters** (e.g. `lambda3 = 0.4`), set with
  `context.setParameter(name, value)` at run time — our λ's live here.
- **State** is obtained with `context.getState(getEnergy=…, getForces=…, getParameterDerivatives=…,
  groups=…)`.
- **Integrator** advances the Context; `Integrator.step(n)` also triggers `Force`s that act during
  a step (barostats, thermostats like `AndersenThermostat`, `CMMotionRemover`).
- **Platform**: Reference (double, C++), CPU (mixed/single, vectorized), OpenCL, CUDA (and HIP).

Two clocks (from the old notes):
```
 BUILD TIME (System)                      RUN TIME (Context)
 forces.py rewrites forces                set_lambdas(context, …)
 builder.scale_msld_system(system, model) LambdaDynamics.step()
```

Units everywhere: nm, ps, kJ/mol, amu (dalton), elementary charge, radians.

Source: OpenMM user guide & API docs; headers `System.h`, `Context.h`, `State.h`. **Doc/Verified.**

