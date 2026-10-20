---
id: FEAT-002
type: feature
title: Bonded term scaling
status: done
milestone: M1
implements: ["[[REQ-003 Scale bonded terms by block lambdas|REQ-003]]", "[[REQ-004 Configurable bonded scaling per term type|REQ-004]]", "[[REQ-023 Lambda one reproduces the base system|REQ-023]]"]
components: ["[[Bonded scaling module]]"]
decisions: ["[[ADR-0006 Bonded scaling via grouped custom forces|ADR-0006]]", "[[ADR-0014 Bonded scaling on by default|ADR-0014]]"]
tasks: ["[[TASK-004 Implement bonded term scaling|TASK-004]]", "[[TASK-011 Cross-variant check and CHARMM impropers|TASK-011]]", "[[TASK-057 BLaDE-style bonded scaling switches|TASK-057]]"]
issues: ["[[ISS-014 Bonded scaling defaults differ from BLaDE|ISS-014]]", "[[ISS-023 Restrained-atom bonded scaling rule missing|ISS-023]]", "[[ISS-015 Cross-site 1-4 and CMAP are refused|ISS-015]]"]
created: 2026-07-31
updated: 2026-09-27
retrospective: true
---
# FEAT-002 — Bonded term scaling

Bonds, UB, angles, periodic torsions, CHARMM harmonic impropers → grouped custom forces with λ
prefactors and analytic derivatives. Done. Follow-ups: BLaDE-style six switches and defaults
([[TASK-057 BLaDE-style bonded scaling switches|TASK-057]]), restrained-atom exception ([[ISS-023 Restrained-atom bonded scaling rule missing|ISS-023]]), CMAP ([[FEAT-036 CMAP scaling|FEAT-036]]).

