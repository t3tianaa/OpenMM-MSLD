---
title: Production plugin architecture
type: component
subsystem: "[[Simulation subsystem]]"
layer: L2
status: partial
code: []
requirements: ["[[REQ-011 Soft-core for alchemical nonbonded|REQ-011]]", "[[REQ-019 NPT ensemble|REQ-019]]", "[[REQ-020 Accurate dU-dlambda for every term|REQ-020]]", "[[REQ-029 Production performance on GPU|REQ-029]]"]
decisions: ["[[ADR-0026 Tier 2 plugin with scope S0 to S4|ADR-0026]]", "[[ADR-0027 Plugin technology choices|ADR-0027]]", "[[ADR-0035 Gate plugin work|ADR-0035]]", "[[ADR-0042 OpenMM multistate samplers for fixed-lambda cross-checks|ADR-0042]]", "[[ADR-0046 openmm-ld becomes the standalone MSLD package|ADR-0046]]"]
updated: 2026-11-09
---
# Production plugin architecture (Tier 2, in progress)

From `PLUGIN_PLAN.md` (2026-09-23), now tracked here.

## Why one plugin fixes four problems

| problem today | fixed by |
|---|---|
| electrostatic dU/dλ is FD | analytic λ-derivative inside the nonbonded kernel |
| ~~hot θ~~ (resolved 2026-10-31: θ units + soft-core, [[ISS-018 Theta runs hot in MDM2\|ISS-018]]) | — |
| NPT impossible | a real OpenMM `Integrator` → `MonteCarloBarostat` fires |
| soft-core as extra custom forces (exists in Python since ADR-0043) | radial shift in the same kernel |
| speed | all of the above on GPU |

## Layout ([[ADR-0046 openmm-ld becomes the standalone MSLD package|ADR-0046]]; plugin part from the template, [[OpenMM plugin architecture]])
One package, [t3tianaa/openmm-ld](https://github.com/t3tianaa/openmm-ld); this repository is the reference
implementation during the port, then retires.
```
 openmm-ld/
   openmmapi/             MSLDNonbondedForce (exists)
   platforms/reference/   double precision, also serves the CPU platform (exists)
   platforms/common/      one kernel source -> OpenCL + CUDA + HIP (S2)
   serialization/         XML proxies (exists)
   python/                SWIG module (exists)
   openmm_ld/             Python layer: integrator (a CustomIntegrator, S3), model, forces, dynamics, alf, io (P1);
                          prep (P2), cli (P3): all exist
```
Bonded terms stay stock custom forces (already analytic).

## Stages ([[FEAT-033 Analytic nonbonded plugin force|FEAT-033]], [[FEAT-034 Fused MSLD integrator plugin|FEAT-034]], [[FEAT-031 Soft-core|FEAT-031]])
| stage | deliverable | acceptance | as built (2026-11-09) |
|---|---|---|---|
| S0 | skeleton builds and loads | trivial force = hand calculation | done on Reference + CPU; OpenCL moved to S2 |
| S1 | MSLDNonbondedForce, Reference, soft-core included | λ = 1 invariant; reproduces `tests/data/oracle_toy.json` ([[MSLD energy function spec]]); partial-λ PME energies = Python engine; analytic dU/dλ = Python hybrid; independent Ewald sum ([[EXP-013 Plugin PME against a plain Ewald sum\|EXP-013]]) and BLaDE single points | done except BLaDE ([[TASK-043 BLaDE fixed-lambda cross-check\|TASK-043]]) |
| S2 | same force on common/GPU | = S1 within fp32 tolerance | not started |
| S3 | MSLDIntegrator, as an OpenMM `CustomIntegrator` in `openmm_ld/integrator.py`: no new C++ was needed | T_θ = 300 K; barostat fires; energy conserved at γ = 0; θ/vθ/biases survive `context.setState()`; has `getTemperature()`; runs under `ReplicaExchangeSampler` ([[ADR-0042 OpenMM multistate samplers for fixed-lambda cross-checks\|ADR-0042]]) | done on the toy, 2026-11-09 (`docs/msld_integrator.md` in openmm-ld); pressure and exchange statistics not checked |
| S4 | ~~soft-core~~ folded into S1 (the energy function already includes it) | — | — |
| P1 | Python layer: λ model, bonded/bias/restraint setup, ALF, output | same forces and same ALF updates as this repository on the same inputs | done, 2026-11-09 (`docs/python_layer.md` in openmm-ld); MDM2 runs end to end from a prepared system, briefly |
| P2 | prep ported (`msld/prep/`) | same hybrid System as this repository from the same inputs | done, 2026-11-09 (`docs/prep.md` in openmm-ld): System XML, positions and saved files identical with `random.seed` set |
| P3 | command line: PDB to running system | MDM2 runs from one command without this repository | done, 2026-11-09 (`docs/cli.md` in openmm-ld): `openmm-ld prepare\|alf\|run\|all`, outputs identical to the example scripts on a short run |

Original estimate for S0–S4: 4–7 months part-time. Technology choices: [[ADR-0027 Plugin technology choices|ADR-0027]].
While the port runs, `use_plugin` (`msld/plugin.py`) lets this engine run on the plugin's force for comparison.

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
