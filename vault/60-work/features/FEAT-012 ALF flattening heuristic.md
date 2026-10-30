---
id: FEAT-012
type: feature
title: ALF flattening heuristic
status: needs-rework
milestone: M6
implements: ["[[REQ-030 Adaptive landscape flattening|REQ-030]]", "[[REQ-060 Free energy per variant with uncertainty|REQ-060]]"]
components: ["[[ALF flattening component]]"]
decisions: ["[[ADR-0024 Home-grown ALF heuristic|ADR-0024]]", "[[ADR-0034 Adopt published ALF and two-leg ddG|ADR-0034]]"]
tasks: ["[[TASK-024 ALF phases 1 to 3|TASK-024]]", "[[TASK-046 Implement or adopt standard ALF|TASK-046]]"]
issues: ["[[ISS-011 ALF is a heuristic and ddG is single-leg|ISS-011]]"]
created: 2026-09-16
updated: 2026-09-27
retrospective: true
---
# FEAT-012 — ALF flattening (heuristic, as built)

Phases 1–3 in `msld/alf.py`. Toy-validated but not the published algorithm ([[ISS-011 ALF is a heuristic and ddG is single-leg|ISS-011]]); to be
replaced by [[FEAT-035 Standard ALF|FEAT-035]].

