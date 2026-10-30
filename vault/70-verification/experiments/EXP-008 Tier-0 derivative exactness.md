---
id: EXP-008
type: experiment
title: Tier-0 derivative exactness
status: done
date: 2026-09-17
requirements: ["[[REQ-020 Accurate dU-dlambda for every term|REQ-020]]"]
related: ["[[FEAT-009 Tier-0 analytic dU-dlambda|FEAT-009]]"]
---
# EXP-008 — Tier-0 hybrid dU/dλ vs full finite difference

New (analytic + group-0 FD) vs old (full-energy FD) agree to ~5e-9; ~7× faster on a tiny NoCutoff toy
(more on systems with many custom forces). `tests/test_analytic_dudl.py`. Reference (double) was as
hot as OpenCL in MDM2 → heat is not only FD noise.

