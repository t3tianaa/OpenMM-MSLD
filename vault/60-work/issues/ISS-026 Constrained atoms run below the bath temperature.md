---
id: ISS-026
type: issue
title: Constrained atoms run below the bath temperature
status: fixed
kind: bug
severity: medium
confidence: confirmed
source: "[[AUD-003 Theta and lambda-dynamics integration review|AUD-003]]"
affects: ["[[Lambda dynamics integrator component]]"]
requirements: ["[[REQ-016 Canonical sampling of atoms and theta|REQ-016]]"]
fixed_by: ["[[ADR-0044 Own SHAKE in the Python driver|ADR-0044]]"]
found: 2026-10-29
updated: 2026-10-29
---
# ISS-026 — Constrained atoms run below the bath temperature

**Symptom.** Rigid water: 267–271 K at γ = 1 ps⁻¹, ~291 K at γ = 5, target 300 K; same on Reference,
CPU and OpenCL, and on MDM2 (258–278 K after 5 ps). Flexible water: 299 K.

**Cause.** `integrator.py:_drift_x` used `Context.applyConstraints`, whose reference positions are
the predicted ones, so the projection is not SHAKE. Also, initial velocities were not projected
(start at T·(3N−Nc)/3N).

**Fix.** ADR-0044. After: 300.7 ± 1.2 K (γ = 1, dt 1 fs).
