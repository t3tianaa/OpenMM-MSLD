---
title: Preparation subsystem
type: subsystem
status: as-built
layer: L1
code: [msld/prep/]
requirements: ["[[REQ-040 Ingest Amber, CHARMM, PDB and SDF inputs|REQ-040]]", "[[REQ-041 Lossless parameters including NBFIX|REQ-041]]", "[[REQ-042 Map amino-acid mutation sites|REQ-042]]", "[[REQ-043 Map ligand R-group sites|REQ-043]]", "[[REQ-044 Multiple sites per system|REQ-044]]", "[[REQ-045 Place variant coordinates in the shared frame|REQ-045]]", "[[REQ-046 Consistent charges across variants|REQ-046]]", "[[REQ-047 Solvate and neutralize consistently|REQ-047]]", "[[REQ-048 No bonded term between same-site blocks|REQ-048]]", "[[REQ-049 Prep hands off a plain System and a model|REQ-049]]", "[[REQ-050 Inspectable prep artifacts|REQ-050]]", "[[REQ-051 Validate input geometry|REQ-051]]"]
decisions: ["[[ADR-0015 ParmEd Structure as prep common representation|ADR-0015]]", "[[ADR-0016 Prep emits a plain System|ADR-0016]]", "[[ADR-0017 Staged prep pipeline|ADR-0017]]", "[[ADR-0018 Two ingest modes and NBFIX recovery|ADR-0018]]", "[[ADR-0019 Core defined by identity and equal LJ|ADR-0019]]", "[[ADR-0020 Variants as monomer residues|ADR-0020]]", "[[ADR-0021 Charge averaging, renormalization, iso-charge guard|ADR-0021]]", "[[ADR-0022 Solvation by overlay after grafting|ADR-0022]]"]
issues: ["[[ISS-021 Preparation layer never audited|ISS-021]]", "[[ISS-022 Ingest does not validate geometry|ISS-022]]", "[[ISS-024 Core-only bonded terms take reference parameters|ISS-024]]", "[[ISS-025 NBFIX recovery assumes the OpenMM table convention|ISS-025]]", "[[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]]"]
updated: 2026-09-27
---
# Preparation subsystem

## Purpose
Turn standard molecular inputs and a list of chemical variants into a correct hybrid MSLD system:
one shared environment, one block per variant per site, consistent charges and parameters, aligned
coordinates, optional solvent — handed to the engine as a plain OpenMM System plus the site/block
bookkeeping ([[HybridSystemBundle]]).

## Why it is a subsystem of its own
The alchemical hybrid residue is not a real molecule, so no force field template exists for it.
Each real part (environment, each variant) must be parametrized on its own and then **grafted**.
Doing this correctly (charges, lost parameters, atom correspondence, coordinates) is a large problem
on its own ([[G-3 Automated system preparation|G-3]]).

## Stages (decision [[ADR-0017 Staged prep pipeline|ADR-0017]])

```
 Stage 0  INGEST     any input → one parametrized ParmEd Structure per part      [[Ingest component]]
 Stage 1  MAPPING    per site: which atoms are shared env, which form each block   [[Mapping component]]
 Stage 2  ASSEMBLY   graft blocks, harmonize charges, solvate, build plain System  [[Assembly component]]
 façade   build_msld_system(environment, sites, forcefield=…) runs all stages      [[Prep facade component]]
```

## Key design rules
- ParmEd `Structure` is the one representation inside prep ([[ADR-0015 ParmEd Structure as prep common representation|ADR-0015]]); prefer lossless
  ParmEd-native reads; recover NBFIX after OpenMM→ParmEd hops ([[ADR-0018 Two ingest modes and NBFIX recovery|ADR-0018]]).
- Mapping is explicit per site (`"backbone"` or `"mcs"`); no guessing ([[ADR-0019 Core defined by identity and equal LJ|ADR-0019]]).
- Variants are plain monomer residues, parametrized with `ignoreExternalBonds` ([[ADR-0020 Variants as monomer residues|ADR-0020]]).
- Env charges averaged, blocks renormalized to integers, equal net charge enforced ([[ADR-0021 Charge averaging, renormalization, iso-charge guard|ADR-0021]]).
- Solvate by overlay after grafting; solute indices preserved ([[ADR-0022 Solvation by overlay after grafting|ADR-0022]]).
- Output System is plain; same-site exclusions and all λ scaling belong to the engine ([[ADR-0016 Prep emits a plain System|ADR-0016]]).

## As-built status
Code: `msld/prep/` (~2 400 lines) + 15 test files, all passing. End-to-end on the MDM2 peptide
system (Amber ff14SB, 4 variants, solvated 26 k atoms) ([[FEAT-022 MDM2 test system|FEAT-022]]).

Gaps and risks:
- **Never audited** — the 2026-09-26 audit covered the engine only ([[ISS-021 Preparation layer never audited|ISS-021]], [[TASK-040 Audit the preparation layer|TASK-040]]).
- Emits per-block centroid restraint groups by default — wrong semantics ([[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]]).
- No input-geometry validation ([[ISS-022 Ingest does not validate geometry|ISS-022]]).
- Core-only bonded terms silently take the reference variant's parameters ([[ISS-024 Core-only bonded terms take reference parameters|ISS-024]]).
- NBFIX recovery assumes OpenMM's table convention ([[ISS-025 NBFIX recovery assumes the OpenMM table convention|ISS-025]]).
- No multi-site or ligand system run end to end; no CHARMM hybrid end to end.
- No importer for BLaDE/CHARMM MSLD setups ([[REQ-052 Import a BLaDE or CHARMM MSLD setup|REQ-052]]).

