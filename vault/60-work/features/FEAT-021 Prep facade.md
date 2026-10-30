---
id: FEAT-021
type: feature
title: Prep facade
status: done
milestone: M3
implements: ["[[REQ-049 Prep hands off a plain System and a model|REQ-049]]"]
components: ["[[Prep facade component]]"]
decisions: ["[[ADR-0020 Variants as monomer residues|ADR-0020]]"]
tasks: ["[[TASK-019 Monomer variants via ignoreExternalBonds|TASK-019]]", "[[TASK-020 Prep facade build_msld_system|TASK-020]]"]
created: 2026-09-01
updated: 2026-09-27
retrospective: true
---
# FEAT-021 — Prep façade `build_msld_system`

One call for ingest + sites + assemble, with per-part force fields and monomer variants.

