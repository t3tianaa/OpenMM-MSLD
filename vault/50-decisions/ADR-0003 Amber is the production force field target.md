---
id: ADR-0003
type: adr
title: Amber is the production force field target
status: accepted
date: 2026-08-01
deciders: [Tetiana]
affects: ["[[Preparation subsystem]]", "[[Simulation subsystem]]"]
requirements: ["[[REQ-040 Ingest Amber, CHARMM, PDB and SDF inputs|REQ-040]]", "[[REQ-071 Agree with FEP or TI on Amber|REQ-071]]"]
retrospective: true
---
# ADR-0003 — Amber is the production force field; CHARMM for validation

## Context
The science target uses Amber (ff14SB/ff19SB, GAFF/OpenFF for ligands); BLaDE reads only CHARMM.

## Decision
Production = Amber. CHARMM36 is fully supported by the engine and prep, but used mainly to validate
against BLaDE. The engine stays force-field agnostic by dispatching on OpenMM force types.

## Consequences
- The engine needs both LJ paths (plain LB and CHARMM NBFIX tables) and CHARMM impropers/UB.
- Amber validation needs another oracle (FEP/TI) ([[REQ-071 Agree with FEP or TI on Amber|REQ-071]]).
- ff14SB has identical backbone types and no CMAP → Gly/Pro are side-chain-scope; ff19SB/CHARMM36
  make them backbone mutations ([[Force field functional forms]]).
- Earlier docs over-claimed "force-field agnostic" before CHARMM LJ support existed (corrected
  2026-08-17).

