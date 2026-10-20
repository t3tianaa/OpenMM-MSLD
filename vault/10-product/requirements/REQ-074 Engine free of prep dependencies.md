---
id: REQ-074
type: requirement
title: Engine free of prep dependencies
area: process
priority: should
status: implemented
derives_from: ["[[G-6 Traceable engineering process|G-6]]"]
decisions: ["[[ADR-0030 Hard dependencies and a ParmEd-free engine|ADR-0030]]"]
created: 2026-08-19
updated: 2026-09-27
retrospective: true
---
# REQ-074 — Engine free of prep dependencies

**Statement.** The engine modules import only openmm and numpy, so an existing OpenMM System can be
run with MSLD without ParmEd/RDKit/openmmforcefields.
