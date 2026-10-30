---
id: REQ-001
type: requirement
title: Represent sites, blocks and environment
area: engine
priority: must
status: implemented
derives_from: ["[[G-1 Free energies for many variants at once|G-1]]", "[[UC-1 Protein mutation scan|UC-1]]", "[[UC-2 Ligand R-group scan|UC-2]]"]
satisfied_by: ["[[FEAT-001 MSLD data model|FEAT-001]]"]
verified_by: ["test_model"]
decisions: ["[[ADR-0005 Lambda as softmax of fnex sin theta|ADR-0005]]"]
created: 2026-07-27
updated: 2026-09-27
retrospective: true
---
# REQ-001 — Represent sites, blocks and environment

**Statement.** The engine shall hold an MSLD model: block 0 = environment (site 0, λ ≡ 1); every
other atom set belongs to exactly one block; blocks belong to sites ≥ 1; each site has ≥ 2
blocks (or exactly one fixed block); any number of sites.

**Rationale.** The site/block structure defines every scaling rule ([[Multisite lambda dynamics]]).

## Acceptance criteria
- [x] AC1 — an atom cannot be in two blocks; out-of-range atoms rejected (`test_model`).
- [x] AC2 — blocks must be ordered by consecutive sites; site 0 has exactly one block (mirrors
  BLaDE `Msld::initialize`, [[BLaDE MSLD data model]]).
- [x] AC3 — multi-site models supported.

Component: [[MSLD model component]].

