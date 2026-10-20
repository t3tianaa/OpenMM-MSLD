---
id: FEAT-039
type: feature
title: Cross-site 1-4 scaling
status: deferred
milestone: M8
implements: ["[[REQ-009 1-4 pair scaling|REQ-009]]"]
components: ["[[1-4 exception scaling module]]"]
tasks: ["[[TASK-052 Cross-site 1-4 scaling|TASK-052]]"]
issues: ["[[ISS-015 Cross-site 1-4 and CMAP are refused|ISS-015]]"]
created: 2026-09-01
updated: 2026-09-27
---
# FEAT-039 — Cross-site 1-4 scaling

λ_bλ_c 1-4 pairs (sites three bonds apart). Exception offsets are linear → needs a
`CustomBondForce` for these pairs with the 1-4 LJ + Coulomb (and PME exclusion handling).

