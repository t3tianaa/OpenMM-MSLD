---
id: ISS-015
type: issue
title: Cross-site 1-4 and CMAP are refused
status: open
kind: gap
severity: low
confidence: source
source: "[[AUD-001 Engine audit of the local working copy|AUD-001]]"
affects: ["[[1-4 exception scaling module]]", "[[Bonded scaling module]]"]
requirements: ["[[REQ-009 1-4 pair scaling|REQ-009]]", "[[REQ-010 CMAP scaling|REQ-010]]"]
fixed_by: ["[[TASK-052 Cross-site 1-4 scaling|TASK-052]]", "[[TASK-053 CMAP scaling spike|TASK-053]]"]
found: 2026-09-26
updated: 2026-09-27
---
# ISS-015 — Cross-site 1-4 and CMAP are refused (audit F12)

BLaDE scales cross-site 1-4 by λ_iλ_j (only same-site 1-4 is fatal) and scales CMAP with up to 3
λ's. We raise for both. Blocks CHARMM36/ff19SB backbone mutations and adjacent-residue sites.

