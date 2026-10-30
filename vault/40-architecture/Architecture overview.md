---
title: Architecture overview
type: architecture
status: partial
layer: L0
decisions: ["[[ADR-0001 Build MSLD natively in OpenMM|ADR-0001]]", "[[ADR-0004 Correctness first in Python on stock OpenMM|ADR-0004]]", "[[ADR-0032 Three subsystems preparation simulation analysis|ADR-0032]]"]
updated: 2026-09-27
---
# Architecture overview

This is the **blueprint** of MSLD-OpenMM: what we build, how the parts fit, and why. It is our
synthesis; every choice links to an ADR in [[Decision log]]. Each note states the **target**
design and the **as-built** status, so the gap is always visible.

## L0 — System context

```
                 researcher / agent
                        │ variants, structures, settings
                        ▼
 ┌─────────────────────────────── MSLD-OpenMM ───────────────────────────────┐
 │                                                                           │
 │   PREPARATION  ──bundle──▶  SIMULATION  ──λ trajectories──▶  ANALYSIS     │
 │   subsystem                 subsystem                        subsystem    │
 │                                                                           │
 └──────┬──────────────────────────┬───────────────────────────────┬─────────┘
        │ uses                     │ uses / extends                │ reports
        ▼                          ▼                               ▼
 ParmEd, RDKit,            OpenMM (System, Context,         ΔG, ΔΔG, uncertainty,
 openmmforcefields,        platforms) + our plugin          diagnostics
 AmberTools                (future)
        ▲                          ▲
        │ force fields             │ validated against
 Amber ff14SB/ff19SB, GAFF,  BLaDE (CHARMM) and FEP/TI (Amber)
 OpenFF, CHARMM36
```

## L1 — The three subsystems (decision [[ADR-0032 Three subsystems preparation simulation analysis|ADR-0032]])

The architecture follows from the main goal ([[G-1 Free energies for many variants at once|G-1]]): to get free energies we must **prepare** a
hybrid system, **simulate** it with λ-dynamics, and **analyse** the λ trajectories.

| subsystem | responsibility | input → output | note |
|---|---|---|---|
| **Preparation** | turn standard inputs + variant lists into a hybrid MSLD system | files → `HybridSystemBundle` | [[Preparation subsystem]] |
| **Simulation** | apply MSLD to an OpenMM System and run λ-dynamics (incl. ALF flattening) | bundle → λ/energy/coordinate trajectories + learned biases | [[Simulation subsystem]] |
| **Analysis** | turn trajectories into free energies with uncertainties and diagnostics | trajectories → ΔG, ΔΔG, reports | [[Analysis subsystem]] (specified only at high level for now) |

Cross-cutting: **validation** ([[BLaDE cross-validation harness]], [[Partial-lambda oracle tests]])
and the **data contracts** between subsystems ([[CoreMapping and HybridBlueprint]],
[[HybridSystemBundle]], [[MSLD model data contract]], [[Context parameter naming]],
[[Lambda trajectory format]]).

## L2 — Components

```
 PREPARATION                      SIMULATION                               ANALYSIS
 ┌──────────────┐                 ┌───────────────────┐                    ┌──────────────────┐
 │ Ingest       │                 │ MSLD model        │                    │ Free energy      │
 │ Mapping      │  bundle.system  │ Force scaling ────┼─ modules: bonded,  │ estimation       │
 │ Assembly     │ ───────────────▶│  (builder)        │  elec, LJ, 1-4,    │ Sampling         │
 │  · grafting  │  bundle.to_     │ λ-dynamics        │  biases, restraints│ diagnostics      │
 │  · alignment │  model()        │  integrator       │                    └──────────────────┘
 │  · charges   │                 │ Output reporters ─┼──── λ CSV, DCD ──────────▲
 │  · solvation │                 │ ALF flattening    │                          │
 │  · System    │                 │ (future) plugin:  │                          │
 │  · artifacts │                 │  MSLDNonbonded +  │                          │
 │ Prep facade  │                 │  MSLDIntegrator   │                          │
 └──────────────┘                 └───────────────────┘
```

Component notes: [[Ingest component]] · [[Mapping component]] · [[Assembly component]] ·
[[Prep facade component]] · [[MSLD model component]] · [[Force scaling component]] ·
[[Lambda dynamics integrator component]] · [[Output reporters component]] ·
[[ALF flattening component]] · [[Production plugin architecture]] ·
[[Free energy estimation component]] · [[Sampling diagnostics component]].

## Architectural principles (each backed by an ADR)

1. **BLaDE is the specification.** Where MSLD conventions are ambiguous, we do what BLaDE does, or
   write an ADR explaining a deliberate difference ([[ADR-0002 BLaDE is the reference and validation oracle|ADR-0002]]).
2. **Correctness before speed.** A Python engine on stock OpenMM first; a C++/GPU plugin only after
   the physics is validated ([[ADR-0004 Correctness first in Python on stock OpenMM|ADR-0004]], [[ADR-0035 Gate plugin work|ADR-0035]]).
3. **The engine transforms any OpenMM System.** It dispatches on OpenMM force types, so it is
   force-field agnostic; prep is where force-field specifics live ([[ADR-0003 Amber is the production force field target|ADR-0003]], [[ADR-0016 Prep emits a plain System|ADR-0016]]).
4. **Plain System in, scaled System out.** Prep produces an unmodified, faithful System; the engine
   applies every MSLD change, so λ = 1 ≡ base is testable ([[ADR-0011 Master invariant as the primary gate|ADR-0011]], [[ADR-0016 Prep emits a plain System|ADR-0016]]).
5. **Fail loudly.** Anything we cannot scale correctly raises ([[ADR-0028 Refuse what cannot be scaled|ADR-0028]], [[ADR-0037 Whitelist force types|ADR-0037]]).
6. **One common representation per layer.** ParmEd `Structure` inside prep, OpenMM `System` +
   `MSLDModel` at the engine boundary ([[ADR-0015 ParmEd Structure as prep common representation|ADR-0015]]).
7. **Engine stays light.** Engine imports only openmm + numpy ([[ADR-0030 Hard dependencies and a ParmEd-free engine|ADR-0030]]).

## Where the design is known to be weak (as of 2026-09-27)

- Partial-λ physics never checked against an independent code ([[ISS-012 No validation at partial lambda|ISS-012]]).
- The dU/dλ of electrostatics and biases is a finite difference ([[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]).
- The Python driver: slow, NVT only ([[ISS-009 NPT impossible with the Python driver|ISS-009]]).
- Atom-restraint groups and θ-mass conventions ([[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]], [[ISS-002 Theta mass convention differs from BLaDE|ISS-002]]).
See [[Issue tracker]].

