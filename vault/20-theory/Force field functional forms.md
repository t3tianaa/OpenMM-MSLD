---
title: Force field functional forms
type: theory
status: reviewed
related: ["[[Lennard-Jones, combining rules and NBFIX]]", "[[ParmEd createSystem mapping to OpenMM forces]]"]
updated: 2026-09-27
---
# Force field functional forms (Amber vs CHARMM)

| term | Amber (ff14SB/ff19SB, GAFF) | CHARMM36 (+CGenFF) | OpenMM force |
|---|---|---|---|
| bonds | harmonic | harmonic | `HarmonicBondForce` |
| Urey–Bradley (1-3) | — | harmonic on 1-3 distance | 2nd `HarmonicBondForce` |
| angles | harmonic | harmonic | `HarmonicAngleForce` |
| proper dihedrals | periodic series | periodic series | `PeriodicTorsionForce` |
| improper dihedrals | periodic | **harmonic** | `PeriodicTorsionForce` / `CustomTorsionForce` |
| CMAP | ff19SB only | yes (protein backbone) | `CMAPTorsionForce` |
| LJ | LB combining rule | LB + NBFIX | `NonbondedForce` / tabulated `CustomNonbondedForce` |
| 1-4 | scaled: scee 1.2, scnb 2.0 | special 1-4 LJ params (ε14, Rmin14), elec ×1.0 | `NonbondedForce` exceptions |
| water | TIP3P (ff14SB), OPC (ff19SB) | CHARMM TIP3P (with H LJ) | — |

Facts that drove our design (verified in the prep work, see [[Mapping component]]):
- ff14SB backbone atom types are identical across residues and there is no CMAP → Gly/Pro
  mutations are clean side-chain mutations.
- CHARMM36 and ff19SB have residue-specific backbone types and CMAP → Gly/Pro become backbone
  mutations, hitting the CMAP guard ([[REQ-010 CMAP scaling|REQ-010]]).
- Charges: CHARMM backbone charges are standardized; Amber charges are RESP-fitted per residue →
  shared atoms can differ across variants → averaging ([[Charge renormalization]]).

