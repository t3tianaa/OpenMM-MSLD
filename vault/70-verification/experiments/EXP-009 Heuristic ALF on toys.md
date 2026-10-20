---
id: EXP-009
type: experiment
title: Heuristic ALF on toys
status: done
date: 2026-09-16
requirements: ["[[REQ-030 Adaptive landscape flattening|REQ-030]]"]
issues: ["[[ISS-011 ALF is a heuristic and ddG is single-leg|ISS-011]]"]
related: ["[[FEAT-012 ALF flattening heuristic|FEAT-012]]"]
---
# EXP-009 — Heuristic ALF on toys (and a first MDM2 attempt)

- P1: toy 2-block site with an injected ΔG·λ₂ and no atomic forces, fnex = 2 → the flat point
  biascoef₂ − biascoef₁ = −ΔG recovered.
- P2: an injected −A·λ₁λ₂ midpoint trap → coupling learns k ≈ +A and un-traps θ. Two wrong attempts
  first: targeting uniform-λ overlap or a λ-histogram fit drove k the wrong way; the target must be the
  bare-softmax reference overlap.
- P3: `estimate_ddg` recovers an injected ΔG on the toy; the first attempt with endpoint-population
  reweighting gave the wrong sign (claimed "softmax distortion" — doubted by the audit).
- MDM2 (dry, fnex 5.5): "stuck at λ = 0.5" was largely overdamping (mass 25, γ 10); lighter θ reached
  endpoints without coupling; a large coupling (capped +75) re-froze θ.

