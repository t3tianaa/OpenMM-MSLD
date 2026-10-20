---
title: Problem statement
type: product
status: active
updated: 2026-09-27
---
# Problem statement

## The scientific problem

Many questions in drug design and protein engineering are questions about **free-energy
differences** between chemically similar molecules:

- Which of 20 side chains at position 99 makes the protein most stable?
- Which R-group on a ligand scaffold binds the target best?
- Which *combination* of substitutions at 3 positions is optimal?

The rigorous physics-based answer is an **alchemical free-energy calculation**: simulate a
non-physical path that turns molecule A into molecule B and measure the work
([[Alchemical free energy basics]]). Classic methods (FEP, TI) need one set of simulations **per
pair** of molecules. For combinatorial chemistry this explodes: 3 sites × 5 substituents =
125 molecules = hundreds of separate calculations.

**Multi-site λ-dynamics (MSLD)** solves this: all variants at all sites live in **one**
simulation, and continuous λ variables move dynamically to choose which variant is "present"
([[Multisite lambda dynamics]]). One simulation samples the whole combinatorial space, so the cost
grows roughly with the *sum* of substituents, not their *product*.

## The software problem

Today, production MSLD exists only in the CHARMM ecosystem: **CHARMM BLOCK** and **BLaDE**
(the GPU "Basic Lambda Dynamics Engine", [[BLaDE overview]]). Both read only CHARMM inputs and
force fields.

The team wants MSLD in **OpenMM**, because OpenMM:

- runs **Amber** (and other) force fields natively — the production force field of this
  project ([[ADR-0003 Amber is the production force field target|ADR-0003]]);
- is a Python-scriptable, extensible, open-source engine with GPU platforms and a plugin system;
- fits the team's broader tool chain (OpenMM, PyTorch, ML-based sampling).

OpenMM has **no MSLD**. Its alchemical tools (e.g. openmmtools) do FEP/TI with fixed λ, one or two
end states, not λ-dynamics over many sites and substituents. So we must build it.

## Why this is hard

```
 1. ENERGY      every energy term must be scaled by the right λ's, with MSLD's special rules
                (same-site pairs never interact; within-block pairs scale linearly; …)
                — and PME electrostatics mixes all charges on one grid.
 2. FORCES ON λ  the dynamics needs ∂U/∂λ for every block, every step, accurately.
                OpenMM's NonbondedForce does not provide it.
 3. DYNAMICS    atoms and θ (the λ coordinates) must be integrated together, thermostatted
                correctly, at constant pressure.
 4. SAMPLING    raw λ-dynamics collapses into one variant; biases must be learned (ALF) before
                populations mean anything.
 5. PREPARATION building a hybrid system with all variants overlaid, consistent charges and
                force-field parameters, is a large problem on its own.
 6. ANALYSIS    turning λ trajectories into ΔG / ΔΔG with error bars and convergence checks.
 7. TRUST       every piece must be validated against an independent reference, or the
                numbers are worthless.
```

## What went wrong so far (lessons that shape this vault)

The first implementation (July–September 2026) delivered a lot of code quickly, but
([[AUD-001 Engine audit of the local working copy|AUD-001]]):

- features were declared "done" when they only worked at λ = 1 ([[ISS-012 No validation at partial lambda|ISS-012]]);
- a BLaDE feature was re-implemented from its name, not its code ([[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]]);
- conclusions (e.g. "we need a C++ plugin to fix hot θ") rested on one unit convention that was
  never checked ([[ISS-002 Theta mass convention differs from BLaDE|ISS-002]]);
- decisions were scattered across chat sessions and three documents that drifted apart;
- nothing was committed to git for weeks ([[ISS-020 Recent work is uncommitted on one laptop|ISS-020]]).

So the project needs, besides code: explicit requirements with acceptance criteria, documented
decisions, a shared knowledge base, and independent validation. That is what this vault provides.

