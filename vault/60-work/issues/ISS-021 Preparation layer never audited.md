---
id: ISS-021
type: issue
title: Preparation layer never audited
status: open
kind: risk
severity: medium
confidence: confirmed
source: "[[AUD-001 Engine audit of the local working copy|AUD-001]]"
affects: ["[[Preparation subsystem]]"]
requirements: ["[[REQ-040 Ingest Amber, CHARMM, PDB and SDF inputs|REQ-040]]", "[[REQ-046 Consistent charges across variants|REQ-046]]", "[[REQ-042 Map amino-acid mutation sites|REQ-042]]"]
fixed_by: ["[[TASK-040 Audit the preparation layer|TASK-040]]"]
found: 2026-09-26
updated: 2026-09-27
---
# ISS-021 — The preparation layer has never been audited

The 2026-09-26 audit covered the engine; prep (~2 400 lines) got only a quick read while writing this
vault, which already surfaced [[ISS-024 Core-only bonded terms take reference parameters|ISS-024]] and [[ISS-025 NBFIX recovery assumes the OpenMM table convention|ISS-025]] and the ligand-alignment question in
[[Coordinate alignment]]. Plan: [[TASK-040 Audit the preparation layer|TASK-040]].

