---
id: TASK-031
type: task
title: Rebuild atom restraint groups
status: todo
kind: fix
priority: P0
milestone: M4
feature: "[[FEAT-007 Atom restraints|FEAT-007]]"
issues: ["[[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]]", "[[ISS-023 Restrained-atom bonded scaling rule missing|ISS-023]]"]
refs: ["[[REQ-014 Atom restraints between substituents]]", "[[BLaDE atom restraints and soft bonds]]", "[[ADR-0033 Atom restraints group equivalent atoms|ADR-0033]]"]
depends_on: ["[[TASK-030 Commit and push the local state to a branch|TASK-030]]"]
created: 2026-09-27
updated: 2026-09-27
---
# TASK-031 — Rebuild atom restraint groups as equivalent atoms across substituents

## Acceptance criteria
- [ ] `model_from_mappings(add_restraints=…)` default False; MDM2 script without restraints.
- [ ] New builder of groups from `CoreMapping.core_corresp` / duplicated core atoms: one group per
      equivalent atom, one atom per block.
- [ ] Test: a site with duplicated backbone gets groups {N₁, N₂, …}; a plain side-chain site gets none.
- [ ] ADR-0033 accepted (owner).

