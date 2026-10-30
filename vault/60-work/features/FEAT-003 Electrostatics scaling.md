---
id: FEAT-003
type: feature
title: Electrostatics scaling
status: needs-rework
milestone: M1
implements: ["[[REQ-005 Nonbonded pair scaling rules|REQ-005]]", "[[REQ-006 Same-site pairs never interact|REQ-006]]", "[[REQ-007 PME electrostatics at partial lambda|REQ-007]]", "[[REQ-025 Supported nonbonded methods are correct|REQ-025]]"]
components: ["[[Electrostatics scaling module]]"]
decisions: ["[[ADR-0007 Charges scaled by NonbondedForce offsets|ADR-0007]]", "[[ADR-0009 Within-block real-space electrostatics linear|ADR-0009]]", "[[ADR-0010 Same-site pairs excluded in every nonbonded force|ADR-0010]]", "[[ADR-0036 Same-site reciprocal-space convention|ADR-0036]]", "[[ADR-0040 Supported nonbonded methods|ADR-0040]]"]
tasks: ["[[TASK-005 Implement nonbonded scaling|TASK-005]]", "[[TASK-014 Make within-block electrostatics linear|TASK-014]]", "[[TASK-038 Refuse reaction-field cutoff methods|TASK-038]]", "[[TASK-037 Read PME alpha from the force|TASK-037]]", "[[TASK-044 Decide the same-site PME convention|TASK-044]]"]
issues: ["[[ISS-003 Within-block correction wrong for cutoff methods|ISS-003]]", "[[ISS-006 Same-site PME differs from BLaDE and docs are backwards|ISS-006]]", "[[ISS-008 PME alpha recomputed from the tolerance|ISS-008]]", "[[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]"]
created: 2026-08-05
updated: 2026-09-27
retrospective: true
---
# FEAT-003 — Electrostatics scaling

Charge offsets (native PME), same-site exclusions, within-block linear correction. Works for
NoCutoff and PME at λ = 1; needs: refuse/fix reaction-field methods ([[TASK-038 Refuse reaction-field cutoff methods|TASK-038]]), real PME α
([[TASK-037 Read PME alpha from the force|TASK-037]]), a decided same-site PME convention ([[TASK-044 Decide the same-site PME convention|TASK-044]]), partial-λ validation
([[FEAT-030 BLaDE cross-validation harness|FEAT-030]], [[FEAT-045 Independent partial-lambda oracle tests|FEAT-045]]).

