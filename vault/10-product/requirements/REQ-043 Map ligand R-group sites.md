---
id: REQ-043
type: requirement
title: Map ligand R-group sites
area: prep
priority: must
status: partial
derives_from: ["[[UC-2 Ligand R-group scan|UC-2]]"]
satisfied_by: ["[[FEAT-016 Ligand MCS mapper|FEAT-016]]"]
verified_by: ["test_mcs"]
decisions: ["[[ADR-0019 Core defined by identity and equal LJ|ADR-0019]]"]
created: 2026-08-19
updated: 2026-09-27
retrospective: true
---
# REQ-043 — Map ligand R-group sites

**Statement.** For a reference ligand and analogs, find the common scaffold by maximum common
substructure (element match, rings kept whole, optional LJ-type agreement), refuse partial-ring
cores, and split each analog into core + R-group block(s), including multiple sites on one scaffold.

## Acceptance criteria
- [x] AC1 — MCS core found; ring-break guard (`test_mcs`).
- [ ] AC2 — multi-site ligand (≥ 2 R-group positions) end to end.
- [ ] AC3 — a real ligand series (e.g. HSP90) built and run.

