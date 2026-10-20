---
id: ADR-0041
type: adr
title: Default bonded scaling follows BLaDE practice
status: proposed
date: 2026-09-27
deciders: [Tetiana]
affects: ["[[Bonded scaling module]]", "[[MSLD model component]]"]
requirements: ["[[REQ-004 Configurable bonded scaling per term type|REQ-004]]"]
supersedes: ["[[ADR-0014 Bonded scaling on by default|ADR-0014]]"]
retrospective: false
---
# ADR-0041 — Default bonded scaling follows BLaDE `removescaling` practice (proposed)

## Proposed decision
- Split the switches into BLaDE's six: bond, urey, angle, dihe, impr, cmap.
- Default: **not scaled** = bond, urey, angle (BLaDE doc: "at least bond and angle are recommended");
  dihe and impr scaled by default (T4L peptide example) — user sets per system.
- Tests that exercise scaling set the flags explicitly.
- Implement BLaDE's restrained-atom exception ([[ISS-023 Restrained-atom bonded scaling rule missing|ISS-023]]).

## Evidence still needed
Which removescaling set ALF-generated protein inputs use (T4L149F: bond urey angle impr; HSP90
ligands: bond urey angle dihe impr).
