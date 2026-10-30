---
id: ADR-0019
type: adr
title: Core defined by identity and equal LJ
status: accepted
date: 2026-08-19
deciders: [Tetiana]
affects: ["[[Mapping component]]"]
requirements: ["[[REQ-042 Map amino-acid mutation sites|REQ-042]]", "[[REQ-043 Map ligand R-group sites|REQ-043]]"]
retrospective: true
---
# ADR-0019 — Core = same identity AND same LJ; name matching for peptides, MCS for ligands

## Context
Env atoms are unscaled, so they carry one LJ set; charges can be harmonized later. Type-name
strings are unreliable after OpenMM→ParmEd hops (synthesized names like "O2D" vs "O1").

## Decision
- An atom is core iff it is present (once) in every variant and its LJ (element + σ + ε) is equal.
- Peptides: identity = atom name (`AminoAcidBackboneMapper`).
- Ligands: identity = RDKit MCS position (element-only graph, rings whole, ring-break guard).
- The mapper is always explicit per site — no auto-detection.

## Consequences
- Backbone atoms with residue-specific types (CHARMM36, ff19SB) drop out of the core → flagged as
  backbone mutations (needs duplicated backbones + restraints, not yet supported end to end).
- Earlier "same type string" rule caused duplicated backbone O atoms — fixed by comparing LJ values.

