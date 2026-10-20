---
id: UC-1
type: use-case
title: Protein mutation scan
status: active
derives_from: ["[[G-1 Free energies for many variants at once|G-1]]", "[[G-3 Automated system preparation|G-3]]", "[[G-5 Meaningful analysis|G-5]]"]
updated: 2026-09-27
---
# UC-1 — Protein mutation scan

**Actor.** A researcher with a protein (or protein–peptide complex) structure.

**Flow.**
1. Provide the environment (PDB + Amber ffxml, or prmtop, or CHARMM psf + parameters).
2. Choose the site residue(s) and the candidate amino acids (as monomer PDB residues).
3. Prep builds the hybrid system and solvates it ([[Preparation subsystem]]).
4. Run ALF to flatten, then production MSLD, for the complex and for the reference state
   (unbound peptide, or unfolded model).
5. Analysis reports ΔG per variant per leg, ΔΔG, uncertainties, convergence.

**Example in the repo.** MDM2 + peptide, site = peptide residue 4, variants ILE/LEU/SER/VAL
([[FEAT-022 MDM2 test system|FEAT-022]]). Reference literature case: T4 lysozyme residue 99 / 149 ([[BLaDE T4L and HSP90 examples]]).

**Special cases.** Gly and Pro change the backbone (residue-specific backbone types, CMAP in
CHARMM36/ff19SB) → backbone mutation flag; needs extra handling ([[FEAT-036 CMAP scaling|FEAT-036]], [[ISS-015 Cross-site 1-4 and CMAP are refused|ISS-015]]).

