---
title: Prep facade component
type: component
subsystem: "[[Preparation subsystem]]"
layer: L2
status: as-built
code: [msld/prep/build.py]
requirements: ["[[REQ-049 Prep hands off a plain System and a model|REQ-049]]"]
decisions: ["[[ADR-0020 Variants as monomer residues|ADR-0020]]"]
updated: 2026-09-27
---
# Prep façade — `build_msld_system`

```python
bundle = build_msld_system(
    environment="complex.pdb" | Part(...) | Structure,
    sites=[Site(residue=<index into env.residues> | [atom indices],
                variants={"ILE": "ILE_var.pdb", "LIG2": Part("lig2.sdf", forcefield=["gaff-2.11"])},
                mapper="backbone" | "mcs" | Mapper, reference_name="WT")],
    forcefield=["amber14-all.xml"], renormalize=True, solvate=True)
model = bundle.to_model()          # → MSLDModel
```

- `Part(path, forcefield=None, extra_forcefield=None, add_hydrogens=False, ignore_external_bonds=None)`
  lets each molecule carry its own force field (non-standard residue XML, ligand FF).
- Variants default to `ignore_external_bonds=True` (monomers), the environment to False.
- The reference (WT) side chain already in the environment competes as a block automatically.

Name clash to remember: `build_msld_system` = prep façade; `scale_msld_system` /
`MSLDModel.scale_system` = engine entry.

Example: `test_systems/mdm2/mdm2_run.py` ([[FEAT-022 MDM2 test system|FEAT-022]]).
