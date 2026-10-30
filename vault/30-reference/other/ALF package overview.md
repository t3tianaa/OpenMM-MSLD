---
title: ALF package overview
type: reference
status: draft
system: alf
version: not pinned
related: ["[[REQ-030 Adaptive landscape flattening]]", "[[ALF flattening component]]"]
updated: 2026-09-27
---
# ALF package overview (stub — to study)

The ALF Python package (github.com/RyanLeeHayes/ALF, Hayes and co-workers) automates adaptive
landscape flattening for CHARMM and BLaDE: it writes the bias variables (`variables*.inp`, e.g.
`cs1s1s1s2` coefficients used by `cb7.inp`), runs short simulations, analyses λ trajectories, updates
b, c, x, s, and finally analyses production runs.

**Not yet studied in this project.** Before replacing our heuristic ([[ADR-0034 Adopt published ALF and two-leg ddG|ADR-0034]]) we must read and
document ([[TASK-074 Study the ALF package|TASK-074]]):
- the file layout and loop (initial flattening, short → long iterations, production);
- the exact objective used to update biases (likelihood / WHAM), regularization, damping;
- the λ histogram binning and the cutoff for end states;
- the production free-energy estimator and how uncertainties are computed;
- whether it can drive OpenMM directly (then we could call it rather than re-implement).

