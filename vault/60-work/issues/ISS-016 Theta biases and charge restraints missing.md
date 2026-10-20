---
id: ISS-016
type: issue
title: Theta biases and charge restraints missing
status: open
kind: gap
severity: low
confidence: source
source: "[[AUD-001 Engine audit of the local working copy|AUD-001]]"
affects: ["[[Bias module]]"]
requirements: ["[[REQ-013 Theta biases|REQ-013]]", "[[REQ-015 Charge-changing perturbations|REQ-015]]"]
fixed_by: ["[[TASK-051 Implement theta biases|TASK-051]]", "[[TASK-054 Charge-changing perturbations|TASK-054]]"]
found: 2026-09-26
updated: 2026-09-27
---
# ISS-016 — θ biases and charge restraints are not implemented (audit F12)

Needed for many-substituent sites (FPL) and charge-changing perturbations respectively; BLaDE also
has variable-bias types 1–5, 7, 9, 11, 12 that we lack.

