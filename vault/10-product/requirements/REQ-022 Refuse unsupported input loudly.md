---
id: REQ-022
type: requirement
title: Refuse unsupported input loudly
area: engine
priority: must
status: partial
derives_from: ["[[G-2 Physically correct MSLD|G-2]]"]
satisfied_by: ["[[FEAT-047 Engine hardening|FEAT-047]]"]
decisions: ["[[ADR-0028 Refuse what cannot be scaled|ADR-0028]]", "[[ADR-0037 Whitelist force types|ADR-0037]]"]
created: 2026-08-05
updated: 2026-09-27
retrospective: true
---
# REQ-022 — Refuse unsupported input loudly

**Statement.** If any force, term or setting that touches an alchemical atom cannot be scaled
correctly, the engine shall raise with a clear message — never leave it silently unscaled.

## Acceptance criteria
- [x] AC1 — CMAP, cross-site/same-site 1-4, same-site bonded terms raise.
- [ ] AC2 — whitelist of known forces; any other force touching an alchemical atom raises
  ([[ISS-005 Unsupported force types silently unscaled|ISS-005]]).
- [ ] AC3 — unsupported nonbonded methods refused ([[ISS-003 Within-block correction wrong for cutoff methods|ISS-003]]).

