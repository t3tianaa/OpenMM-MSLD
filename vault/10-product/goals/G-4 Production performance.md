---
id: G-4
type: goal
title: Production performance
status: active
updated: 2026-09-27
---
# G-4 — Production performance

Run MSLD at a speed close to ordinary OpenMM MD on a GPU, in the NPT ensemble, for solvated
systems of 20 000 – 100 000 atoms, so that ns–μs of sampling are practical.

Current state: the Python driver is ~80 ms/step on OpenCL for 26 k atoms ([[EXP-007 MDM2 first end-to-end run and benchmark|EXP-007]]) — orders
of magnitude too slow, NVT only. The path is the C++ plugin ([[Production plugin architecture]]).

