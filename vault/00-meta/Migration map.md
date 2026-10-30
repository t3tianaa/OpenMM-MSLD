---
title: Migration map
type: meta
status: active
updated: 2026-09-29
---
# Migration map — where the old documents went

On 2026-09-27 the project knowledge was moved into this vault (decision [[ADR-0031 Project knowledge system in an Obsidian vault|ADR-0031]]). The old
files were deleted on 2026-09-29 ([[TASK-073 Retire the legacy documents|TASK-073]]); this table records where
their content lives now. New knowledge goes only into the vault.

| old source | content | new home |
|---|---|---|
| `README.md` | status + quick start | [[Home]], [[Status]], [[Simulation subsystem]] (usage) |
| `GUIDE.md` Part 0 (concepts, rules, chain rule, BLaDE conventions, invariants) | theory + conventions | [[Multisite lambda dynamics]], [[Alchemical scaling rules in MSLD]], [[Theta force by the chain rule]], [[Invariants]], [[BLaDE nonbonded direct space]] |
| `GUIDE.md` Part 1 (ingest) | as-built design | [[Ingest component]], [[ParmEd round trips and NBFIX loss]] |
| `GUIDE.md` Part 2 (mapping) | as-built design | [[Mapping component]], [[CoreMapping and HybridBlueprint]] |
| `GUIDE.md` Part 3 (assembly) | as-built design | [[Assembly component]] and its sub-notes |
| `GUIDE.md` Part 4 (engine) | as-built design | [[MSLD model component]], [[Force scaling component]], [[Lambda dynamics integrator component]] |
| `GUIDE.md` Part 5 (façade) | as-built design | [[Prep facade component]] |
| `GUIDE.md` Part 6 (deps, FFs, tests, glossary) | reference | [[Dependencies]], [[Force field functional forms]], [[Test catalog]], [[Glossary]] |
| `DEFERRED.md` §A (simplifications) | open decisions + gaps | ADRs ([[Decision log]]), features with status `deferred`, [[Issue tracker]] |
| `DEFERRED.md` §B (not built) | plans | [[FEAT-012 ALF flattening heuristic\|FEAT-012]], [[FEAT-030 BLaDE cross-validation harness\|FEAT-030]]…[[FEAT-042 Additional ingest routes\|FEAT-042]], [[Roadmap]] |
| `DEFERRED.md` "By design" | decisions | [[ADR-0010 Same-site pairs excluded in every nonbonded force\|ADR-0010]], [[ADR-0016 Prep emits a plain System\|ADR-0016]], [[ADR-0009 Within-block real-space electrostatics linear\|ADR-0009]], [[ADR-0011 Master invariant as the primary gate\|ADR-0011]] |
| `PLUGIN_PLAN.md` | plugin design | [[Production plugin architecture]], [[ADR-0026 Tier 2 plugin with scope S0 to S4\|ADR-0026]], [[ADR-0027 Plugin technology choices\|ADR-0027]], [[FEAT-033 Analytic nonbonded plugin force\|FEAT-033]], [[FEAT-034 Fused MSLD integrator plugin\|FEAT-034]], [[FEAT-031 Soft-core\|FEAT-031]] |
| `AUDIT_2026-09-26.md` | audit | [[AUD-001 Engine audit of the local working copy\|AUD-001]] + issues [[ISS-001 Atom restraint groups have the wrong meaning\|ISS-001]]…[[ISS-019 Fixed-block lambda semantics differ from BLaDE\|ISS-019]] + experiments [[EXP-001 Theta samples the exact Boltzmann distribution on a toy\|EXP-001]]…[[EXP-005 Dispersion correction on\|EXP-005]] |
| `MSLD_obsidian/λ Dynamics.md` | theory | [[Lambda dynamics]], [[Multisite lambda dynamics]], [[Free energies from lambda populations]], [[Biasing potentials in MSLD]] |
| `MSLD_obsidian/How BLaDE works.md` | BLaDE internals + early plan | [[BLaDE overview]] and the `30-reference/blade` notes; early phase plan → [[Roadmap]] |
| `MSLD_obsidian/Engine Code Break Down.md` | OpenMM basics + engine walkthrough | [[OpenMM object model]], [[OpenMM custom forces and parameter derivatives]], [[Force scaling component]] |
| `MSLD_obsidian/System Preprocessing Code Break Down.md` | early prep notes (charges) | [[Charge renormalization]] |
| `MSLD_obsidian/T4L peptide example.md` | BLaDE input anatomy | [[BLaDE input script language]], [[BLaDE T4L and HSP90 examples]] |
| `MSLD_obsidian/GUIDE.md` | older copy of GUIDE.md | superseded by the repository `GUIDE.md` (identical except §3.8 and I/O) |
| Claude memory files (earlier sessions) | decisions + findings | [[Project timeline]], ADRs, [[EXP-006 MDM2 theta-parameter sweep\|EXP-006]], [[EXP-007 MDM2 first end-to-end run and benchmark\|EXP-007]] |

Images from the old vault that are still used were copied to `00-meta/attachments`.

