---
id: FEAT-007
type: feature
title: Atom restraints
status: needs-rework
milestone: M4
implements: ["[[REQ-014 Atom restraints between substituents|REQ-014]]"]
components: ["[[Atom restraint module]]"]
decisions: ["[[ADR-0023 Restraint groups per block centroid|ADR-0023]]", "[[ADR-0033 Atom restraints group equivalent atoms|ADR-0033]]"]
tasks: ["[[TASK-007 Add biases, restraints and constraints|TASK-007]]", "[[TASK-031 Rebuild atom restraint groups|TASK-031]]"]
issues: ["[[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]]", "[[ISS-023 Restrained-atom bonded scaling rule missing|ISS-023]]"]
created: 2026-08-10
updated: 2026-09-27
retrospective: true
---
# FEAT-007 — Atom restraints

Force math correct; group semantics wrong and on by default ([[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]]). Rework in [[TASK-031 Rebuild atom restraint groups|TASK-031]]
per [[ADR-0033 Atom restraints group equivalent atoms|ADR-0033]].

