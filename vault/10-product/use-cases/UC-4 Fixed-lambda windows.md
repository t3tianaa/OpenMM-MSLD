---
id: UC-4
type: use-case
title: Fixed-lambda windows
status: active
derives_from: ["[[G-1 Free energies for many variants at once|G-1]]", "[[G-2 Physically correct MSLD|G-2]]"]
updated: 2026-09-27
---
# UC-4 — Fixed-λ windows

Hold λ at fixed values (FEP/TI-style windows, or BLaDE `msld fix`) using the same scaled System,
for debugging, for validation against conventional FEP/TI ([[FEAT-041 Amber validation vs FEP or TI|FEAT-041]]), and for endpoint checks.

Status: `Block.fixed` exists; its λ semantics differ from BLaDE ([[ISS-019 Fixed-block lambda semantics differ from BLaDE|ISS-019]]).

