---
id: FEAT-036
type: feature
title: CMAP scaling
status: deferred
milestone: M8
implements: ["[[REQ-010 CMAP scaling|REQ-010]]"]
components: ["[[Bonded scaling module]]"]
tasks: ["[[TASK-053 CMAP scaling spike|TASK-053]]"]
issues: ["[[ISS-015 Cross-site 1-4 and CMAP are refused|ISS-015]]"]
created: 2026-08-19
updated: 2026-09-27
---
# FEAT-036 — CMAP scaling

Needed for CHARMM36/ff19SB backbone mutations. `CMAPTorsionForce` has a fixed formula and no
parameter derivatives. Options: move alchemical CMAP terms to a `CustomCompoundBondForce` with a
`Continuous2DFunction` map and a λ prefactor (must reproduce CMAP's bicubic interpolation exactly),
or implement it in the plugin. Spike in [[TASK-053 CMAP scaling spike|TASK-053]].

