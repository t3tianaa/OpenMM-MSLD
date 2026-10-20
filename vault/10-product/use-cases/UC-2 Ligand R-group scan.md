---
id: UC-2
type: use-case
title: Ligand R-group scan
status: active
derives_from: ["[[G-1 Free energies for many variants at once|G-1]]", "[[G-3 Automated system preparation|G-3]]", "[[G-5 Meaningful analysis|G-5]]"]
updated: 2026-09-27
---
# UC-2 — Ligand R-group scan

**Actor.** A medicinal chemist with a protein–ligand complex and a series of analogs.

**Flow.** Provide the protein, the reference ligand and analogs as SDF; prep parametrizes each
with GAFF/OpenFF, finds the common scaffold by maximum common substructure, builds one block per
R-group per site; run ALF + production for complex and solvated ligand; report ΔΔG_bind.

**Reference case.** BLaDE `test/HSP90`: 2 sites, 6 + 5 substituents ([[BLaDE T4L and HSP90 examples]]).

**Status.** The MCS mapper exists ([[FEAT-016 Ligand MCS mapper|FEAT-016]]) but no end-to-end ligand system has been built
and run yet.

