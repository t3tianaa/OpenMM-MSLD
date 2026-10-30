---
title: Hybrid and multiple topologies
type: theory
status: reviewed
related: ["[[Multisite lambda dynamics]]", "[[Maximum common substructure mapping]]"]
updated: 2026-09-27
---
# Hybrid and multiple topologies

**In one sentence.** Alchemical methods differ in how the atoms of the end states coexist in one
simulation.

| topology | idea | used by |
|---|---|---|
| single topology | one set of atoms whose parameters morph (types, charges) | classic FEP |
| dual topology | both molecules present as separate copies, each scaled | many RBFE tools |
| **hybrid / multiple topology** | shared core atoms present once; each variant's unique atoms present as its own group | **MSLD** |

MSLD: the core (environment) is shared; each substituent is a block of its own atoms, all blocks
present simultaneously and overlapping in space, interacting with the core but never with each
other at the same site. The core must be chosen so that core atoms have identical LJ parameters in
all variants (they are unscaled); charges may differ and are harmonized
([[Charge renormalization]]).

Where to cut: MSLD assumes pendant substituents; cutting through a ring is invalid
([[Maximum common substructure mapping]]). Charge-renormalization and "buffer atoms" at the
junction are how the core's charges are made consistent ([[Net charge changes in alchemical calculations]]).

