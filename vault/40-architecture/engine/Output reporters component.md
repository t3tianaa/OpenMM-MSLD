---
title: Output reporters component
type: component
subsystem: "[[Simulation subsystem]]"
layer: L2
status: partial
code: [msld/io.py]
requirements: ["[[REQ-027 Trajectory, lambda and energy output|REQ-027]]"]
updated: 2026-09-27
---
# Output reporters component — `msld/io.py`

- `LambdaTrajectoryWriter(path, model, every=100, mapping=None)` → CSV
  ([[Lambda trajectory format]]).
- `TrajectoryWriter(path, structure, every=1000, mapping=None)` → DCD + companion topology PDB
  (block-only residues renamed `HYB` so viewers draw CONECT to the core; CRYST1 from the box).
- `read_trajectory(path)`, `populations(path)` (mean λ per block — a crude "who wins" signal, not
  a free energy).
- `LambdaDynamics.run` schedules reporters at their own intervals (steps in gcd chunks).

Gaps: no θ / θ-velocity columns; no BLaDE `.lmd` writer; no energy decomposition; no run metadata
(versions, seed, settings — [[REQ-031 Reproducible runs|REQ-031]]); λ every 100 steps by default (ALF analysis uses every
10 steps in BLaDE examples).

