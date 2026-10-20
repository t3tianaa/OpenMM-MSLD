---
id: G-2
type: goal
title: Physically correct MSLD
status: active
updated: 2026-09-27
---
# G-2 — Physically correct MSLD

The OpenMM implementation computes the **same energy function, the same λ forces and the same
sampling** as the reference MSLD implementation (BLaDE / CHARMM BLOCK) for the same system and
settings — or documents, in an ADR, every deliberate difference and its size.

Why: a fast engine with a subtle convention bug produces confident, wrong free energies.

Success: [[REQ-070 Agree with BLaDE on a shared CHARMM system|REQ-070]] met; all engine requirements `verified`, not only `implemented`.

