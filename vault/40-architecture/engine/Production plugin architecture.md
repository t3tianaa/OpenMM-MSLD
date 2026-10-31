---
title: Production plugin architecture
type: component
subsystem: "[[Simulation subsystem]]"
layer: L2
status: planned
code: []
requirements: ["[[REQ-011 Soft-core for alchemical nonbonded|REQ-011]]", "[[REQ-019 NPT ensemble|REQ-019]]", "[[REQ-020 Accurate dU-dlambda for every term|REQ-020]]", "[[REQ-029 Production performance on GPU|REQ-029]]"]
decisions: ["[[ADR-0026 Tier 2 plugin with scope S0 to S4|ADR-0026]]", "[[ADR-0027 Plugin technology choices|ADR-0027]]", "[[ADR-0035 Gate plugin work|ADR-0035]]", "[[ADR-0042 OpenMM multistate samplers for fixed-lambda cross-checks|ADR-0042]]"]
updated: 2026-10-31
---
# Production plugin architecture (Tier 2, planned)

From `PLUGIN_PLAN.md` (2026-09-23), now tracked here.

## Why one plugin fixes four problems

| problem today | fixed by |
|---|---|
| electrostatic dU/dλ is FD | analytic λ-derivative inside the nonbonded kernel |
| ~~hot θ~~ (resolved 2026-10-31: θ units + soft-core, [[ISS-018 Theta runs hot in MDM2\|ISS-018]]) | — |
| NPT impossible | a real OpenMM `Integrator` → `MonteCarloBarostat` fires |
| soft-core as extra custom forces (exists in Python since ADR-0043) | radial shift in the same kernel |
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
| S1 | MSLDNonbondedForce, Reference, soft-core included | λ = 1 invariant; reproduces `tests/data/oracle_toy.json` ([[MSLD energy function spec]]); partial-λ PME energies = Python engine; analytic dU/dλ = Python hybrid |
| S2 | same force on common/GPU | = S1 within fp32 tolerance; last FD gone |
| S3 | MSLDIntegrator | T_θ = 300 K; barostat fires; energy conserved at γ = 0; θ/vθ/biases survive `context.setState()`; has `getTemperature()`; runs under `ReplicaExchangeSampler` ([[ADR-0042 OpenMM multistate samplers for fixed-lambda cross-checks\|ADR-0042]]) |
| S4 | ~~soft-core~~ folded into S1 (the energy function already includes it) | — |

Original estimate: 4–7 months part-time. Technology choices: [[ADR-0027 Plugin technology choices|ADR-0027]].

## OpenMM 8.6 multistate samplers ([[AUD-002 OpenMM 8.6 impact on MSLD|AUD-002]], [[ADR-0042 OpenMM multistate samplers for fixed-lambda cross-checks|ADR-0042]], proposed)
OpenMM 8.6 adds `ReplicaExchangeSampler` / `ExpandedEnsembleSampler`. They swap replicas with
`context.setState()` and step with `integrator.step()`. If `MSLDIntegrator` keeps θ, vθ and the bias coefficients
in Context state (integrator parameters/globals) and exposes `getTemperature()`, then **BP-REX**, replica
checkpoints and MBAR-ready energy output come for free, with no MSLD-specific replica code. 8.6 does **not**
change S1/S2: `NonbondedForce` still has no λ-derivatives.

## Gate ([[ADR-0035 Gate plugin work|ADR-0035]], proposed)
Do not start S0 until: the θ-mass/units question is settled ([[TASK-032 Resolve BLaDE theta units|TASK-032]], [[TASK-033 Rerun MDM2 with reference theta parameters|TASK-033]]) — it may
remove the "hot θ" motivation — and a first BLaDE partial-λ cross-check exists ([[TASK-043 BLaDE fixed-lambda cross-check|TASK-043]]), so the
plugin reproduces a validated energy function, not a convention bug.


**Gate met (2026-10-31).** θ units settled ([[ADR-0038 Theta units and default theta mass|ADR-0038]]) and the NumPy oracle passes at partial λ
([[TASK-067 NumPy partial-lambda oracle tests|TASK-067]]); the BLaDE cross-check moves into the plugin stage. Target energy:
[[MSLD energy function spec]]. Also in the plugin stage: the published ALF update ([[ALF package overview]],
[[EXP-012 MDM2 TI and ALF on the fixed build|EXP-012]]), atom friction 0.1 ps⁻¹ / dt 2 fs, long runs on a CUDA machine.
