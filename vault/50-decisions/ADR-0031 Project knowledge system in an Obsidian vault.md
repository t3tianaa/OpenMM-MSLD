---
id: ADR-0031
type: adr
title: Project knowledge system in an Obsidian vault
status: accepted
date: 2026-09-27
deciders: [Tetiana]
affects: ["[[README]]"]
requirements: ["[[REQ-073 Documentation and traceability|REQ-073]]"]
retrospective: false
---
# ADR-0031 — Project knowledge system: an Obsidian vault in git, with ADRs and stable IDs

## Context
Knowledge lived in chat sessions, three drifting documents (README, GUIDE, DEFERRED, plus
PLUGIN_PLAN and an audit) and a flat Obsidian vault on one laptop. Several humans and many agents
will work in parallel on two laptops and in the cloud. The owner asked for a structured,
traceable project: problem → goals → requirements → features → tasks, with documented decisions, a
theory KB, a "how existing code works" KB, and an architecture that can be viewed both as a
blueprint and with its decision history.

## Options
1. **Obsidian vault as plain Markdown inside the code repository** — versioned with the code; PRs
   carry docs + code; agents read files directly; Obsidian gives graph, backlinks, Dataview boards.
2. Obsidian vault outside git (e.g. Obsidian Sync) — nice for humans; agents and branches cannot see
   it; docs drift from code.
3. GitHub Issues/Projects for tasks + wiki for knowledge — good UI; not versioned with code; hard for
   agents to use offline; split sources of truth.
4. A dedicated tool (Jira, Notion, Linear) — powerful; external; agents need connectors; knowledge
   not next to code.

## Decision
Option 1. The vault lives in `vault/` in the repository. Notes: theory, reference, architecture
(blueprint), ADRs (decision history), requirements, features, tasks, issues, experiments — all
Markdown with YAML frontmatter, stable IDs, wikilinks. Boards via Dataview; a stdlib link checker in
`00-meta/tools`. Git is the audit trail. GitHub Issues may mirror tasks later if more people join.

## Consequences
- One source of truth, branch-aware, reviewable in PRs; agents follow [[Agent protocol]].
- Obsidian-specific syntax (wikilinks, embeds) renders less nicely on GitHub; acceptable.
- Discipline needed: docs updated in the same PR as code ([[Workflow]]).
- The legacy docs stay until retired ([[TASK-073 Retire the legacy documents|TASK-073]]).

