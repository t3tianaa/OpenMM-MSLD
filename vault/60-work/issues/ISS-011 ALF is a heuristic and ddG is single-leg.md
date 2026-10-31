---
id: ISS-011
type: issue
title: ALF is a heuristic and ddG is single-leg
status: open
kind: design-flaw
severity: medium
confidence: source
source: "[[AUD-001 Engine audit of the local working copy|AUD-001]]"
affects: ["[[ALF flattening component]]"]
requirements: ["[[REQ-030 Adaptive landscape flattening|REQ-030]]", "[[REQ-060 Free energy per variant with uncertainty|REQ-060]]", "[[REQ-061 Relative ddG from two legs|REQ-061]]"]
fixed_by: ["[[TASK-046 Implement or adopt standard ALF|TASK-046]]", "[[TASK-047 Two-leg ddG estimator|TASK-047]]"]
found: 2026-09-26
updated: 2026-10-31
---
# ISS-011 — ALF is a home-grown heuristic; `estimate_ddg` is single-leg (audit F11)

`msld/alf.py` updates fixed biases by `rate·kT·ln(p/p_target)` and only a type-6 coupling. Published
ALF fits b, c (6), x (10, l0 = −5.56), s (8, l0 = 0.017) by likelihood over λ histograms
(`test/HSP90/cb7.inp`). The docstring claim that the endpoint estimator is distorted by the softmax
is doubtful (by symmetry all blocks share the same endpoint probability). `estimate_ddg` returns a
single-environment ΔG; ΔΔG needs two legs. Plan: [[ADR-0034 Adopt published ALF and two-leg ddG|ADR-0034]].


**Confirmed on MDM2 (2026-10-31).** The heuristic switches variants well but does not converge and
rarely commits to endpoints; b and the type-6 couplings run away against each other
([[EXP-012 MDM2 TI and ALF on the fixed build|EXP-012]]). Capping the couplings would make blending worse. Fix deferred to the plugin stage
with the published algorithm ([[ALF package overview]]).
