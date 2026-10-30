---
id: TASK-079
type: task
title: Update the Mac env to OpenMM 8.6.1
status: done
kind: chore
priority: P1
milestone: M4
feature: "[[FEAT-047 Engine hardening|FEAT-047]]"
refs: ["[[Dependencies]]", "[[AUD-002 OpenMM 8.6 impact on MSLD|AUD-002]]"]
created: 2026-10-29
updated: 2026-10-29
---
# TASK-079 — Update the Mac env to the pinned OpenMM 8.6.1 and re-run the tests

`env/environment.yml` pins `openmm=8.6.1` (2026-10-29). Run `conda env update -f env/environment.yml` (or recreate
`msld`), re-run all `tests/test_*.py` on Reference, CPU and **OpenCL**, and update the measured versions in
[[Dependencies]]. Optional: before/after timing of the MDM2 benchmark ([[EXP-007 MDM2 first end-to-end run and benchmark|EXP-007]]) for the 8.6 GPU PME speed-ups.

## Log
- 2026-10-29 — pin added; cloud copy passed on 8.6.1 (Reference/CPU) (agent).
- 2026-10-29 — Mac env `msld` updated 8.5.2 → 8.6.1 via `conda env update` (NumPy/ParmEd/RDKit unchanged). `testInstallation`: Reference/CPU/OpenCL OK. All 33 `tests/test_*.py` pass (Reference is hard-coded in the tests; ~45 s total, slowest test_alf 20 s, test_ingest 10 s). OpenCL (single) smoke check on the test_master toy: λ=1 reproduces the base energy to 1.3e-7 relative and forces exactly; CPU 7.9e-11 / 1.9e-6. MDM2 run skipped (no short-run option) (agent).
