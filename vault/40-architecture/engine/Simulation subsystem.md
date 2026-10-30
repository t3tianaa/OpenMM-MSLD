---
title: Simulation subsystem
type: subsystem
status: partial
layer: L1
code: [msld/model.py, msld/builder.py, msld/forces.py, msld/integrator.py, msld/io.py, msld/alf.py]
requirements: ["[[REQ-001 Represent sites, blocks and environment|REQ-001]]", "[[REQ-002 Lambda from theta with implicit constraints|REQ-002]]", "[[REQ-003 Scale bonded terms by block lambdas|REQ-003]]", "[[REQ-005 Nonbonded pair scaling rules|REQ-005]]", "[[REQ-006 Same-site pairs never interact|REQ-006]]", "[[REQ-007 PME electrostatics at partial lambda|REQ-007]]", "[[REQ-012 Fixed and variable lambda biases|REQ-012]]", "[[REQ-016 Canonical sampling of atoms and theta|REQ-016]]", "[[REQ-019 NPT ensemble|REQ-019]]", "[[REQ-020 Accurate dU-dlambda for every term|REQ-020]]", "[[REQ-021 Runs on Reference, CPU, OpenCL, CUDA|REQ-021]]", "[[REQ-022 Refuse unsupported input loudly|REQ-022]]", "[[REQ-023 Lambda one reproduces the base system|REQ-023]]", "[[REQ-029 Production performance on GPU|REQ-029]]", "[[REQ-030 Adaptive landscape flattening|REQ-030]]"]
decisions: ["[[ADR-0004 Correctness first in Python on stock OpenMM|ADR-0004]]", "[[ADR-0005 Lambda as softmax of fnex sin theta|ADR-0005]]", "[[ADR-0006 Bonded scaling via grouped custom forces|ADR-0006]]", "[[ADR-0007 Charges scaled by NonbondedForce offsets|ADR-0007]]", "[[ADR-0008 LJ scaled by grouped CustomNonbondedForces|ADR-0008]]", "[[ADR-0009 Within-block real-space electrostatics linear|ADR-0009]]", "[[ADR-0010 Same-site pairs excluded in every nonbonded force|ADR-0010]]", "[[ADR-0011 Master invariant as the primary gate|ADR-0011]]", "[[ADR-0012 Python driver integrator instead of CustomIntegrator|ADR-0012]]", "[[ADR-0013 Tier 0 analytic dU-dlambda via force groups|ADR-0013]]"]
issues: ["[[ISS-002 Theta mass convention differs from BLaDE|ISS-002]]", "[[ISS-003 Within-block correction wrong for cutoff methods|ISS-003]]", "[[ISS-004 CHARMM NBFIX systems fail on CPU|ISS-004]]", "[[ISS-005 Unsupported force types silently unscaled|ISS-005]]", "[[ISS-006 Same-site PME differs from BLaDE and docs are backwards|ISS-006]]", "[[ISS-007 Dispersion correction removed for the whole system|ISS-007]]", "[[ISS-008 PME alpha recomputed from the tolerance|ISS-008]]", "[[ISS-009 NPT impossible with the Python driver|ISS-009]]", "[[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]", "[[ISS-012 No validation at partial lambda|ISS-012]]", "[[ISS-017 Zero-mass particles break the integrator|ISS-017]]"]
updated: 2026-09-27
---
# Simulation subsystem (the MSLD engine)

## Purpose
Given any OpenMM `System` and an `MSLDModel`, (1) rewrite the System so every energy term carries
the right λ factors and exposes ∂U/∂λ, and (2) integrate atoms and θ together with correct
thermostatting, (3) flatten the landscape with learned biases, and (4) write the trajectories the
analysis needs.

## Components

```
 MSLDModel ─────────────┐                      [[MSLD model component]]
 (sites, blocks, θ, biases, restraints, flags) │
                        ▼
 scale_msld_system(system, model)              [[Force scaling component]]
   bonded · electrostatics · LJ · 1-4 · biases · restraints · force groups
                        ▼
 Context(system, VerletIntegrator(dummy), platform)
                        ▼
 LambdaDynamics(ctx, model, T, dt, …)          [[Lambda dynamics integrator component]]
   .minimize()  .step()  .run(metrics=…, trajectory=…)
                        ▼
 reporters: λ/energy CSV, DCD                  [[Output reporters component]]
 alf.flatten(dyn, …) → learned biases          [[ALF flattening component]]

 FUTURE: MSLDNonbondedForce + MSLDIntegrator    [[Production plugin architecture]]
```

## Two tiers (decisions [[ADR-0004 Correctness first in Python on stock OpenMM|ADR-0004]], [[ADR-0013 Tier 0 analytic dU-dlambda via force groups|ADR-0013]], [[ADR-0026 Tier 2 plugin with scope S0 to S4|ADR-0026]])

| tier | what | status |
|---|---|---|
| Tier 1 (Python, stock OpenMM) | correctness reference; all platforms; slow; NVT | built, being hardened |
| Tier 0 (inside Tier 1) | analytic dU/dλ where OpenMM allows; FD only group 0 | built |
| Tier 2 (C++ plugin) | analytic elec dU/dλ, fused integrator (NPT), soft-core, GPU speed | planned, gated ([[ADR-0035 Gate plugin work\|ADR-0035]]) |

## Usage (as built)
```python
model = bundle.to_model()                 # or build MSLDModel by hand
model.scale_bond = model.scale_angle = False   # BLaDE-style removescaling (see ADR-0041)
model.scale_system(system)                # == scale_msld_system(system, model)
ctx = mm.Context(system, mm.VerletIntegrator(0.001), mm.Platform.getPlatformByName("OpenCL"))
ctx.setPositions(positions)
dyn = LambdaDynamics(ctx, model, temperature=300, timestep=0.001, atom_friction=1.0, seed=1)
dyn.minimize(); dyn.run(10_000, metrics="out/metrics.csv", metrics_every=100)
```

## As-built status and known problems
33 test files pass. Findings from [[AUD-001 Engine audit of the local working copy|AUD-001]]: [[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]]…[[ISS-017 Zero-mass particles break the integrator|ISS-017]]. The largest open risks:
no partial-λ validation ([[ISS-012 No validation at partial lambda|ISS-012]]), θ mass convention ([[ISS-002 Theta mass convention differs from BLaDE|ISS-002]]), FD noise ([[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]),
NVT only ([[ISS-009 NPT impossible with the Python driver|ISS-009]]).

