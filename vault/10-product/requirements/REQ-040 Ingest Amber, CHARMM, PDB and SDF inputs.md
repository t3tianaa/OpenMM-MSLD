---
id: REQ-040
type: requirement
title: Ingest Amber, CHARMM, PDB and SDF inputs
area: prep
priority: must
status: implemented
derives_from: ["[[G-3 Automated system preparation|G-3]]", "[[UC-1 Protein mutation scan|UC-1]]", "[[UC-2 Ligand R-group scan|UC-2]]"]
satisfied_by: ["[[FEAT-013 Ingest pipeline|FEAT-013]]"]
verified_by: ["test_ingest"]
decisions: ["[[ADR-0015 ParmEd Structure as prep common representation|ADR-0015]]", "[[ADR-0018 Two ingest modes and NBFIX recovery|ADR-0018]]"]
created: 2026-08-19
updated: 2026-09-27
retrospective: true
---
# REQ-040 — Ingest Amber, CHARMM, PDB and SDF inputs

**Statement.** Prep shall read: Amber prmtop (+ coordinates); CHARMM psf + rtf/prm/str
(+ coordinates); PDB + OpenMM ffxml (proteins, incl. non-standard residues with extra ffxml);
SDF + GAFF/OpenFF (ligands) — into one common parametrized representation, with precise errors
for insufficient or contradictory inputs.

## Acceptance criteria
- [x] AC1 — all four routes (`test_ingest`).
- [x] AC2 — routing by extension; contradictory combinations rejected with clear messages.
- [ ] AC3 — GROMACS top/gro and tleap frcmod+mol2 routes ([[FEAT-042 Additional ingest routes|FEAT-042]]) — could.

