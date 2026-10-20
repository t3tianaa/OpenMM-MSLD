---
title: Production plugin architecture
type: component
subsystem: "[[Simulation subsystem]]"
layer: L2
status: planned
code: []
requirements: ["[[REQ-011 Soft-core for alchemical nonbonded|REQ-011]]", "[[REQ-019 NPT ensemble|REQ-019]]", "[[REQ-020 Accurate dU-dlambda for every term|REQ-020]]", "[[REQ-029 Production performance on GPU|REQ-029]]"]
decisions: ["[[ADR-0026 Tier 2 plugin with scope S0 to S4|ADR-0026]]", "[[ADR-0027 Plugin technology choices|ADR-0027]]", "[[ADR-0035 Gate plugin work|ADR-0035]]"]
updated: 2026-09-27
---
# Production plugin architecture (Tier 2, planned)

From `PLUGIN_PLAN.md` (2026-09-23), now tracked here.

## Why one plugin fixes four problems

| problem today | fixed by |
|---|---|
| electrostatic dU/dλ is FD | analytic λ-derivative inside the nonbonded kernel |
| hot θ | fused θ + atom integrator with better θ treatment |
| NPT impossible | a real OpenMM `Integrator` → `MonteCarloBarostat` fires |
| no soft-core | radial shift in the same kernel |
| speed | all of the above on GPU |

## Layout (from the example plugin template, [[OpenMM plugin architecture]])
```
 openmm-msld/
   openmmapi/   MSLDNonbondedForce (λ-scaled LJ + PME elec + soft-core + analytic dU/dλ_b)
                MSLDIntegrator (fused θ + atom Langevin, a real Integrator)
   platforms/reference/   written FIRST, double precision — the oracle
   platforms/common/      one kernel source → OpenCL + CUDA + HIP
   serialization/  python/ (SWIG)  tests/ (Reference-vs-GPU parity)
```
Bonded terms stay as stock custom forces (already analytic); prep and `MSLDModel` stay in Python.

## Stages ([[FEAT-033 Analytic nonbonded plugin force|FEAT-033]], [[FEAT-034 Fused MSLD integrator plugin|FEAT-034]], [[FEAT-031 Soft-core|FEAT-031]])
| stage | deliverable | acceptance |
|---|---|---|
| S0 | skeleton builds, loads on Reference + OpenCL | trivial force = hand calculation |
| S1 | MSLDNonbondedForce, Reference | λ = 1 invariant; partial-λ energies = Python engine; analytic dU/dλ = Python hybrid |
| S2 | same force on common/GPU | = S1 within fp32 tolerance; last FD gone |
| S3 | MSLDIntegrator | T_θ = 300 K; barostat fires; energy conserved at γ = 0 |
| S4 | soft-core | bounded dU/dλ for strained variants; λ = 1 invariant |

Original estimate: 4–7 months part-time. Technology choices: [[ADR-0027 Plugin technology choices|ADR-0027]].

## Gate ([[ADR-0035 Gate plugin work|ADR-0035]], proposed)
Do not start S0 until: the θ-mass/units question is settled ([[TASK-032 Resolve BLaDE theta units|TASK-032]], [[TASK-033 Rerun MDM2 with reference theta parameters|TASK-033]]) — it may
remove the "hot θ" motivation — and a first BLaDE partial-λ cross-check exists ([[TASK-043 BLaDE fixed-lambda cross-check|TASK-043]]), so the
plugin reproduces a validated energy function, not a convention bug.

