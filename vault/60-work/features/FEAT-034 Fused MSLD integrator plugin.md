---
id: FEAT-034
type: feature
title: Fused MSLD integrator plugin
status: planned
milestone: M7
implements: ["[[REQ-016 Canonical sampling of atoms and theta|REQ-016]]", "[[REQ-019 NPT ensemble|REQ-019]]", "[[REQ-029 Production performance on GPU|REQ-029]]"]
components: ["[[Production plugin architecture]]"]
decisions: ["[[ADR-0026 Tier 2 plugin with scope S0 to S4|ADR-0026]]"]
tasks: ["[[TASK-061 Plugin S3 fused integrator|TASK-061]]"]
created: 2026-09-23
updated: 2026-09-27
---
# FEAT-034 — Fused MSLD integrator (`MSLDIntegrator`)

Plugin stage S3: θ + atoms in one OpenMM Integrator; barostat works; θ at 300 K.

