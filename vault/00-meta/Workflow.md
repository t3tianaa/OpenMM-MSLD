---
title: Workflow
type: meta
status: active
updated: 2026-09-27
---
# Workflow — how work moves through the project

## Lifecycle of a change

```
  idea / bug / audit finding
        │
        ▼
  ISS (if something is wrong)  or  REQ (if something new is needed)
        │
        ▼
  FEAT (a coherent capability)  ──▶  architecture note: what changes in the blueprint
        │                                 │
        │                                 ▼
        │                           ADR (if a real choice with alternatives is made)
        ▼
  TASK(s) with acceptance criteria and links to theory / reference notes
        │
        ▼
  git branch  ──▶  code + tests + vault edits  ──▶  PR (docs and code together)
        │
        ▼
  verification: tests pass, EXP note if a measurement was needed, REQ status → implemented/verified
```

## Status transitions

```
 TASK:  todo ──▶ doing ──▶ review ──▶ done
          │        │
          └──▶ blocked ──┘        cancelled (with a reason)

 FEAT:  planned ──▶ in-progress ──▶ done ──▶ needs-rework (an issue re-opened it)
 REQ:   proposed ──▶ approved ──▶ partial ──▶ implemented ──▶ verified
 ADR:   proposed ──▶ accepted ──▶ superseded (by a newer ADR)
 ISS:   open ──▶ investigating ──▶ fixed (fixed_by: TASK) | wontfix (with an ADR)
```

## Git and branches

- `main` is the reviewed line. Work happens on short branches named after the task:
  `task/TASK-041-restraint-groups`.
- Two laptops and several agents may work in parallel: **one task per branch**, merge through
  GitHub PRs. Never let two sessions edit the same note at the same time; if unavoidable, the
  task's owner merges.
- A PR description links the TASK and lists the vault notes it changed.
- Large outputs (trajectories, serialized Systems) never go in git.

## Definition of done (task)

- [ ] acceptance criteria in the task note are met and ticked;
- [ ] tests added or updated; the full test suite passes;
- [ ] the master invariant still holds ([[Invariants]]);
- [ ] architecture note "As-built status" updated;
- [ ] ADR written if a choice was made; superseded ADRs marked;
- [ ] requirement / feature / issue statuses updated;
- [ ] `vault_check.py` passes.

## Where tasks and decisions live — and why not elsewhere

Tasks, decisions and knowledge all live **here**, in git, as Markdown (see [[ADR-0031 Project knowledge system in an Obsidian vault|ADR-0031]]).
GitHub Issues / Projects may be added later as a mirror if more people join, but the vault stays
the source of truth because agents read files, not web UIs, and because a PR can then carry code
and its documentation together.

