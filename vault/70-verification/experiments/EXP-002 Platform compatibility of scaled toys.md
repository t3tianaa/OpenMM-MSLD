---
id: EXP-002
type: experiment
title: Platform compatibility of scaled toys
status: done
date: 2026-09-26
requirements: ["[[REQ-021 Runs on Reference, CPU, OpenCL, CUDA|REQ-021]]"]
issues: ["[[ISS-004 CHARMM NBFIX systems fail on CPU|ISS-004]]"]
related: ["[[AUD-001 Engine audit of the local working copy|AUD-001]]"]
---
# EXP-002 — Platform compatibility (audit E2)

Scaled Amber toy: OK on CPU and OpenCL. Scaled CHARMM NBFIX toy: OpenCL OK; **CPU fails** with
"All Forces must have identical exclusions" ([[ISS-004 CHARMM NBFIX systems fail on CPU|ISS-004]]). CUDA not available.

