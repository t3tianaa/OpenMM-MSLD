---
id: UC-5
type: use-case
title: Explore combinatorial chemical space
status: active
derives_from: ["[[G-1 Free energies for many variants at once|G-1]]", "[[G-4 Production performance|G-4]]", "[[G-5 Meaningful analysis|G-5]]"]
updated: 2026-09-27
---
# UC-5 — Explore combinatorial chemical space

Many sites × many substituents (e.g. 3 × 10 = 1000 molecules) in one simulation, with θ biases to
keep the fraction of physical states usable, and analysis that ranks all combinations with
uncertainties (including combinations rarely visited).

Needs: θ biases ([[FEAT-038 Theta biases|FEAT-038]]), scalable LJ grouping ([[TASK-069 Scalable LJ grouping for many sites|TASK-069]]), production speed
([[FEAT-033 Analytic nonbonded plugin force|FEAT-033]]), combinatorial analysis ([[REQ-063 Combinatorial multi-site free energies|REQ-063]]).

