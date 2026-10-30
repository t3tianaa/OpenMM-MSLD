---
id: TASK-034
type: task
title: Add same-site exclusions to CHARMM LJ copies
status: todo
kind: fix
priority: P1
milestone: M4
feature: "[[FEAT-047 Engine hardening|FEAT-047]]"
issues: ["[[ISS-004 CHARMM NBFIX systems fail on CPU|ISS-004]]"]
refs: ["[[OpenMM exclusion parity across nonbonded forces]]"]
created: 2026-09-27
updated: 2026-09-27
---
# TASK-034 — Add same-site exclusions to the CHARMM LJ copies

- [ ] `add_scaled_charmm_lj` adds `_same_site_pairs` exclusions to every copy and the restricted original.
- [ ] Exclusion-parity test extended to a CHARMM NBFIX system; CPU Context creation works.

