---
id: TASK-029
type: task
title: Build the project knowledge vault
status: review
kind: docs
priority: P0
milestone: M4
feature: "[[FEAT-044 Knowledge vault and process|FEAT-044]]"
refs: ["[[Conventions]]", "[[Workflow]]", "[[Agent protocol]]"]
created: 2026-09-27
---
# TASK-029 — Build the project knowledge vault

## Goal
Design and populate this vault: conventions, product layer, theory KB, reference KB, architecture,
ADRs, work items, verification, history — migrated from all existing sources ([[ADR-0031 Project knowledge system in an Obsidian vault|ADR-0031]]).

## Acceptance criteria
- [x] structure, conventions, templates, dashboards, link checker
- [x] problem, goals, use cases, requirements with acceptance criteria
- [x] theory notes for every concept the code relies on
- [x] reference notes for OpenMM, BLaDE, ParmEd with file:line
- [x] architecture from L0 to L3 with as-built status
- [x] retrospective ADRs + proposed ADRs for open decisions
- [x] features, tasks, issues reconstructed; audit findings linked
- [ ] owner review; commit on a branch ([[TASK-030 Commit and push the local state to a branch|TASK-030]]); CLAUDE.md pointer ([[TASK-072 Point agents to the vault via CLAUDE.md|TASK-072]])

## Log
- 2026-09-27 — built by Claude from the local folder, the old vault, the audit, BLaDE source and
  earlier session memory. Not reviewed yet.
