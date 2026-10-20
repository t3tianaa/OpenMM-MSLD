---
title: Bonded terms and dummy atoms in alchemy
type: theory
status: reviewed
related: ["[[Alchemical scaling rules in MSLD]]", "[[BLaDE bonded term scaling]]"]
updated: 2026-09-27
---
# Bonded terms and dummy atoms in alchemy

**In one sentence.** A disappearing substituent should lose its *interactions with the rest of the
system* but keep its *internal geometry and attachment*, so it stays a well-behaved "dummy".

## The problem with scaling bonds and angles

If bonds and angles of a block are multiplied by λ_b, then at λ_b → 0 the block loses the bonds
that attach it to the core; it drifts away and must be pulled back when λ rises again (large
forces, slow sampling). Measured in our MDM2 run: an ILE side chain drifted from 2.8 to 4.8 Å from
CB with bond/angle scaling on, 2.8 → 2.9 Å with it off ([[EXP-007 MDM2 first end-to-end run and benchmark|EXP-007]]).

## Why not scaling is still exact

A term that stays at full strength in every λ state contributes the same free energy in both legs
of the thermodynamic cycle (as long as it does not couple the dummy to the environment's
conformations in a leg-dependent way). Standard practice: do **not** scale bonds, angles (and
often dihedrals and impropers) of alchemical groups; scale nonbonded interactions.

## BLaDE practice (from example inputs)

| example | removescaling (terms NOT scaled) |
|---|---|
| HSP90 ligands (`cb7.inp`) | bond urey angle dihe impr |
| T4L protein (`T4L149F.inp`) | bond urey angle impr (dihedrals scaled) |
| T4L peptide (`input`) | bond angle (urey, dihe, impr, cmap scaled) |

BLaDE's help text: "At least bond and angle are recommended." Our engine default scales everything;
the MDM2 script turns bond + angle off ([[ISS-014 Bonded scaling defaults differ from BLaDE|ISS-014]], [[ADR-0014 Bonded scaling on by default|ADR-0014]], [[ADR-0041 Default bonded scaling follows BLaDE practice|ADR-0041]]).

## Subtlety: restrained atoms
In BLaDE, a term type that is *not* scaled is still scaled if **all** of its same-block atoms are
restrained atoms (atom restraints) — so duplicated backbone atoms tied by restraints keep scaled
bonded terms ([[BLaDE bonded term scaling]], [[ISS-023 Restrained-atom bonded scaling rule missing|ISS-023]]).

