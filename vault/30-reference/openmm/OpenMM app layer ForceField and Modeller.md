---
title: OpenMM app layer ForceField and Modeller
type: reference
status: verified
system: openmm
version: 8.5.2
related: ["[[Ingest component]]", "[[Solvation]]"]
updated: 2026-09-27
---
# OpenMM app layer: `ForceField`, `Modeller`, PDB

- `ForceField(*ffxml)` matches every residue of a `Topology` to a **template** by its bond graph
  and assigns types, charges and parameters in `createSystem(...)`. Residues without a template
  fail ("No template found").
- `createSystem(ignoreExternalBonds=True)` lets a lone residue match its **mid-chain** template
  (its N and C have no peptide partners) → correct in-chain parameters for a monomer
  (verified in our prep, max |Δq| = 0, [[ADR-0020 Variants as monomer residues|ADR-0020]]).
- `registerTemplateGenerator(gen)` adds on-the-fly templates (GAFF/OpenFF via openmmforcefields).
- `Modeller.addHydrogens(ff)` adds missing H (treats a lone residue as a terminus → adds terminal
  H; do not use on variant monomers).
- `Modeller.addSolvent` needs templates for every solute residue → fails for our hybrid residue,
  hence solvation by overlay ([[ADR-0022 Solvation by overlay after grafting|ADR-0022]]).
- The ffxml → parameters path exists **only in Python**; no C++ library does it (found while
  planning a C++ project, 2026-09-21).

