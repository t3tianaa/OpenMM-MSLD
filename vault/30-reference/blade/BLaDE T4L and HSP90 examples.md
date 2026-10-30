---
title: BLaDE T4L and HSP90 examples
type: reference
status: verified
system: blade
version: c677277
related: ["[[BLaDE input script language]]", "[[UC-1 Protein mutation scan|UC-1]]", "[[UC-2 Ligand R-group scan|UC-2]]"]
updated: 2026-09-27
---
# BLaDE example systems (T4L, HSP90, RNaseH)

Source: `test/` in the BLaDE repository. These are the natural validation targets ([[FEAT-030 BLaDE cross-validation harness|FEAT-030]]).

| example | what | sites × substituents | notable settings |
|---|---|---|---|
| `T4L_peptide` | peptide from T4 lysozyme, residue 99 | 1 × 6 (nat, ala, phe, ile, met, val) | removescaling bond angle; softcore on; θ mass 5; ready-made `minimized.psf/pdb` |
| `T4L` | T4 lysozyme residue 149 (prep script `T4L149F.inp`) | 1 × several | removescaling bond urey angle impr; softcore on, softcore14 off |
| `HSP90` | ligand series (`cb7.inp`) | 2 × (6, 5) | removescaling bond urey angle dihe impr; softcore on; ALF biases 6/10/8 per pair; θ mass 5; `msld gamma 1.0`; atom `gamma 0.1`; dt 2 fs; freqnpt 100; freqlmd 10 |
| `RNaseH` | multi-site protein design incl. Pro | several | backbone restraints `msld restrain site{n}consN…`, krestraint 118.4, Pro soft bond CB–CG |

## How a CHARMM MSLD system is prepared (from `T4L99U.inp`, old notes)
1. Load MSLD topology/parameters (`top_all36_msld.rtf`, `par_all36_msld.prm`) and per-amino-acid
   patch streams (`aa_stream/ca_*.str`) that graft a side chain onto a Cα.
2. Build the native protein; `patch ca_<aa>` for each variant at the site; `ic build` coordinates.
   Each variant's atoms get a suffix letter (`CBA`, `CBF`, …) so they coexist in one PSF.
3. Define selections per substituent (native = residue minus backbone minus mutants).
4. Delete bonded terms between different variants; regenerate angles/dihedrals.
5. Add solvent and ions, set the box, minimize, write `minimized.psf/pdb`.
6. BLaDE input: `msld call`, `initialize`, biases, run.

Not all toppar/stream files referenced by the T4L CHARMM script are in the repo, so the prep script
cannot be re-run as is; the minimized PSF/PDB can be used directly.

Old-notes figures of the T4L input:
![[Pasted image 20260812120252.png]]
![[Pasted image 20260812122833.png|500]]
![[Pasted image 20260812123115.png]]
![[Pasted image 20260812123152.png|500]]
![[Pasted image 20260812123228.png]]
