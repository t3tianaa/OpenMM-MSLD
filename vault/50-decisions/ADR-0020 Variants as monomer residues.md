---
id: ADR-0020
type: adr
title: Variants as monomer residues
status: accepted
date: 2026-09-01
deciders: [Tetiana]
affects: ["[[Ingest component]]", "[[Prep facade component]]"]
requirements: ["[[REQ-042 Map amino-acid mutation sites|REQ-042]]"]
retrospective: true
---
# ADR-0020 — Variants are plain monomer residues parametrized with `ignoreExternalBonds`

## Context
A lone amino acid has no template (its N/C lack peptide partners). The first solution capped
variants (ACE/NME) and stripped the caps (`Part.caps`, `strip_caps`).

## Decision
Supply each variant as a plain monomer PDB residue (with in-chain hydrogens) and parametrize with
`createSystem(ignoreExternalBonds=True)` so the mid-chain template matches. The caps machinery was
removed.

## Consequences
- Correct in-chain types and charges (verified max |Δq| = 0 vs the residue in a full chain), no OXT
  or terminal H.
- Do not run `addHydrogens` on a variant (it treats it as a terminus).

