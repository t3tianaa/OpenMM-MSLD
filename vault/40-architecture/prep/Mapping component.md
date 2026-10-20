---
title: Mapping component
type: component
subsystem: "[[Preparation subsystem]]"
layer: L2
status: as-built
code: [msld/prep/mapping/core.py, msld/prep/mapping/backbone.py, msld/prep/mapping/mcs.py]
requirements: ["[[REQ-042 Map amino-acid mutation sites|REQ-042]]", "[[REQ-043 Map ligand R-group sites|REQ-043]]", "[[REQ-044 Multiple sites per system|REQ-044]]"]
decisions: ["[[ADR-0019 Core defined by identity and equal LJ|ADR-0019]]"]
issues: ["[[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]]"]
updated: 2026-09-27
---
# Mapping component

## Purpose
Per site, decide which atoms are the shared **environment core** and which atoms form each
competing **block**, as a force-field-agnostic [[CoreMapping and HybridBlueprint|CoreMapping]].

```
 variant WT  :  ●─●─●─○○        ● shared core (env) → present once, never λ-scaled
 variant MUT :  ●─●─●─◦◦◦       ○/◦ block atoms      → each block has its own λ
```

## Interfaces
```python
class Mapper(ABC):
    def get_mapping(self, reference=None, variants=None) -> CoreMapping
AminoAcidBackboneMapper(reference_name="WT")   # peptides
MCSMapper(reference_name=…, match_types=True, reject_ring_break=True)   # ligands
ManualMapper(env_atoms, blocks, …)             # explicit / tests
model_from_mappings(n_atoms, mappings, fnex=5.5, add_restraints=True) -> MSLDModel
```

## Design
- **Core rule (both mappers):** an atom is core iff it appears in every variant and has the same
  **LJ parameters** (element + σ + ε) everywhere — env atoms are unscaled so they carry one LJ set.
  Charges may differ (averaged later). Comparing LJ values, not type names, because OpenMM→ParmEd
  hops synthesize type names ([[ADR-0019 Core defined by identity and equal LJ|ADR-0019]]).
- **Peptides** (`AminoAcidBackboneMapper`): match by atom **name**, exactly once per variant, same
  LJ; flag `backbone_mutation` if N/CA/C/O fall out of the core (Gly/Pro under CHARMM36/ff19SB).
- **Ligands** (`MCSMapper`): RDKit MCS on element-only single-bond graphs, rings whole; optional LJ
  filter; **ring-break guard** refuses a core that cuts a ring ([[Maximum common substructure mapping]]).
- Both feed one shared assembly function `build_hybrid_local_mapping` (core slots 0..E−1, then
  each variant's non-core atoms, renamed uniquely), in a **residue-local** frame; the assembler
  converts to global indices.
- `model_from_mappings` builds the `MSLDModel`: blocks in site order, then variant order; **and adds
  one restraint group per block (all its atoms)** when `add_restraints=True` (default) — this is the
  wrong restraint semantics ([[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]], [[ADR-0033 Atom restraints group equivalent atoms|ADR-0033]]).

## As-built status
Tests: `test_mapping_core`, `test_backbone_mapper`, `test_mcs`, `test_prep_mapping`.
Gaps: restraint groups ([[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]]); backbone mutations produce no duplicated-backbone
restraints or soft bonds (BLaDE RNaseH style); multi-site ligand scaffolds untested.

