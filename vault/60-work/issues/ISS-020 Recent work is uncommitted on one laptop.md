---
id: ISS-020
type: issue
title: Recent work is uncommitted on one laptop
status: open
kind: process
severity: high
confidence: confirmed
source: "[[AUD-001 Engine audit of the local working copy|AUD-001]]"
affects: ["[[README]]"]
fixed_by: ["[[TASK-030 Commit and push the local state to a branch|TASK-030]]"]
found: 2026-09-26
updated: 2026-09-27
---
# ISS-020 — Months of work exist only as uncommitted files on one laptop

HEAD = `7863097` (2026-08-14) = `origin/msld-phase1`. Everything since (the whole staged prep
pipeline, `alf.py`, `io.py`, 20 test files, all docs, the MDM2 system) is untracked or modified;
deletes of untracked files are unrecoverable. The committed `msld/prep/` does not even import
(missing `__init__.py`). Large outputs (49 MB in `test_systems/mdm2/out/`) must be git-ignored first.
Fix: [[TASK-030 Commit and push the local state to a branch|TASK-030]] (needs the owner's approval to commit/push).

