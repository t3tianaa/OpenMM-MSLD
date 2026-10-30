---
id: REQ-050
type: requirement
title: Inspectable prep artifacts
area: prep
priority: should
status: implemented
derives_from: ["[[G-3 Automated system preparation|G-3]]", "[[G-6 Traceable engineering process|G-6]]"]
satisfied_by: ["[[FEAT-020 System build and bundle outputs|FEAT-020]]"]
verified_by: ["test_hybrid_output"]
created: 2026-09-15
updated: 2026-09-27
retrospective: true
---
# REQ-050 — Inspectable prep artifacts

**Statement.** Save the serialized System, mapping JSON, a viewer-friendly PDB (merged hybrid
residue, CONECT, CRYST1, TER at chain breaks) and a force-field XML of the hybrid residue, so a
human can inspect every atom, charge and parameter.

