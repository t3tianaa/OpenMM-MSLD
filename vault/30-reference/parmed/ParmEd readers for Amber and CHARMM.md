---
title: ParmEd readers for Amber and CHARMM
type: reference
status: verified
system: parmed
version: 4.3.1
related: ["[[Ingest component]]"]
updated: 2026-09-27
---
# ParmEd readers for Amber and CHARMM

- `pmd.load_file(prmtop, xyz=inpcrd)` — Amber topology with all parameters; coordinates optional.
  Lossless.
- `pmd.charmm.CharmmPsfFile(psf)` + `CharmmParameterSet(*rtf_prm_str)` +
  `psf.load_parameters(params)` — CHARMM connectivity + parameters, including NBFIX on the atom
  types. Lossless. Coordinates from `pmd.load_file(crd_or_pdb)`.
- `pmd.openmm.load_topology(topology, system, xyz)` — builds a Structure from an OpenMM
  Topology + System (used after OpenMM `ForceField.createSystem`). **Lossy for CHARMM**
  ([[ParmEd round trips and NBFIX loss]]).

Our wrappers: `prep/ingest/pipeline.py:load_amber`, `load_charmm`, `apply_forcefield`
([[Ingest component]]).

