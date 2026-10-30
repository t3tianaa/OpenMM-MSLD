---
title: Lambda dynamics integrator component
type: component
subsystem: "[[Simulation subsystem]]"
layer: L2
status: partial
code: [msld/integrator.py]
requirements: ["[[REQ-016 Canonical sampling of atoms and theta|REQ-016]]", "[[REQ-017 Per-block theta mass, friction and fixing|REQ-017]]", "[[REQ-018 Holonomic constraints and virtual sites|REQ-018]]", "[[REQ-019 NPT ensemble|REQ-019]]", "[[REQ-026 Energy minimization at fixed lambda|REQ-026]]"]
decisions: ["[[ADR-0012 Python driver integrator instead of CustomIntegrator|ADR-0012]]", "[[ADR-0013 Tier 0 analytic dU-dlambda via force groups|ADR-0013]]", "[[ADR-0038 Theta units and default theta mass|ADR-0038]]"]
issues: ["[[ISS-002 Theta mass convention differs from BLaDE|ISS-002]]", "[[ISS-009 NPT impossible with the Python driver|ISS-009]]", "[[ISS-017 Zero-mass particles break the integrator|ISS-017]]", "[[ISS-018 Theta runs hot in MDM2|ISS-018]]", "[[ISS-019 Fixed-block lambda semantics differ from BLaDE|ISS-019]]"]
updated: 2026-09-27
---
# λ-dynamics integrator component — `LambdaDynamics`

## Purpose
Integrate atoms and θ together with Langevin BAOAB (VRORV), using OpenMM only to evaluate forces,
energies and parameter derivatives ([[Langevin dynamics and BAOAB splitting]]).

## Interfaces
```python
LambdaDynamics(context, model, temperature=300.0, timestep=0.001, atom_friction=1.0,
               fd_step=1e-4, seed=None)
  .project() → λ (softmax, pushed to the Context)     .get_lambdas()
  .dUdlambda()  .dUdtheta()                            .potential_energy()
  .minimize(max_iterations=0, tolerance=10.0)         (atoms only, at current λ)
  .step(n)                                             .run(n, minimize=…, metrics=…, trajectory=…, reporters=…)
  .theta_temperature()
```

## One step (B A O A B)
```
 B: v_x += dt/2·F_x/m;   RATTLE;   v_θ += dt/2·F_θ/m_θ
 A: x += dt/2·v_x (SHAKE via context.applyConstraints, correction folded into v);  θ += dt/2·v_θ
 O: v_x = a·v_x + b·ξ;   RATTLE;   v_θ = a_θ·v_θ + b_θ·ξ         (per-block friction)
 A: as above
 force evaluation: θ→λ, set λ globals, getState(forces, param derivatives) + FD (group 0)
                   F_θ = −dU/dθ (chain rule)
 B: as above
```
Positions and velocities live in NumPy; each force evaluation copies positions into the Context.

## Why a Python driver (not CustomIntegrator)
The electrostatic ∂U/∂λ is not available to `deriv()` ([[ADR-0012 Python driver integrator instead of CustomIntegrator|ADR-0012]]). Consequences: slow
(~80 ms/step for 26 k atoms on Apple OpenCL, [[EXP-007 MDM2 first end-to-end run and benchmark|EXP-007]]), and **no barostat** ([[ISS-009 NPT impossible with the Python driver|ISS-009]]).

## As-built status
Verified: exact θ/λ Boltzmann sampling on an analytic toy, T_θ = 300 K ([[EXP-001 Theta samples the exact Boltzmann distribution on a toy|EXP-001]]); FD check of
the chain rule (`test_integrator`); constraints (`test_constraints`); minimization (`test_minimize`).
Problems: θ runs hot on MDM2 (1 400–8 000 K) ([[ISS-018 Theta runs hot in MDM2|ISS-018]]) — likely parameters/units
([[ISS-002 Theta mass convention differs from BLaDE|ISS-002]]) and FD noise ([[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]), not integrator code; zero-mass particles divide by zero
([[ISS-017 Zero-mass particles break the integrator|ISS-017]]); fixed-block semantics ([[ISS-019 Fixed-block lambda semantics differ from BLaDE|ISS-019]]); no checkpoint/restart ([[REQ-028 Checkpoint and restart|REQ-028]]); no CM
motion removal (probably unnecessary with Langevin, **Inferred**).

