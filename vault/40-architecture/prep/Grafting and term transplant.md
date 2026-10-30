---
title: Grafting and term transplant
type: component
subsystem: "[[Preparation subsystem]]"
layer: L3
status: as-built
code: [msld/prep/assemble/structure.py, msld/prep/assemble/merge.py]
requirements: ["[[REQ-045 Place variant coordinates in the shared frame|REQ-045]]", "[[REQ-048 No bonded term between same-site blocks|REQ-048]]"]
decisions: ["[[ADR-0017 Staged prep pipeline|ADR-0017]]"]
issues: ["[[ISS-024 Core-only bonded terms take reference parameters|ISS-024]]"]
updated: 2026-09-27
---
# Grafting and term transplant

## What happens per site (`HybridStructureBuilder._build_site`)

```
   ●─●─●   backbone (env, stays)          WT side chain: already in the structure → marked as a block
       │
   ○   WT side chain (block, in place)
       ◦   each OTHER variant: align its residue onto the site residue (BackboneAligner),
           APPEND its block atoms (aligned coordinates, unique names) as one new residue on the
           site's chain, map its core atoms onto the existing env indices,
           TRANSPLANT only its block-touching bonded terms (remapped indices)
```

- `merge._transplant_terms` copies bonds, angles, dihedrals, Urey–Bradley, impropers, CMAP and
  1-4 adjusts that touch a block atom; parameter types are cloned once per source type
  (`_TypeCache`). Adjusts must be copied explicitly or an env↔block 1-4 would become a full pair.
- Cross-variant guard: `find/assert/delete_cross_variant_terms` — no term may link two blocks of
  one site (safety net; the grafting never creates one).
- The hybrid starts as `copy.copy(env_structure)` (a full copy, [[ParmEd Structure model]]).

## Assumption to document (and check)
Terms whose atoms are **all core** come from the environment (the reference variant). If a variant
has different parameters for a core-only term (e.g. a backbone torsion that depends on the side
chain type), that difference is lost. For ff14SB backbones this is expected to be harmless;
unverified for CHARMM36 and ligands ([[ISS-024 Core-only bonded terms take reference parameters|ISS-024]]).

