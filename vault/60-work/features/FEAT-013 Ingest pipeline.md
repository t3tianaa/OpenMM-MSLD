---
id: FEAT-013
type: feature
title: Ingest pipeline
status: done
milestone: M3
implements: ["[[REQ-040 Ingest Amber, CHARMM, PDB and SDF inputs|REQ-040]]"]
components: ["[[Ingest component]]"]
decisions: ["[[ADR-0015 ParmEd Structure as prep common representation|ADR-0015]]", "[[ADR-0018 Two ingest modes and NBFIX recovery|ADR-0018]]"]
tasks: ["[[TASK-015 Prep redesign phases A to I|TASK-015]]"]
issues: ["[[ISS-022 Ingest does not validate geometry|ISS-022]]"]
created: 2026-08-19
updated: 2026-09-27
retrospective: true
---
# FEAT-013 — Ingest pipeline

Router + pipeline + loaders for Amber, CHARMM, PDB+ffxml, SDF+GAFF/OpenFF. Done; geometry validation
missing ([[FEAT-043 Input geometry validation|FEAT-043]]).

