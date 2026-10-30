---
title: CoreMapping and HybridBlueprint
type: contract
status: as-built
code: [msld/prep/mapping/core.py]
updated: 2026-09-27
---
# Data contract: `CoreMapping` and `HybridBlueprint`

```python
@dataclass
class CoreMapping:                              # ONE site
    env_atoms: set[int]                         # shared (unscaled) atom indices
    blocks: dict[str, set[int]]                 # {variant_name: atom indices}; one block = one λ
    attachments: list[tuple[int, int]]          # env→block boundary bonds (rings may cross twice)
    align_xform: dict[str, object]              # per-variant rigid transform
    core_charges: dict[int, float]              # reference charge per env atom
    buffer_atoms: set[int]                      # env atoms allowed per-variant charge (⊆ env_atoms)
    core_corresp: dict[str, dict[int, int]]     # {variant: {variant core atom → env atom}}
    atom_names: dict[int, str]; source_names: dict[int, str]
    variant_index_maps: dict[str, dict[int, int]]  # {variant: {variant local → combined index}}
    metadata: dict                              # e.g. {"backbone_mutation": True, "reference": "WT"}
    def validate(self) -> "CoreMapping"          # rejects empty blocks, overlaps, bad indices…
    to_dict / from_dict / to_json / from_json

@dataclass
class HybridBlueprint:                          # all sites of a system
    n_atoms: int
    sites: list[CoreMapping]                    # sites[k] → MSLD site k+1
    def validate(self)                           # indices < n_atoms; no atom in two sites
    global_env → every atom not in a block;  to_model(**kw) → MSLDModel;  JSON round trip
```

Frames: mappers emit residue-local indices; the assembler rewrites them to global hybrid indices.
`core_corresp` is exactly what the correct atom-restraint groups need ([[ADR-0033 Atom restraints group equivalent atoms|ADR-0033]]).

