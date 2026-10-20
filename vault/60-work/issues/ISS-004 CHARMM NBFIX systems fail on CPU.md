---
id: ISS-004
type: issue
title: CHARMM NBFIX systems fail on CPU
status: open
kind: bug
severity: medium
confidence: confirmed
source: "[[AUD-001 Engine audit of the local working copy|AUD-001]]"
affects: ["[[Lennard-Jones scaling module]]"]
requirements: ["[[REQ-008 LJ scaling including NBFIX|REQ-008]]", "[[REQ-021 Runs on Reference, CPU, OpenCL, CUDA|REQ-021]]"]
fixed_by: ["[[TASK-034 Add same-site exclusions to CHARMM LJ copies|TASK-034]]"]
found: 2026-09-26
updated: 2026-09-27
---
# ISS-004 — CHARMM NBFIX systems fail on the CPU platform (audit F4)

`add_scaled_charmm_lj` copies the original tabulated force's exclusions but not the same-site
exclusions → `OpenMMException: All Forces must have identical exclusions` on CPU (OpenCL accepted
it; CUDA untested) ([[EXP-002 Platform compatibility of scaled toys|EXP-002]], [[OpenMM exclusion parity across nonbonded forces]]). Fix: add
`_same_site_pairs` to the copies, as the within-block correction already does; add a CHARMM case to
the exclusion-parity test.

