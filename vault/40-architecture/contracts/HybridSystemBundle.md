---
title: HybridSystemBundle
type: contract
status: as-built
code: [msld/prep/assemble/hub.py]
updated: 2026-09-27
---
# Data contract: `HybridSystemBundle` (prep → engine hand-off)

```python
@dataclass
class HybridSystemBundle:
    structure: pmd.Structure       # hybrid solute (+ solvent), charges final
    system: openmm.System          # PLAIN: not λ-scaled, no same-site exclusions
    mapping: HybridBlueprint       # global indices (after solvation)
    reports: …                     # charge reports etc.
    def to_model(self, **kw) -> MSLDModel      # fnex, add_restraints, block_options
    def save(self, out_dir, prefix="hybrid")   # system.xml, mapping.json, topology.pdb, residue.xml
```

The engine consumes exactly `bundle.system` and `bundle.to_model()`; positions come from
`bundle.structure.positions`.

