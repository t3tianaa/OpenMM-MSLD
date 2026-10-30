---
title: Conventions
type: meta
status: active
updated: 2026-09-27
---
# Conventions

These rules keep the vault machine-readable for Dataview and for agents, and keep links stable.

## 1. Note kinds and IDs

| kind | ID pattern | folder | file name |
|---|---|---|---|
| goal | `G-n` | `10-product/goals` | `G-1 Title.md` |
| use case | `UC-n` | `10-product/use-cases` | `UC-1 Title.md` |
| requirement | `REQ-nnn` | `10-product/requirements` | `REQ-006 Title.md` |
| feature | `FEAT-nnn` | `60-work/features` | `FEAT-003 Title.md` |
| task | `TASK-nnn` | `60-work/tasks` | `TASK-041 Title.md` |
| issue (bug, flaw, risk, divergence) | `ISS-nnn` | `60-work/issues` | `ISS-001 Title.md` |
| decision | `ADR-nnnn` | `50-decisions` | `ADR-0009 Title.md` |
| experiment | `EXP-nnn` | `70-verification/experiments` | `EXP-001 Title.md` |
| audit | `AUD-nnn` | `80-history/audits` | `AUD-001 Title.md` |
| theory / reference / architecture | no ID | their folders | descriptive title |

- IDs are **never reused** and **never renumbered**. A dropped item keeps its ID with status
  `dropped` / `cancelled` / `rejected`.
- To get the next free ID: look at the index dashboards, or run `vault_check.py --next REQ`.
- Titles are short (≤ 7 words), plain ASCII in file names (write `lambda`, not `λ`, in titles;
  Greek letters are fine in the body).
- Link with the full file name. Obsidian autocompletes it. In text you can shorten the label:
  `[[REQ-006 Same-site pairs never interact|REQ-006]]`.

## 2. Frontmatter (YAML properties)

Every note starts with frontmatter. Common keys:

```yaml
id: REQ-006            # ID notes only
type: requirement      # see list below
title: Same-site pairs never interact
status: implemented    # allowed values depend on type (table below)
created: 2026-07-27
updated: 2026-09-27
tags: [engine]
```

Links in frontmatter are quoted wikilinks, so Dataview and Obsidian Properties can follow them:
`implements: ["[[REQ-006 Same-site pairs never interact|REQ-006]]"]`.

| type | status values | key link fields |
|---|---|---|
| `goal` | active · achieved · dropped | — |
| `use-case` | active · dropped | `derives_from` (goals) |
| `requirement` | proposed · approved · partial · implemented · verified · deferred · rejected | `derives_from`, `satisfied_by` (FEAT), `verified_by` (tests/EXP), `decisions` |
| `feature` | planned · in-progress · done · needs-rework · deferred · dropped | `implements` (REQ), `components`, `decisions`, `tasks`, `issues`, `milestone` |
| `task` | todo · doing · blocked · review · done · cancelled | `feature`, `issues`, `refs`, `depends_on`, `milestone`, `priority`, `kind` |
| `issue` | open · investigating · fixed · wontfix · duplicate | `affects`, `requirements`, `fixed_by`, `source`, `severity`, `confidence` |
| `adr` | proposed · accepted · superseded · deprecated · rejected | `affects`, `requirements`, `supersedes`, `superseded_by` |
| `experiment` | planned · running · done | `requirements`, `issues`, `related` |
| `theory` | draft · reviewed | `related`, `sources` |
| `reference` | draft · verified | `system`, `version`, `related` |
| `subsystem` / `component` / `contract` | target · as-built · partial · planned | `subsystem`, `requirements`, `decisions`, `issues`, `code` |

Meaning of the requirement statuses:
`partial` = some acceptance criteria met; `implemented` = code exists and unit-tested;
`verified` = checked against an independent reference (BLaDE, analytic result, literature).

Task `kind`: impl · fix · test · experiment · research · docs · chore.
Task `priority`: P0 (blocks correctness) · P1 (next) · P2 (later) · P3 (nice to have).
Issue `severity`: critical · high · medium · low. Issue `confidence`: confirmed (reproduced) ·
source (read in code) · inferred (reasoned, not run).

`retrospective: true` marks items written after the fact (reconstructed on 2026-09-27 from git
history, the old docs and the audit). Their dates are best estimates.

## 3. What goes where — the decision test

```
 Is it true independent of our project?            ── yes ─▶ 20-theory or 30-reference
     │ no
 Is it a CHOICE we made (with alternatives)?       ── yes ─▶ ADR in 50-decisions
     │ no                                                   + update the architecture note
 Is it a description of OUR system's design?       ── yes ─▶ 40-architecture
     │ no
 Is it something the system MUST do / be?          ── yes ─▶ REQ in 10-product
     │ no
 Is it work to do (or done)?                        ── yes ─▶ FEAT / TASK in 60-work
     │ no
 Is it something wrong or risky?                    ── yes ─▶ ISS in 60-work/issues
     │ no
 Is it a measurement / run we did?                  ── yes ─▶ EXP in 70-verification
```

## 4. Writing style

- Plain English, short sentences, define jargon on first use, prefer small ASCII diagrams and tiny
  worked examples. Pair every design choice with its reason.
- Every factual claim about external code cites **file:line and version / commit**.
- Every claim about our code cites `path/file.py:function`.
- Mark uncertainty explicitly: **Verified** (run or read today), **Source** (read in code),
  **Inferred** (reasoned, not checked), **Open question**.
- Theory notes cite papers. If a citation is not yet checked, write `(citation to verify)`.

## 5. Architecture note sections

Every component note uses the same skeleton so agents can find things:
`Purpose · Responsibilities · Interfaces (in/out) · Design · Invariants · Decisions ·
Theory & reference links · Requirements · As-built status (code, gaps, issues) · Open questions`.

## 6. ADR rules

- One decision per ADR. Sections: `Context · Options · Decision · Consequences · Links`.
- `accepted` ADRs are immutable except for status and a "Superseded by" line.
- A reversed decision = a **new** ADR with `supersedes:`; the old one gets
  `status: superseded` and `superseded_by:`.
- `proposed` ADRs are open decisions; they list the evidence still needed.

