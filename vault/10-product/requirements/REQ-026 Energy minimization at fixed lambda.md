---
id: REQ-026
type: requirement
title: Energy minimization at fixed lambda
area: engine
priority: must
status: implemented
derives_from: ["[[G-3 Automated system preparation|G-3]]"]
satisfied_by: ["[[FEAT-023 Minimization at fixed lambda|FEAT-023]]"]
verified_by: ["test_minimize"]
created: 2026-09-15
updated: 2026-09-27
retrospective: true
---
# REQ-026 — Energy minimization at fixed λ

**Statement.** Minimize atom positions of the scaled system at the current λ before dynamics
(freshly grafted/solvated systems have clashes).

