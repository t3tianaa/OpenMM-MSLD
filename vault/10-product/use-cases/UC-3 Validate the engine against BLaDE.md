---
id: UC-3
type: use-case
title: Validate the engine against BLaDE
status: active
derives_from: ["[[G-2 Physically correct MSLD|G-2]]"]
updated: 2026-09-27
---
# UC-3 — Validate the engine against BLaDE

**Actor.** A developer (human or agent) after any engine change.

**Flow.** Load the same CHARMM system and MSLD setup into BLaDE and into our engine; compare, at a
grid of fixed λ vectors, every energy term and every ∂U/∂λ_b; then compare short dynamics
statistics. Differences must be zero within tolerance or explained by an ADR.

**Status.** Not built ([[FEAT-030 BLaDE cross-validation harness|FEAT-030]]); needs a CUDA machine for BLaDE ([[TASK-042 Get BLaDE running with reference data|TASK-042]]).

