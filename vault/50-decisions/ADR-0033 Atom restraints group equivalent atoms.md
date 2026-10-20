---
id: ADR-0033
type: adr
title: Atom restraints group equivalent atoms
status: proposed
date: 2026-09-27
deciders: [Tetiana]
affects: ["[[Atom restraint module]]", "[[Mapping component]]"]
requirements: ["[[REQ-014 Atom restraints between substituents|REQ-014]]"]
supersedes: ["[[ADR-0023 Restraint groups per block centroid|ADR-0023]]"]
retrospective: false
---
# ADR-0033 — Atom restraint groups are equivalent atoms across substituents (proposed)

## Context
[[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]]: our groups are "all atoms of one block"; BLaDE's are "the same atom in each
substituent of a site" ([[BLaDE atom restraints and soft bonds]]), used when substituents carry
duplicated core atoms (backbone mutations). Plain side-chain mutations use none in BLaDE examples.

## Options
1. Keep per-block groups (wrong physics). 2. **Build groups from the mapping's core
correspondence: for each duplicated core atom, one group = its copies in every block; none when
the core is shared.** 3. Disable restraints entirely until option 2 exists.

## Proposed decision
Option 2, with option 3 as the immediate step: default `add_restraints=False` now; implement
equivalent-atom groups for backbone mutations; configurable k (59.2 kcal/mol/Å² default; note
CHARMM's 59.2·n/(n−1) convention).

## Evidence still needed
- Confirm with BLaDE/ALF inputs for a Gly/Pro site that groups are exactly one atom per
  substituent; check whether ALF-generated protein inputs use `restrain` for side-chain sites.
- Re-run MDM2 without restraints and compare geometry/energies ([[TASK-031 Rebuild atom restraint groups|TASK-031]]).

