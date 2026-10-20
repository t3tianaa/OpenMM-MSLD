---
title: OpenMM platforms and precision
type: reference
status: verified
system: openmm
version: 8.5.2
related: ["[[Finite differences and floating-point precision]]"]
updated: 2026-09-27
---
# OpenMM platforms and precision

| platform | precision options | notes for us |
|---|---|---|
| Reference | double | exact but ~31 s/step for 26 k atoms ([[EXP-007 MDM2 first end-to-end run and benchmark\|EXP-007]]) |
| CPU | mixed (single + double accumulation) | needs exclusion parity; set `OPENMM_CPU_THREADS` to limit cores |
| OpenCL | single / mixed / double | **Apple M4: only single works** (mixed and double fail, verified 2026-09-23) |
| CUDA | single / mixed / double | production cluster; not available on the Mac |

Single precision matters for us because finite-difference dU/dλ of a large energy is noisy
([[Finite differences and floating-point precision]]). Energy accumulation in OpenMM GPU kernels
uses 64-bit fixed point for forces; energies in single precision still carry ~1e-7 relative
error.

