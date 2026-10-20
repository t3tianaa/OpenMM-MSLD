---
id: REQ-021
type: requirement
title: Runs on Reference, CPU, OpenCL, CUDA
area: platform
priority: must
status: partial
derives_from: ["[[G-4 Production performance|G-4]]"]
satisfied_by: ["[[FEAT-010 Multi-platform support|FEAT-010]]"]
verified_by: ["test_minimize", "[[EXP-002 Platform compatibility of scaled toys|EXP-002]]"]
decisions: ["[[ADR-0010 Same-site pairs excluded in every nonbonded force|ADR-0010]]"]
created: 2026-09-15
updated: 2026-09-27
retrospective: true
---
# REQ-021 — Runs on Reference, CPU, OpenCL, CUDA

**Statement.** Any scaled System shall create a Context and run on all OpenMM platforms.

## Acceptance criteria
- [x] AC1 — Amber toy on CPU and OpenCL ([[EXP-002 Platform compatibility of scaled toys|EXP-002]]).
- [ ] AC2 — CHARMM NBFIX on CPU ([[ISS-004 CHARMM NBFIX systems fail on CPU|ISS-004]]).
- [ ] AC3 — CUDA tested on a cluster ([[TASK-063 CUDA validation run on the cluster|TASK-063]]).

