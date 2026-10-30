---
title: README
type: meta
status: active
updated: 2026-09-27
---
# MSLD-OpenMM knowledge vault

This folder is the **single source of truth** for the MSLD-OpenMM project: the problem, the
requirements, the theory, how the reference codes work, our architecture, every design decision,
and every piece of work. It is plain Markdown, versioned in git next to the code, and it opens as an
[Obsidian](https://obsidian.md) vault.

Start at **[[Home]]**.

## Why it exists

The project is built by people and by AI agents, often in parallel, over months. Without a shared,
structured memory, every new session re-derives context, repeats old mistakes and silently changes
old decisions. This vault fixes that:

```
   problem ──▶ goals ──▶ requirements ──▶ features ──▶ tasks ──▶ code + tests
                               ▲               │
                               │               ▼
   theory KB ──┐          decisions (ADR) ──▶ architecture blueprint
   reference KB┴──────────────┘
```

Every arrow is a link, so any line of code can be traced back to the requirement it serves, the
decision that shaped it, and the theory or reference code it relies on.

## How to open it

1. Install Obsidian. Choose **Open folder as vault** and pick this `vault/` folder.
2. Settings → Community plugins → install and enable **Dataview** (the dashboards use it).
   Everything still reads fine without it; the dashboards just show the query text.
3. Optional: the **Templater** or core **Templates** plugin, pointed at `00-meta/templates`.
4. Optional: an Obsidian ↔ Claude integration. Claude sessions in this repository read the
   files directly, so no plugin is required for agents.

## The seven parts

| folder | what it holds | nature |
|---|---|---|
| `10-product` | problem, goals, use cases, requirements, roadmap | what we must achieve |
| `20-theory` | MSLD, λ-dynamics, PME, ALF, soft-core, Langevin, … | ground truth from literature |
| `30-reference` | how OpenMM, BLaDE, ParmEd, ALF actually work, with file:line | ground truth from code |
| `40-architecture` | our blueprint, from system context down to code modules | **our synthesis** |
| `50-decisions` | numbered Architecture Decision Records (ADR) | why the blueprint is this way |
| `60-work` | features, tasks, issues (with status) | who does what, and what is broken |
| `70-verification` | test catalog, experiments, validation plan | how we know it is correct |
| `80-history` | timeline, audits | how we got here |

`00-meta` holds the rules ([[Conventions]], [[Agent protocol]], [[Workflow]]), the
[[Glossary]], templates and a link checker. `01-dashboards` holds live boards.

## The rules in one screen

- Every requirement, feature, task, issue, decision and experiment has a **stable ID**
  (`REQ-006`, `ADR-0009`, …) and YAML frontmatter with its status and links. See [[Conventions]].
- **A decision is never edited away.** To change one, write a new ADR that supersedes it.
- **Code and docs change in the same branch / PR.** A PR that changes behaviour updates the
  matching architecture note, the task status, and adds an ADR if a decision changed.
- Theory and reference notes describe **existing** knowledge. Architecture notes and ADRs are
  **our** choices and must say why.
- Run `python vault/00-meta/tools/vault_check.py` before committing: it checks links and
  frontmatter and refreshes the static indexes.

