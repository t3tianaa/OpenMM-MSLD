---
id: REQ-048
type: requirement
title: No bonded term between same-site blocks
area: prep
priority: must
status: implemented
derives_from: ["[[G-2 Physically correct MSLD|G-2]]"]
satisfied_by: ["[[FEAT-017 Hybrid structure grafting|FEAT-017]]"]
verified_by: ["test_prep_cross_variant"]
decisions: ["[[ADR-0017 Staged prep pipeline|ADR-0017]]"]
created: 2026-08-14
updated: 2026-09-27
retrospective: true
---
# REQ-048 — No bonded term between same-site blocks

**Statement.** The hybrid structure shall contain no bonded term (bond, angle, dihedral, improper,
UB, CMAP, 1-4) linking two different blocks of the same site. Prep never creates one and checks
before building the System.

