---
id: ISS-005
type: issue
title: Unsupported force types silently unscaled
status: open
kind: design-flaw
severity: medium
confidence: source
source: "[[AUD-001 Engine audit of the local working copy|AUD-001]]"
affects: ["[[Force scaling component]]"]
requirements: ["[[REQ-022 Refuse unsupported input loudly|REQ-022]]"]
fixed_by: ["[[TASK-035 Whitelist force types|TASK-035]]"]
found: 2026-09-26
updated: 2026-09-27
---
# ISS-005 — Unsupported force types are silently left unscaled (audit F5)

`builder._check_unhandled` guards only `CMAPTorsionForce`. Alchemical atoms in `GBSAOBCForce`,
`CustomGBForce`, `RBTorsionForce`, AMOEBA forces, pre-existing custom bonded forces or a second
`NonbondedForce` stay at full strength with no error. Fix: whitelist ([[ADR-0037 Whitelist force types|ADR-0037]]).

