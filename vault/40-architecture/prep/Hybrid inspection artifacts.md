---
title: Hybrid inspection artifacts
type: component
subsystem: "[[Preparation subsystem]]"
layer: L3
status: as-built
code: [msld/prep/assemble/hybrid_output.py, msld/prep/assemble/hub.py]
requirements: ["[[REQ-050 Inspectable prep artifacts|REQ-050]]"]
updated: 2026-09-27
---
# Hybrid inspection artifacts

`bundle.save(out_dir, prefix="hybrid")` writes:
- `hybrid_system.xml` — serialized plain System;
- `hybrid_mapping.json` — the HybridBlueprint;
- `hybrid_topology.pdb` — every site merged into one residue `HYB` (core + all variants' side
  chains), explicit CONECT, CRYST1 box, TER at real chain breaks, atom names unique within 4 chars;
- `hybrid_residue.xml` — a self-contained OpenMM-style FF XML of the hybrid residue (types, charges,
  bonded and nonbonded parameters) read from the plain System — an **inspection** artifact, not a
  loadable molecule.

Why: the engine keeps each variant's block atoms in separate ParmEd residues (ParmEd cannot insert
atoms into an earlier residue), which renders confusingly in viewers. The merged PDB shows the true
picture. Tests: `test_hybrid_output`.

