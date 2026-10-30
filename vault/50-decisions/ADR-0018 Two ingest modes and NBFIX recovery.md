---
id: ADR-0018
type: adr
title: Two ingest modes and NBFIX recovery
status: accepted
date: 2026-08-19
deciders: [Tetiana]
affects: ["[[Ingest component]]"]
requirements: ["[[REQ-040 Ingest Amber, CHARMM, PDB and SDF inputs|REQ-040]]", "[[REQ-041 Lossless parameters including NBFIX|REQ-041]]"]
retrospective: true
---
# ADR-0018 — Two ingest modes; prefer lossless reads; recover NBFIX after OpenMM hops

## Decision
- Mode B (parametrized topology: prmtop, psf + params) → ParmEd-native, lossless — preferred.
- Mode A (structure + force field: PDB + ffxml, SDF + GAFF/OpenFF) → OpenMM `createSystem` →
  `load_topology` → `recover_charmm_lj` (no-op for Amber).
- Routing by file extension; force fields only via `forcefield=`, never sniffed from `.xml` paths.
- SDF ⇔ small-molecule FF policy.

## Consequences
- NBFIX survives every route (tested for ion–water in solvation).
- `recover_charmm_lj` is tied to OpenMM's A/B table convention ([[ISS-025 NBFIX recovery assumes the OpenMM table convention|ISS-025]]).

