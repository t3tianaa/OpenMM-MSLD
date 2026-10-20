---
title: Partial-lambda oracle tests
type: component
status: planned
layer: L2
requirements: ["[[REQ-072 Every feature has an automated test|REQ-072]]", "[[REQ-070 Agree with BLaDE on a shared CHARMM system|REQ-070]]"]
updated: 2026-09-27
---
# Partial-λ oracle tests (planned, [[FEAT-045 Independent partial-lambda oracle tests|FEAT-045]])

A cheap, independent check that does not need BLaDE: for small **NoCutoff** toy systems, compute
the MSLD energy and every ∂U/∂λ_b directly from the definition ([[Multisite lambda dynamics]]) in
plain NumPy — pair loops with the scaling rules, bonded terms with product factors — and compare
with the scaled OpenMM System at random interior λ vectors (all sites, several blocks, cross-site
pairs, 1-4s, biases). This closes most of the "only λ = 1 is tested" gap ([[ISS-012 No validation at partial lambda|ISS-012]]) and runs in
seconds. PME cannot be checked this way (except against an Ewald sum for tiny boxes).

