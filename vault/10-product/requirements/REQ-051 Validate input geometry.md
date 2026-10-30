---
id: REQ-051
type: requirement
title: Validate input geometry
area: prep
priority: should
status: proposed
derives_from: ["[[G-3 Automated system preparation|G-3]]"]
satisfied_by: ["[[FEAT-043 Input geometry validation|FEAT-043]]"]
created: 2026-09-15
updated: 2026-09-27
---
# REQ-051 — Validate input geometry

**Statement.** Ingest shall warn or fail on broken geometry (bond lengths far from equilibrium,
atom overlaps, huge initial energy). Origin: the MDM2 peptide had an OXT 51 Å from its carbon and
nothing complained ([[ISS-022 Ingest does not validate geometry|ISS-022]]).

