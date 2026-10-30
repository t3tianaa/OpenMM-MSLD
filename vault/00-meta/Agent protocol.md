---
title: Agent protocol
type: meta
status: active
updated: 2026-09-27
---
# Agent protocol — rules for Claude (and any other agent)

Read this before touching code or docs in this repository.

## Before you start

1. Read [[Home]], [[Status]] and the note of the task you were given (or find it on the
   [[Task board]]). If there is no task for your work, create one (next free ID) and link it to a
   feature and a requirement.
2. Read the linked architecture note(s) and every ADR they list. **Do not re-decide an
   `accepted` ADR silently.** If you think it is wrong, stop and write a `proposed` ADR that
   supersedes it, with evidence, and tell the human.
3. Read the linked theory / reference notes instead of re-deriving physics or re-reading
   OpenMM / BLaDE source. If a reference note is missing or wrong, fix it (it is shared memory).

## While you work

- Keep the task note current: status `doing`, a short progress log at the bottom, and any new
  finding written as an `ISS` note, not only in chat.
- Cite sources. External code → file:line + commit/version. Our code → `path:function`.
- Mark every claim **Verified / Source / Inferred**. Never present an inference as a fact.
- Protect the [[Invariants]]. Any change to the engine must keep the master invariant test green.
- Respect resources: limit parallel jobs and threads (e.g. `OPENMM_CPU_THREADS=2`,
  `OMP_NUM_THREADS=2`) unless the human agrees to more. Ask before long or heavy runs.

## When you finish

- Update statuses: TASK → `review` or `done`; FEAT / REQ / ISS as appropriate.
- Update the architecture note's "As-built status".
- Record measurements as an `EXP` note.
- Run `python vault/00-meta/tools/vault_check.py`; fix every broken link it reports.
- Code and vault changes go in the **same** branch and PR. Never commit, push or open a PR
  without the human's permission.

## Things agents got wrong before (do not repeat)

- Declaring work "complete" while partial-λ physics was never checked against an independent
  implementation ([[ISS-012 No validation at partial lambda|ISS-012]]).
- Reading a BLaDE feature by its name instead of its code (atom restraints, [[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]]).
- Tuning parameters on single short runs; θ statistics need many independent, long runs
  ([[EXP-001 Theta samples the exact Boltzmann distribution on a toy|EXP-001]], [[EXP-006 MDM2 theta-parameter sweep|EXP-006]]).
- Writing "BLaDE does X" in docs when BLaDE does the opposite (same-site PME, [[ISS-006 Same-site PME differs from BLaDE and docs are backwards|ISS-006]]).
- Leaving months of work uncommitted ([[ISS-020 Recent work is uncommitted on one laptop|ISS-020]]).

