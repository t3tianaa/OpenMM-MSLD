---
title: Home
type: meta
status: active
updated: 2026-09-27
---
# Home — MSLD-OpenMM

> **Mission.** Build a native, validated multi-site λ-dynamics (MSLD) engine in OpenMM, plus the
> preparation and analysis around it, so we can compute relative free energies for many chemical
> variants at once and explore chemical space efficiently.

## Where are we? (2026-09-27)

- The **Python engine** on stock OpenMM is feature-rich and its 33 test files pass, but a full audit
  ([[AUD-001 Engine audit of the local working copy|AUD-001]]) found real correctness problems: wrong atom-restraint groups ([[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]]), a
  suspicious θ mass convention ([[ISS-002 Theta mass convention differs from BLaDE|ISS-002]]), several silent-failure paths, and **no validation at
  partial λ** against any independent code.
- The **preparation pipeline** (ingest → map → assemble) runs end to end on the MDM2 peptide
  system, but it has not been audited yet ([[TASK-040 Audit the preparation layer|TASK-040]]).
- There is **no analysis subsystem** beyond a λ-population readout and a heuristic ΔΔG.
- **All of this code is uncommitted** on one laptop ([[ISS-020 Recent work is uncommitted on one laptop|ISS-020]], [[TASK-030 Commit and push the local state to a branch|TASK-030]]).
- Next milestone: **M4 Correctness hardening**, then **M5 BLaDE validation**. See [[Roadmap]] and
  [[Status]].

## Navigate

| I want to… | go to |
|---|---|
| understand the problem and the goals | [[Problem statement]] · [[Vision and goals]] · [[Scope]] · [[Use cases]] |
| see what the system must do | [[Requirements index]] |
| learn the physics and algorithms | [[Theory map]] |
| learn how OpenMM / BLaDE / ParmEd work inside | [[Reference map]] |
| see our design | [[Architecture overview]] · [[Invariants]] · [[Data flow]] |
| know why a design is this way | [[Decision log]] |
| see what is done, broken, next | [[Status]] · [[Task board]] · [[Issue tracker]] · [[Roadmap]] |
| check how correctness is proven | [[Verification strategy]] · [[Test catalog]] |
| see the history | [[Project timeline]] · [[AUD-001 Engine audit of the local working copy\|AUD-001]] |
| learn the rules of this vault | [[Conventions]] · [[Workflow]] · [[Agent protocol]] |

## Three layers of knowledge

```
 ┌─────────────────────── GROUND TRUTH (we describe, we do not invent) ─────────────────────┐
 │  20-theory       what MSLD, PME, ALF, Langevin … ARE          (papers, textbooks)        │
 │  30-reference    how OpenMM, BLaDE, ParmEd DO it               (source code, file:line)  │
 └───────────────────────────────────────┬──────────────────────────────────────────────────┘
                                         │ cited by
 ┌───────────────────────────────────────▼──────── SYNTHESIS (we decide) ───────────────────┐
 │  40-architecture  the blueprint of OUR system (subsystems → components → modules)        │
 │  50-decisions     ADRs: context, options, choice, consequences — why the blueprint is so │
 └───────────────────────────────────────┬──────────────────────────────────────────────────┘
                                         │ realised by
 ┌───────────────────────────────────────▼──────── EXECUTION (we do) ───────────────────────┐
 │  10-product requirements → 60-work features → tasks → code → 70-verification             │
 └──────────────────────────────────────────────────────────────────────────────────────────┘
```

