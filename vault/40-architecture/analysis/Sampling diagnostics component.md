---
title: Sampling diagnostics component
type: component
subsystem: "[[Analysis subsystem]]"
layer: L2
status: planned
requirements: ["[[REQ-062 Sampling and convergence diagnostics|REQ-062]]"]
updated: 2026-09-27
---
# Sampling diagnostics component (planned)

Per run: 1-D λ histograms per block, 2-D per pair; FPL; end-state transition counts per block;
θ kinetic temperature; time series of running G estimates; agreement across ≥ 3 independent
replicas. Flags: FPL < 0.01, < N transitions, T_θ outside T ± 5 %, replica spread > 0.5 kcal/mol
(thresholds to agree with the owner).

