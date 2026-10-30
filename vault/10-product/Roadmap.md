---
title: Roadmap
type: product
status: active
updated: 2026-10-29
---
# Roadmap

Milestones are ordered by **risk reduction**: first make the physics provably right, then fast.
This order follows the original phase plan (old vault, "How BLaDE works") and the audit's
recommendation ([[AUD-001 Engine audit of the local working copy|AUD-001]] §6).

```
 M0 ─ M1 ─ M2 ─ M3 ────── M4 ───── M5 ────── M6 ───────── M7 ──────── M8
 env  energy dyn  prep   harden   validate  free-energy  production   science
 ✓    ✓(λ=1) ✓   ✓      ◀ NOW     vs BLaDE  ALF+analysis  plugin       Amber apps
```

| milestone                    | goal                                                         | status                             | exit criteria                                                                                                                                                                             |
| ---------------------------- | ------------------------------------------------------------ | ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **M0 Foundations**           | env, tools, reference understanding                          | done (no BLaDE reference data yet) | OpenMM + deps installed; BLaDE internals studied                                                                                                                                          |
| **M1 Energy function**       | block-scaled energy at fixed λ                               | done at λ = 1 only                 | master invariant; analytic dU/dλ checks                                                                                                                                                   |
| **M2 λ-dynamics**            | θ + atoms integrated                                         | done, with caveats                 | θ samples the right distribution on a toy ([[EXP-001 Theta samples the exact Boltzmann distribution on a toy\|EXP-001]])                                                                  |
| **M3 Preparation**           | inputs → hybrid system                                       | done for peptides; not audited     | MDM2 end-to-end ([[FEAT-022 MDM2 test system\|FEAT-022]])                                                                                                                                 |
| **M4 Correctness hardening** | fix audit findings; secure the code                          | **next**                           | [[ISS-001 Atom restraint groups have the wrong meaning\|ISS-001]]…[[ISS-011 ALF is a heuristic and ddG is single-leg\|ISS-011]] resolved or accepted by ADR; prep audited; code on GitHub |
| **M5 Validation vs BLaDE**   | partial-λ energies, dU/dλ, λ statistics                      | planned                            | [[REQ-070 Agree with BLaDE on a shared CHARMM system\|REQ-070]] met on a small CHARMM system                                                                                              |
| **M6 Free energies**         | standard ALF, analysis subsystem, ΔΔG                        | planned                            | a published ΔΔG reproduced (e.g. T4L)                                                                                                                                                     |
| **M7 Production engine**     | plugin: analytic PME dU/dλ, fused integrator, NPT, soft-core | planned                            | [[REQ-029 Production performance on GPU\|REQ-029]], [[REQ-019 NPT ensemble\|REQ-019]], [[REQ-011 Soft-core for alchemical nonbonded\|REQ-011]]                                            |
| **M8 Amber science**         | Amber validation vs FEP/TI; first application                | planned                            | [[REQ-071 Agree with FEP or TI on Amber\|REQ-071]]                                                                                                                                        |

Gates between milestones (from [[ADR-0035 Gate plugin work|ADR-0035]], proposed): no plugin work before M4's θ-mass
experiment ([[TASK-033 Rerun MDM2 with reference theta parameters|TASK-033]]) and the first M5 cross-check ([[TASK-043 BLaDE fixed-lambda cross-check|TASK-043]]) — otherwise the plugin may
faithfully reproduce a convention bug, only faster.

**OpenMM 8.6 (2026-10-29, [[AUD-002 OpenMM 8.6 impact on MSLD|AUD-002]]).** Pinned to 8.6.1. Its new `ReplicaExchangeSampler` changes two things
(proposed in [[ADR-0042 OpenMM multistate samplers for fixed-lambda cross-checks|ADR-0042]]):
- **M5 gains a second, cheap check.** Fixed-λ HREX + MBAR on our own scaled System, with the stock integrator, NPT
  and constraints ([[TASK-078 Fixed-lambda replica-exchange cross-check|TASK-078]]). It validates MSLD sampling and gives the in-house FEP-style reference that
  M8 ([[REQ-071 Agree with FEP or TI on Amber|REQ-071]]) needs, without waiting for BLaDE or the plugin. The BLaDE energy cross-check stays.
- **M7 plugin integrator keeps θ in Context state**, so BP-REX and replica checkpoints come from OpenMM for free.
  The plugin scope is otherwise unchanged: 8.6 still has no electrostatic λ-derivatives.

Live task lists: [[Task board]].
