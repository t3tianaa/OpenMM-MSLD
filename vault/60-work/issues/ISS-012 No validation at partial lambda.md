---
id: ISS-012
type: issue
title: No validation at partial lambda
status: open
kind: risk
severity: high
confidence: confirmed
source: "[[AUD-001 Engine audit of the local working copy|AUD-001]]"
affects: ["[[Force scaling component]]", "[[Simulation subsystem]]"]
requirements: ["[[REQ-070 Agree with BLaDE on a shared CHARMM system|REQ-070]]", "[[REQ-072 Every feature has an automated test|REQ-072]]"]
fixed_by: ["[[TASK-067 NumPy partial-lambda oracle tests|TASK-067]]", "[[TASK-043 BLaDE fixed-lambda cross-check|TASK-043]]"]
found: 2026-09-26
updated: 2026-09-27
---
# ISS-012 — Nothing validates partial-λ energies or θ statistics against an independent implementation

Nearly all engine tests run on Reference with toy systems; the master invariant is checked only at
λ = 1 (not a physical state); partial-λ checks compare the code with its own finite differences. No
test compares partial-λ energies/derivatives with an independent calculation, and none checks λ
distributions in a real system. The C++ plugin plan would reproduce any such error faithfully.

Mitigation: [[FEAT-045 Independent partial-lambda oracle tests|FEAT-045]] (NumPy oracle, cheap) and [[FEAT-030 BLaDE cross-validation harness|FEAT-030]] (BLaDE cross-check).

