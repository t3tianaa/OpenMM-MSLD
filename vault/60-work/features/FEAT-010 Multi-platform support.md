---
id: FEAT-010
type: feature
title: Multi-platform support
status: needs-rework
milestone: M3
implements: ["[[REQ-021 Runs on Reference, CPU, OpenCL, CUDA|REQ-021]]"]
components: ["[[Force scaling component]]"]
decisions: ["[[ADR-0010 Same-site pairs excluded in every nonbonded force|ADR-0010]]"]
tasks: ["[[TASK-021 Make the MDM2 run work end to end|TASK-021]]", "[[TASK-034 Add same-site exclusions to CHARMM LJ copies|TASK-034]]", "[[TASK-063 CUDA validation run on the cluster|TASK-063]]"]
issues: ["[[ISS-004 CHARMM NBFIX systems fail on CPU|ISS-004]]"]
created: 2026-09-15
updated: 2026-09-27
retrospective: true
---
# FEAT-010 — Multi-platform support

Exclusion parity makes Amber systems run on CPU/OpenCL (and CUDA in principle). CHARMM NBFIX fails on
CPU ([[ISS-004 CHARMM NBFIX systems fail on CPU|ISS-004]]); CUDA never tested ([[TASK-063 CUDA validation run on the cluster|TASK-063]]).

