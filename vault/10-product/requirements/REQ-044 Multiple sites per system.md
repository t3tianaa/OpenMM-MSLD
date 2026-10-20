---
id: REQ-044
type: requirement
title: Multiple sites per system
area: prep
priority: must
status: partial
derives_from: ["[[UC-1 Protein mutation scan|UC-1]]", "[[UC-2 Ligand R-group scan|UC-2]]", "[[UC-5 Explore combinatorial chemical space|UC-5]]"]
satisfied_by: ["[[FEAT-017 Hybrid structure grafting|FEAT-017]]"]
verified_by: ["test_mapping_core"]
created: 2026-08-19
updated: 2026-09-27
retrospective: true
---
# REQ-044 — Multiple sites per system

**Statement.** Prep shall build systems with several independent sites (no atom in two sites) and
emit one model with all of them. Status: data structures support it (`HybridBlueprint`); no
multi-site system has been built and run end to end.

