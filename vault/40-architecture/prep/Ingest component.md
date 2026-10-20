---
title: Ingest component
type: component
subsystem: "[[Preparation subsystem]]"
layer: L2
status: as-built
code: [msld/prep/ingest/pipeline.py, msld/prep/ingest/recover.py]
requirements: ["[[REQ-040 Ingest Amber, CHARMM, PDB and SDF inputs|REQ-040]]", "[[REQ-041 Lossless parameters including NBFIX|REQ-041]]", "[[REQ-051 Validate input geometry|REQ-051]]"]
decisions: ["[[ADR-0015 ParmEd Structure as prep common representation|ADR-0015]]", "[[ADR-0018 Two ingest modes and NBFIX recovery|ADR-0018]]", "[[ADR-0020 Variants as monomer residues|ADR-0020]]"]
issues: ["[[ISS-022 Ingest does not validate geometry|ISS-022]]", "[[ISS-025 NBFIX recovery assumes the OpenMM table convention|ISS-025]]"]
updated: 2026-09-27
---
# Ingest component

## Purpose
A funnel: whatever the input format, return **one parametrized `parmed.Structure`** carrying atoms,
types, charges, LJ (incl. NBFIX), all bonded terms, 1-4 adjusts, coordinates and box.

## Interfaces
```python
ingest(*paths, forcefield=None, add_hydrogens=False, coordinates=None,
       ignore_external_bonds=False) -> pmd.Structure
   = DataIngestPipeline().load(resolve_source(...))
load_structure(AmberInput | CharmmInput | ForceFieldInput) -> pmd.Structure
```

## Design
- **Router** `resolve_source` (pure function, no file access): classify paths by extension
  (`.prmtop/.parm7` Amber; `.psf` CHARMM; `.prm/.rtf/.str/.par` params; `.inpcrd/.rst7/.crd/.coor`
  coords; `.pdb`; `.sdf`), reject contradictions (prmtop + psf, sdf + topology, duplicates,
  force field with a parametrized topology), pick coordinates (explicit → coord file → pdb), and
  return a spec dataclass.
- **Pipeline** `DataIngestPipeline.load`: check spec completeness, then file existence, then call:

```
 MODE B (parametrized, LOSSLESS)            MODE A (apply a force field)
 AmberInput  → load_amber (pmd.load_file)   ForceFieldInput → apply_forcefield:
 CharmmInput → load_charmm (psf + params)     PDB + ffxml(s)  or  SDF + ONE small-molecule FF
                                              (policy: SDF ⇔ gaff/openff)
                                              → OpenMM createSystem → load_topology (LOSSY for CHARMM)
                                              → recover_charmm_lj (no-op for Amber/GAFF)
```
- `ignore_external_bonds=True` lets a lone monomer residue match its mid-chain template
  ([[ADR-0020 Variants as monomer residues|ADR-0020]]).
- GAFF/OpenFF via `openmmforcefields` template generators, imported lazily (speed).
- Why SDF only for ligands: amino acids must share the protein's force field and templates; GAFF
  needs bond orders, which PDB lacks.

Theory/reference: [[ParmEd readers for Amber and CHARMM]], [[ParmEd round trips and NBFIX loss]],
[[OpenMM app layer ForceField and Modeller]], [[openmmforcefields template generators]].

## As-built status
`test_ingest.py` covers all routes and error messages. Gaps: GROMACS and frcmod+mol2 routes
([[FEAT-042 Additional ingest routes|FEAT-042]]); no geometry validation (MDM2 OXT 51 Å from its C passed silently, [[ISS-022 Ingest does not validate geometry|ISS-022]]);
`recover_charmm_lj` assumes OpenMM A/B tables ([[ISS-025 NBFIX recovery assumes the OpenMM table convention|ISS-025]]).

