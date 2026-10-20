---
id: ISS-019
type: issue
title: Fixed-block lambda semantics differ from BLaDE
status: open
kind: divergence
severity: low
confidence: source
affects: ["[[MSLD model component]]", "[[Lambda dynamics integrator component]]"]
requirements: ["[[REQ-017 Per-block theta mass, friction and fixing|REQ-017]]"]
fixed_by: ["[[TASK-056 Fixed-block semantics like BLaDE|TASK-056]]"]
found: 2026-09-27
updated: 2026-09-27
---
# ISS-019 — Fixed-block λ semantics differ from BLaDE

BLaDE: a fixed block's "θ" holds its λ value; the site's other blocks share `1 − Σλ_fixed` via the
softmax; the chain rule divides by that remainder (`msld.cu:863-985`). Ours: a fixed block's θ is
frozen but its λ still comes from the softmax together with the others. Found while writing
[[BLaDE lambda from theta and theta force]].

