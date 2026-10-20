---
title: RDKit MCS
type: reference
status: verified
system: rdkit
version: 2025.09.6
related: ["[[Maximum common substructure mapping]]", "[[Mapping component]]"]
updated: 2026-09-27
---
# RDKit maximum common substructure (`rdFMCS`)

`rdFMCS.FindMCS(mols, atomCompare=…, bondCompare=…, ringMatchesRingOnly=…, completeRingsOnly=…,
timeout=…)` returns a SMARTS of the MCS; `mol.GetSubstructMatch(query)` maps it to atom indices.

Our usage (`prep/mapping/mcs.py`): element-only, all-single-bond graphs built from ParmEd bonds
(bond orders are not reliable there), **not sanitized** (valences can be non-physical);
ring info initialized with `UpdatePropertyCache(strict=False)` + `Chem.FastFindRings` — without it
`GetSubstructMatch` fails with "RingInfo not initialized" (bug found and fixed 2026-08-21).
`CompareElements` + `CompareAny`, rings kept whole.

