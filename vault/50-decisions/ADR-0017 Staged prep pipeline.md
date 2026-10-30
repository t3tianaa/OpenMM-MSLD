---
id: ADR-0017
type: adr
title: Staged prep pipeline
status: accepted
date: 2026-08-18
deciders: [Tetiana]
affects: ["[[Preparation subsystem]]"]
requirements: ["[[REQ-040 Ingest Amber, CHARMM, PDB and SDF inputs|REQ-040]]", "[[REQ-042 Map amino-acid mutation sites|REQ-042]]", "[[REQ-045 Place variant coordinates in the shared frame|REQ-045]]", "[[REQ-048 No bonded term between same-site blocks|REQ-048]]", "[[REQ-049 Prep hands off a plain System and a model|REQ-049]]"]
retrospective: true
---
# ADR-0017 — Staged prep pipeline: ingest → map → assemble

## Context
The first prep (Aug 12–17: `mapping.py`, `charges.py`, `merge.py`, flat modules) grew by accretion.
A redesign plan (`PREP_REDESIGN_PLAN.md`, 2026-08-18, now deleted and folded into GUIDE) split prep
into stages with one data object between them.

## Decision
Stage 0 `DataIngestPipeline` (files → Structure), Stage 1 `Mapper → CoreMapping` (blueprint only),
Stage 2 `HybridSystemAssembler` (graft with aligner, charges, solvate, System) →
`HybridSystemBundle`; a façade `build_msld_system` on top. Variants are residue-level
(backbone + side chain), aligned on the backbone. Three sub-packages `ingest/`, `mapping/`,
`assemble/` (2026-08-19).

## Consequences
- Each stage testable alone; mappers and aligners swappable.
- `merge.py` survives as a helper for term transplant and cross-variant checks.

