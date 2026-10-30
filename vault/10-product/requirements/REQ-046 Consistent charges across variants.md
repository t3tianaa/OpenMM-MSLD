---
id: REQ-046
type: requirement
title: Consistent charges across variants
area: prep
priority: must
status: implemented
derives_from: ["[[G-2 Physically correct MSLD|G-2]]", "[[G-3 Automated system preparation|G-3]]"]
satisfied_by: ["[[FEAT-018 Charge renormalization|FEAT-018]]"]
verified_by: ["test_prep_charges", "test_renorm"]
decisions: ["[[ADR-0021 Charge averaging, renormalization, iso-charge guard|ADR-0021]]"]
created: 2026-08-13
updated: 2026-09-27
retrospective: true
---
# REQ-046 — Consistent charges across variants

**Statement.** Each shared (environment) atom carries one charge; each variant (env + its block)
has the same integer net charge; charges that do not match are averaged / renormalized by a
documented rule, and charge-changing sites are refused ([[Net charge changes in alchemical calculations]]).

