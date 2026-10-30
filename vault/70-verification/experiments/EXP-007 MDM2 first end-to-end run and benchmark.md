---
id: EXP-007
type: experiment
title: MDM2 first end-to-end run and benchmark
status: done
date: 2026-09-15
requirements: ["[[REQ-021 Runs on Reference, CPU, OpenCL, CUDA|REQ-021]]", "[[REQ-029 Production performance on GPU|REQ-029]]", "[[REQ-026 Energy minimization at fixed lambda|REQ-026]]"]
issues: ["[[ISS-022 Ingest does not validate geometry|ISS-022]]"]
related: ["[[FEAT-022 MDM2 test system|FEAT-022]]"]
---
# EXP-007 — MDM2 first end-to-end run, platform benchmark

- Empty-metrics run traced to: corrupt OXT coordinate (peptide PE +6.9·10⁶ kJ/mol), no minimization
  (PE 7.7·10⁶ → 801 after minimizing; max force 4.8·10⁷ → 61), stiff θ (T_θ 24 800 K at step 20).
- Benchmark, ~26 k atoms solvated: Reference 31.5 s/step; **OpenCL 83 ms/step** (Apple M4, fp32; energy
  matches Reference at a minimized geometry within 0.003 kJ/mol).
- With bond/angle scaling on, switched-off side chains drifted (ILE max distance to CB 2.8 → 4.8 Å);
  off: 2.8 → 2.9 Å → bond/angle scaling turned off in the script ([[ADR-0014 Bonded scaling on by default|ADR-0014]]).
- λ collapsed to SER (solvated) within the short run — populations meaningless without flattening.
- Observation: U is linear in λ, so dU/dλ is bounded — the instability was magnitude/timescale, not an
  end-point singularity.

