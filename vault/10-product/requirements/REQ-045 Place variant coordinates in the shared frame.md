---
id: REQ-045
type: requirement
title: Place variant coordinates in the shared frame
area: prep
priority: must
status: implemented
derives_from: ["[[G-3 Automated system preparation|G-3]]"]
satisfied_by: ["[[FEAT-017 Hybrid structure grafting|FEAT-017]]"]
verified_by: ["test_aligner", "test_hybrid_builder"]
decisions: ["[[ADR-0017 Staged prep pipeline|ADR-0017]]"]
created: 2026-08-19
updated: 2026-09-27
retrospective: true
---
# REQ-045 — Place variant coordinates in the shared frame

**Statement.** Each variant's block atoms shall be placed by rigid superposition of its core atoms
(backbone N, CA, C, O for amino acids) onto the environment's core ([[Kabsch superposition]]).

