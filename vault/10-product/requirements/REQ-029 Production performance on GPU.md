---
id: REQ-029
type: requirement
title: Production performance on GPU
area: platform
priority: must
status: proposed
derives_from: ["[[G-4 Production performance|G-4]]"]
satisfied_by: ["[[FEAT-033 Analytic nonbonded plugin force|FEAT-033]]", "[[FEAT-034 Fused MSLD integrator plugin|FEAT-034]]"]
decisions: ["[[ADR-0026 Tier 2 plugin with scope S0 to S4|ADR-0026]]", "[[ADR-0027 Plugin technology choices|ADR-0027]]", "[[ADR-0035 Gate plugin work|ADR-0035]]"]
created: 2026-09-23
updated: 2026-09-27
---
# REQ-029 — Production performance on GPU

**Statement.** On a CUDA GPU, an MSLD step shall cost at most ~1.5× a plain MD step of the same
system (target to be confirmed by the owner), including dU/dλ for all blocks.

Today: Python driver, ~80 ms/step on Apple OpenCL for 26 k atoms ([[EXP-007 MDM2 first end-to-end run and benchmark|EXP-007]]).

