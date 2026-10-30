---
id: ADR-0042
type: adr
title: OpenMM multistate samplers for fixed-lambda cross-checks
status: proposed
date: 2026-10-29
deciders: [Tetiana]
affects: ["[[Production plugin architecture]]", "[[Roadmap]]", "[[Verification strategy]]"]
requirements: ["[[REQ-071 Agree with FEP or TI on Amber|REQ-071]]", "[[REQ-016 Canonical sampling of atoms and theta|REQ-016]]", "[[REQ-019 NPT ensemble|REQ-019]]"]
retrospective: false
---
# ADR-0042 — Use OpenMM's multistate samplers for fixed-λ cross-checks; plugin θ lives in Context state (proposed)

## Context
OpenMM 8.6 added `ReplicaExchangeSampler`, `ExpandedEnsembleSampler` and `ReplicaExchangeReporter`
([[AUD-002 OpenMM 8.6 impact on MSLD|AUD-002]]). A state is a dict of Context parameters, CustomIntegrator globals, temperature or
weighted force groups. Replicas run serially on one Context (`setState` with parameters and integrator
parameters), each by `simulation.integrator.step()`. The reporter writes the reduced-energy matrix (MBAR-ready),
box volumes, trajectories and checkpoints. `simulateReplica()` / `exchangeReplicas()` are override points.

Our scaled System already exposes every λ_b (and every bias coefficient) as a global Context parameter. But
`LambdaDynamics` is not an OpenMM `Integrator` and keeps θ/vθ in Python ([[ADR-0012 Python driver integrator instead of CustomIntegrator|ADR-0012]]), so the samplers
cannot drive MSLD itself.

## Proposed decision
1. **Python tier: use the samplers for validation, not for MSLD.** Run fixed-λ Hamiltonian replica exchange over
   λ-vectors of our scaled System, with a stock `LangevinMiddleIntegrator`, H-bond constraints and
   `MonteCarloBarostat`, and analyse with MBAR. The ΔG between variant endpoints is independent of θ, the softmax,
   the integrator and ALF. Compare it with MSLD λ-population ΔG on the same Hamiltonian ([[TASK-078 Fixed-lambda replica-exchange cross-check|TASK-078]]). This
   tests sampling ([[REQ-016 Canonical sampling of atoms and theta|REQ-016]]) and gives the in-house FEP-style reference for [[REQ-071 Agree with FEP or TI on Amber|REQ-071]] / [[TASK-064 Amber FEP or TI comparison|TASK-064]].
   It does **not** replace the BLaDE energy cross-check ([[TASK-043 BLaDE fixed-lambda cross-check|TASK-043]]), which tests the energy function itself.
2. **Plugin: design `MSLDIntegrator` (S3) so θ survives `context.setState()`.** Keep θ, vθ and the bias coefficients
   in Context state (integrator parameters or global variables captured by
   `getState(integratorParameters=True)`), and provide `getTemperature()`. Then biasing-potential replica exchange
   (BP-REX), checkpointing and replica reporting come from `ReplicaExchangeSampler` / `ReplicaExchangeReporter` with
   no MSLD-specific code.
3. **No BP-REX in the Python tier.** It would need a subclass that saves θ/vθ beside each replica, and analytic bias
   energies for the exchange step (otherwise every exchange costs n_states full PME evaluations). Not worth it before
   the plugin.

## Consequences
- A cheap, independent free-energy check becomes available in M4/M5 with no new engine code.
- Without soft-core ([[ISS-013 Soft-core off while BLaDE examples use it|ISS-013]]), partial-λ states have end-point problems; use more states near the endpoints.
- The cost is about n_states × one MD run (serial replicas on one Context).
- S3 gets two more acceptance items (state survives `setState`; works under `ReplicaExchangeSampler`).
- The plugin scope ([[ADR-0026 Tier 2 plugin with scope S0 to S4|ADR-0026]]) and gate ([[ADR-0035 Gate plugin work|ADR-0035]]) are unchanged. 8.6 does not provide electrostatic
  λ-derivatives.
