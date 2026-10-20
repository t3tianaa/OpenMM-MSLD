---
id: FEAT-020
type: feature
title: System build and bundle outputs
status: done
milestone: M3
implements: ["[[REQ-049 Prep hands off a plain System and a model|REQ-049]]", "[[REQ-050 Inspectable prep artifacts|REQ-050]]"]
components: ["[[Plain System builder]]", "[[Hybrid inspection artifacts]]", "[[HybridSystemBundle]]"]
decisions: ["[[ADR-0016 Prep emits a plain System|ADR-0016]]"]
tasks: ["[[TASK-015 Prep redesign phases A to I|TASK-015]]", "[[TASK-022 Fix hybrid output artifacts|TASK-022]]"]
created: 2026-08-19
updated: 2026-09-27
retrospective: true
---
# FEAT-020 — System build and bundle outputs

Plain System via ParmEd `createSystem`; `HybridSystemBundle` with `to_model()` and `save()` (XML,
JSON, merged-HYB PDB, residue FF XML).

