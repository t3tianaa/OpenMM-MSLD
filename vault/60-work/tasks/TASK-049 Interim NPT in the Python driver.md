---
id: TASK-049
type: task
title: Interim NPT in the Python driver
status: todo
kind: impl
priority: P2
milestone: M7
feature: "[[FEAT-032 NPT ensemble|FEAT-032]]"
issues: ["[[ISS-009 NPT impossible with the Python driver|ISS-009]]"]
refs: ["[[Pressure control and the Monte Carlo barostat]]", "[[BLaDE pressure coupling]]"]
created: 2026-09-27
updated: 2026-09-27
---
# TASK-049 — Interim NPT: a Monte Carlo volume move in `LambdaDynamics`

Molecule-centre scaling, energy with current λ, Metropolis with P·ΔV − N kT ln(V'/V); test density
of a water box vs OpenMM's barostat.

