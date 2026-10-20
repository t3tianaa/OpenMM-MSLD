---
title: Analysis subsystem
type: subsystem
status: planned
layer: L1
code: [msld/io.py, msld/alf.py]
requirements: ["[[REQ-060 Free energy per variant with uncertainty|REQ-060]]", "[[REQ-061 Relative ddG from two legs|REQ-061]]", "[[REQ-062 Sampling and convergence diagnostics|REQ-062]]", "[[REQ-063 Combinatorial multi-site free energies|REQ-063]]"]
decisions: ["[[ADR-0032 Three subsystems preparation simulation analysis|ADR-0032]]", "[[ADR-0034 Adopt published ALF and two-leg ddG|ADR-0034]]"]
updated: 2026-09-27
---
# Analysis subsystem (planned — high-level only)

Per the owner's instruction (2026-09-26), this subsystem is specified briefly until the current
state is consolidated.

## Purpose
Turn λ (and energy) trajectories from one or more runs/legs into relative free energies with
uncertainties, and judge whether the sampling can be trusted.

## Components (planned)
- [[Free energy estimation component]] — per-variant G, ΔG, two-leg ΔΔG, combinatorial multi-site.
- [[Sampling diagnostics component]] — histograms, FPL, transitions, θ temperature, replica agreement.

## Inputs / outputs
In: λ trajectories ([[Lambda trajectory format]]), the bias parameters in force, run metadata.
Out: tables (variant, G, σ), ΔΔG per variant, diagnostic plots/report.

## As built
Only `io.populations` (mean λ) and `alf.estimate_ddg` (bias readout) — neither is the target.

