---
id: REQ-041
type: requirement
title: Lossless parameters including NBFIX
area: prep
priority: must
status: implemented
derives_from: ["[[G-2 Physically correct MSLD|G-2]]", "[[G-3 Automated system preparation|G-3]]"]
satisfied_by: ["[[FEAT-014 CHARMM NBFIX preservation|FEAT-014]]"]
verified_by: ["test_ingest", "test_prep_solvate"]
decisions: ["[[ADR-0018 Two ingest modes and NBFIX recovery|ADR-0018]]"]
created: 2026-08-17
updated: 2026-09-27
retrospective: true
---
# REQ-041 — Lossless parameters including NBFIX

**Statement.** Every force-field parameter of the input, including CHARMM NBFIX pair overrides,
shall reach the final OpenMM System unchanged (energy of the plain System = energy of a direct
`createSystem` of the same input).

