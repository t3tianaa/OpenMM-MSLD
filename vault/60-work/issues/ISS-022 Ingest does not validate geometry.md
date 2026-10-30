---
id: ISS-022
type: issue
title: Ingest does not validate geometry
status: open
kind: gap
severity: medium
confidence: confirmed
affects: ["[[Ingest component]]"]
requirements: ["[[REQ-051 Validate input geometry|REQ-051]]"]
fixed_by: ["[[TASK-055 Validate input geometry|TASK-055]]"]
found: 2026-09-15
updated: 2026-09-27
---
# ISS-022 — Ingest silently accepts broken geometry

`mdm2_peptide.pdb` had the C-terminal PRO OXT at (3.905, 4.651, −1.704), ~51 Å from its carbon →
peptide PE = +6.9·10⁶ kJ/mol before any MSLD; nothing warned. Fixed in the file by hand
(2026-09-15, mirrored O across CA–C); the code still does not check.

