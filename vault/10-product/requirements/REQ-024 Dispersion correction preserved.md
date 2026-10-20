---
id: REQ-024
type: requirement
title: Dispersion correction preserved
area: engine
priority: should
status: partial
derives_from: ["[[G-2 Physically correct MSLD|G-2]]"]
satisfied_by: ["[[FEAT-047 Engine hardening|FEAT-047]]"]
decisions: ["[[ADR-0039 Dispersion correction handling|ADR-0039]]"]
created: 2026-09-26
updated: 2026-09-27
---
# REQ-024 — Dispersion correction preserved

**Statement.** If the input System uses the long-range LJ dispersion correction, the env–env part
shall be kept exactly, and the alchemical part handled by a documented convention
([[Cutoffs, switching and dispersion correction]]). Today the correction is silently removed for
the whole system ([[ISS-007 Dispersion correction removed for the whole system|ISS-007]]).

