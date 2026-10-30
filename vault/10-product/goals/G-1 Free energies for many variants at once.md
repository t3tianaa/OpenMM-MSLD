---
id: G-1
type: goal
title: Free energies for many variants at once
status: active
updated: 2026-09-27
---
# G-1 — Free energies for many variants at once

Compute relative free energies (ΔG between variants in one environment, ΔΔG between two
environments such as bound vs unbound or folded vs unfolded) for **many** chemical variants at
**one or more** sites, in a **single** λ-dynamics simulation per environment.

Why: this is the whole point of MSLD — combinatorial chemistry at the cost of roughly one
simulation ([[Multisite lambda dynamics]]).

Success: reproduce published MSLD results (e.g. T4 lysozyme side-chain folding ΔΔG, or an HSP90 ligand series; see [[BLaDE T4L and HSP90 examples]]) within statistical error.

Derived: [[UC-1 Protein mutation scan|UC-1]], [[UC-2 Ligand R-group scan|UC-2]], [[UC-5 Explore combinatorial chemical space|UC-5]]; requirements in [[Requirements index]].

