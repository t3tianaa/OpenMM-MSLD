---
id: REQ-042
type: requirement
title: Map amino-acid mutation sites
area: prep
priority: must
status: implemented
derives_from: ["[[UC-1 Protein mutation scan|UC-1]]"]
satisfied_by: ["[[FEAT-015 Peptide backbone mapper|FEAT-015]]"]
verified_by: ["test_backbone_mapper", "test_hybrid_builder"]
decisions: ["[[ADR-0019 Core defined by identity and equal LJ|ADR-0019]]", "[[ADR-0020 Variants as monomer residues|ADR-0020]]"]
created: 2026-08-19
updated: 2026-09-27
retrospective: true
---
# REQ-042 — Map amino-acid mutation sites

**Statement.** For a residue site and a set of candidate amino acids, find the shared core (atoms
with the same name and the same LJ parameters in every variant) and the per-variant blocks; flag
backbone mutations (Gly/Pro, residue-specific backbone types); support non-standard residues.

## Acceptance criteria
- [x] AC1 — WT block fully on reproduces the untouched peptide energy (`test_hybrid_builder`, 3e-15).
- [x] AC2 — backbone-mutation flag.
- [ ] AC3 — Gly/Pro handled end to end (duplicated backbone + atom restraints + soft bonds, as in
  BLaDE RNaseH inputs) ([[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]], [[ISS-015 Cross-site 1-4 and CMAP are refused|ISS-015]]).

