---
title: Coordinate alignment
type: component
subsystem: "[[Preparation subsystem]]"
layer: L3
status: as-built
code: [msld/prep/assemble/align.py]
requirements: ["[[REQ-045 Place variant coordinates in the shared frame|REQ-045]]"]
updated: 2026-09-27
---
# Coordinate alignment

`CoordinateAligner` (ABC) with `BackboneAligner` (fit atoms N, CA, C, O matched by name; ≥ 3
needed) and `IdentityAligner` (already co-framed inputs). `kabsch(mobile, target)` →
`RigidTransform(R, t)` with `apply`, `rmsd`, `as_matrix`. NumPy only, duck-typed on
`atom.name`, `atom.xx/xy/xz` ([[Kabsch superposition]]). Tests: `test_aligner` (9).

For ligands the fit should use the MCS core atoms, not backbone names — today the default aligner
is still `BackboneAligner`; a ligand run needs an MCS-based aligner or co-framed inputs (**Inferred**,
to confirm in [[TASK-040 Audit the preparation layer|TASK-040]]).

