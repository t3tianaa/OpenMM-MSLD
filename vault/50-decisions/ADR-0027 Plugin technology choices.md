---
id: ADR-0027
type: adr
title: Plugin technology choices
status: accepted
date: 2026-09-23
deciders: [Tetiana]
affects: ["[[Production plugin architecture]]"]
requirements: ["[[REQ-029 Production performance on GPU|REQ-029]]", "[[REQ-021 Runs on Reference, CPU, OpenCL, CUDA|REQ-021]]"]
retrospective: true
---
# ADR-0027 — Plugin technology: common compute layer, Reference first, SWIG

## Decisions (each from `PLUGIN_PLAN.md` §2)
1. C++11/14 public API (matches OpenMM headers).
2. Kernels in OpenMM's **common compute layer** — one source for OpenCL (dev Mac) and CUDA
   (production cluster); raw OpenCL would lock out CUDA.
3. **Reference platform first**, double precision, as the oracle for GPU kernels.
4. Fixed-point accumulation of dU/dλ on GPU.
5. SWIG Python bindings; start from `openmmexampleplugin`.
6. Hardware: Mac OpenCL (fp32 only) for development, CUDA (mixed/double) for production and final
   validation.

## Consequences
- CUDA is never exercised on the dev machine → schedule a cluster validation at the end of S2
  ([[TASK-063 CUDA validation run on the cluster|TASK-063]]).
- Needs `swig` in the env.

