---
id: REQ-047
type: requirement
title: Solvate and neutralize consistently
area: prep
priority: must
status: implemented
derives_from: ["[[G-3 Automated system preparation|G-3]]"]
satisfied_by: ["[[FEAT-019 Solvation and ions|FEAT-019]]"]
verified_by: ["test_prep_solvate", "test_hybrid_system"]
decisions: ["[[ADR-0022 Solvation by overlay after grafting|ADR-0022]]"]
created: 2026-08-17
updated: 2026-09-27
retrospective: true
---
# REQ-047 — Solvate and neutralize consistently

**Statement.** Add a water box (with the water model matching the solute force field) and
neutralizing ions around the hybrid solute without changing solute atom indices; preserve CHARMM
ion–water NBFIX.

