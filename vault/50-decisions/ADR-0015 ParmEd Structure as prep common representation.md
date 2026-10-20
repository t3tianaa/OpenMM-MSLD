---
id: ADR-0015
type: adr
title: ParmEd Structure as prep common representation
status: accepted
date: 2026-08-14
deciders: [Tetiana]
affects: ["[[Preparation subsystem]]", "[[Ingest component]]"]
requirements: ["[[REQ-040 Ingest Amber, CHARMM, PDB and SDF inputs|REQ-040]]", "[[REQ-041 Lossless parameters including NBFIX|REQ-041]]"]
retrospective: true
---
# ADR-0015 — ParmEd `Structure` as prep's common representation

## Context
Inputs arrive as prmtop, psf + parameters, PDB + ffxml, SDF + GAFF. Grafting needs atom- and
term-level editing with parameter types; OpenMM `System` has no topology/types; OpenMM `Topology`
has no parameters.

## Options
1. OpenMM Topology + System pairs. 2. **ParmEd Structure** (reads Amber and CHARMM natively; editable
terms and types; lossless `createSystem`). 3. Own data structure.

## Decision
Option 2. Every ingest route returns a parametrized `parmed.Structure`; mapping and assembly work
on it; `createSystem` produces the plain System.

## Consequences
- Lossless for Amber/CHARMM native reads; NBFIX preserved.
- The OpenMM→ParmEd direction is lossy for CHARMM → recovery needed ([[ADR-0018 Two ingest modes and NBFIX recovery|ADR-0018]]).
- Prep depends on ParmEd (4.3.1); the engine must not ([[ADR-0030 Hard dependencies and a ParmEd-free engine|ADR-0030]]).
- Units switch (Å/kcal inside ParmEd).

