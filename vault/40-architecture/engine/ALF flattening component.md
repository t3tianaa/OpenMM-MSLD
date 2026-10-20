---
title: ALF flattening component
type: component
subsystem: "[[Simulation subsystem]]"
layer: L2
status: partial
code: [msld/alf.py]
requirements: ["[[REQ-030 Adaptive landscape flattening|REQ-030]]", "[[REQ-060 Free energy per variant with uncertainty|REQ-060]]"]
decisions: ["[[ADR-0024 Home-grown ALF heuristic|ADR-0024]]", "[[ADR-0034 Adopt published ALF and two-leg ddG|ADR-0034]]"]
issues: ["[[ISS-011 ALF is a heuristic and ddG is single-leg|ISS-011]]"]
updated: 2026-09-27
---
# ALF flattening component — `msld/alf.py`

## As built (heuristic, [[ADR-0024 Home-grown ALF heuristic|ADR-0024]])
- `add_flattening_biases(model, couple=True)` — set `bias_flattening` and add a type-6 coupling
  per block pair per site (call before `scale_system`).
- `flatten(dyn, couple=True, n_iters=20, steps_per_iter=20000, rate, couple_rate, …)`:
  ```
  repeat n_iters: run steps_per_iter with a LambdaHistogram reporter
                  p_b = mean λ occupancy
                  b_b += rate·kT·ln(p_b / p_target)                       (Phase 1)
                  k_ij += couple_rate·kT·(o_obs − o_ref)/o_ref              (Phase 2)
                         o_ref = ⟨λ_iλ_j⟩ of the bare softmax (ref_overlap)
                  push with set_biases
  ```
- `estimate_ddg(report, model)` — tail average of −(b_b − b_ref) over the bias history (Phase 3).
- `EndpointPopulation` — diagnostic only.

Toy-validated: recovers an injected ΔG; coupling removes an injected midpoint trap ([[EXP-009 Heuristic ALF on toys|EXP-009]]).

## Why it must be replaced ([[ISS-011 ALF is a heuristic and ddG is single-leg|ISS-011]], [[ADR-0034 Adopt published ALF and two-leg ddG|ADR-0034]])
- It is not the published ALF (no skew/end-point terms, no likelihood fit over histograms).
- `estimate_ddg` is a single-environment ΔG, not ΔΔG.
- Its docstring's claim that endpoint-population estimates are "distorted by the softmax" is
  doubtful (by symmetry all blocks share the same end-point probability).

## Target design
Reproduce ALF ([[Adaptive landscape flattening]], [[ALF package overview]]): b, c, x, s per site;
histogram-based likelihood update; iteration schedule; then production + analysis in
[[Free energy estimation component]]. Option: drive the official ALF package with our engine as
the MD backend if its interfaces allow ([[TASK-074 Study the ALF package|TASK-074]]).

