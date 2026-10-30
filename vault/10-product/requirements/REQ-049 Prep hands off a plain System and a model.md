---
id: REQ-049
type: requirement
title: Prep hands off a plain System and a model
area: prep
priority: must
status: implemented
derives_from: ["[[G-3 Automated system preparation|G-3]]"]
satisfied_by: ["[[FEAT-020 System build and bundle outputs|FEAT-020]]"]
verified_by: ["test_hybrid_system", "test_build"]
decisions: ["[[ADR-0016 Prep emits a plain System|ADR-0016]]"]
created: 2026-08-19
updated: 2026-09-27
retrospective: true
---
# REQ-049 — Prep hands off a plain System and an MSLD model

**Statement.** Prep's output is a `HybridSystemBundle`: the hybrid structure, a **plain** OpenMM
System (not λ-scaled, no same-site exclusions) and a serializable mapping that converts into an
`MSLDModel` ([[HybridSystemBundle]]). The engine applies all MSLD changes.

