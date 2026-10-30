---
id: ADR-0022
type: adr
title: Solvation by overlay after grafting
status: accepted
date: 2026-08-17
deciders: [Tetiana]
affects: ["[[Solvation]]"]
requirements: ["[[REQ-047 Solvate and neutralize consistently|REQ-047]]"]
retrospective: true
---
# ADR-0022 — Solvate by overlay after grafting

## Context
`Modeller.addSolvent` requires templates for all solute residues; the hybrid residue has none.
tleap is not installed and cannot read our hybrid either.

## Decision
Build a pure water box, overlay, delete clashing waters (KD-tree), convert the farthest waters to
counter-ions; append after the solute so solute indices are unchanged.

## Consequences
- Works for any hybrid; indices stable; CHARMM water LJ recovered.
- Water/ion force field must be chosen to match the solute FF manually (no check).
- Box is cubic with padding; no pre-equilibration of the combined system.

