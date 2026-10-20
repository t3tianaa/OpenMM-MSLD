---
id: FEAT-005
type: feature
title: 1-4 exception scaling
status: done
milestone: M1
implements: ["[[REQ-009 1-4 pair scaling|REQ-009]]"]
components: ["[[1-4 exception scaling module]]"]
decisions: ["[[ADR-0007 Charges scaled by NonbondedForce offsets|ADR-0007]]", "[[ADR-0028 Refuse what cannot be scaled|ADR-0028]]"]
tasks: ["[[TASK-005 Implement nonbonded scaling|TASK-005]]"]
issues: ["[[ISS-015 Cross-site 1-4 and CMAP are refused|ISS-015]]"]
created: 2026-08-05
updated: 2026-09-27
retrospective: true
---
# FEAT-005 — 1-4 exception scaling

Single-λ 1-4 via exception offsets (Amber and CHARMM ε14/NBFIX). Cross-site product 1-4 refused →
[[FEAT-039 Cross-site 1-4 scaling|FEAT-039]].

