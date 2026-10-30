---
title: Issue tracker
type: dashboard
status: active
updated: 2026-09-27
---
# Issue tracker

```dataview
TABLE title, status, severity, kind, confidence, fixed_by
FROM "60-work/issues"
WHERE type = "issue"
SORT severity ASC, id ASC
```

## Static index (generated)
<!-- BEGIN GENERATED -->
| issue | title | status | severity | kind | confidence | fixed by |
|---|---|---|---|---|---|---|
| [[ISS-001 Atom restraint groups have the wrong meaning\|ISS-001]] | Atom restraint groups have the wrong meaning | investigating | high | bug | source | [[TASK-031 Rebuild atom restraint groups\|TASK-031]] |
| [[ISS-002 Theta mass convention differs from BLaDE\|ISS-002]] | Theta mass convention differs from BLaDE | investigating | high | divergence | inferred | [[TASK-032 Resolve BLaDE theta units\|TASK-032]], [[TASK-033 Rerun MDM2 with reference theta parameters\|TASK-033]] |
| [[ISS-012 No validation at partial lambda\|ISS-012]] | No validation at partial lambda | open | high | risk | confirmed | [[TASK-067 NumPy partial-lambda oracle tests\|TASK-067]], [[TASK-043 BLaDE fixed-lambda cross-check\|TASK-043]] |
| [[ISS-018 Theta runs hot in MDM2\|ISS-018]] | Theta runs hot in MDM2 | investigating | high | bug | confirmed | [[TASK-032 Resolve BLaDE theta units\|TASK-032]], [[TASK-033 Rerun MDM2 with reference theta parameters\|TASK-033]] |
| [[ISS-020 Recent work is uncommitted on one laptop\|ISS-020]] | Recent work is uncommitted on one laptop | open | high | process | confirmed | [[TASK-030 Commit and push the local state to a branch\|TASK-030]] |
| [[ISS-003 Within-block correction wrong for cutoff methods\|ISS-003]] | Within-block correction wrong for cutoff methods | open | medium | bug | confirmed | [[TASK-038 Refuse reaction-field cutoff methods\|TASK-038]] |
| [[ISS-004 CHARMM NBFIX systems fail on CPU\|ISS-004]] | CHARMM NBFIX systems fail on CPU | open | medium | bug | confirmed | [[TASK-034 Add same-site exclusions to CHARMM LJ copies\|TASK-034]] |
| [[ISS-005 Unsupported force types silently unscaled\|ISS-005]] | Unsupported force types silently unscaled | open | medium | design-flaw | source | [[TASK-035 Whitelist force types\|TASK-035]] |
| [[ISS-006 Same-site PME differs from BLaDE and docs are backwards\|ISS-006]] | Same-site PME differs from BLaDE and docs are backwards | open | medium | divergence | source | [[TASK-044 Decide the same-site PME convention\|TASK-044]] |
| [[ISS-007 Dispersion correction removed for the whole system\|ISS-007]] | Dispersion correction removed for the whole system | open | medium | bug | confirmed | [[TASK-036 Preserve env-env dispersion correction\|TASK-036]] |
| [[ISS-009 NPT impossible with the Python driver\|ISS-009]] | NPT impossible with the Python driver | open | medium | gap | confirmed | [[TASK-049 Interim NPT in the Python driver\|TASK-049]], [[TASK-061 Plugin S3 fused integrator\|TASK-061]] |
| [[ISS-010 Finite-difference dU-dlambda noisy in single precision\|ISS-010]] | Finite-difference dU/dlambda noisy in single precision | investigating | medium | design-flaw | inferred | [[TASK-041 Analytic bias derivatives\|TASK-041]], [[TASK-059 Plugin S1 Reference nonbonded force\|TASK-059]] |
| [[ISS-011 ALF is a heuristic and ddG is single-leg\|ISS-011]] | ALF is a heuristic and ddG is single-leg | open | medium | design-flaw | source | [[TASK-046 Implement or adopt standard ALF\|TASK-046]], [[TASK-047 Two-leg ddG estimator\|TASK-047]] |
| [[ISS-014 Bonded scaling defaults differ from BLaDE\|ISS-014]] | Bonded scaling defaults differ from BLaDE | open | medium | divergence | source | [[TASK-057 BLaDE-style bonded scaling switches\|TASK-057]] |
| [[ISS-017 Zero-mass particles break the integrator\|ISS-017]] | Zero-mass particles break the integrator | open | medium | bug | inferred | [[TASK-039 Handle zero-mass particles in the integrator\|TASK-039]] |
| [[ISS-021 Preparation layer never audited\|ISS-021]] | Preparation layer never audited | open | medium | risk | confirmed | [[TASK-040 Audit the preparation layer\|TASK-040]] |
| [[ISS-022 Ingest does not validate geometry\|ISS-022]] | Ingest does not validate geometry | open | medium | gap | confirmed | [[TASK-055 Validate input geometry\|TASK-055]] |
| [[ISS-015 Cross-site 1-4 and CMAP are refused\|ISS-015]] | Cross-site 1-4 and CMAP are refused | open | low | gap | source | [[TASK-052 Cross-site 1-4 scaling\|TASK-052]], [[TASK-053 CMAP scaling spike\|TASK-053]] |
| [[ISS-016 Theta biases and charge restraints missing\|ISS-016]] | Theta biases and charge restraints missing | open | low | gap | source | [[TASK-051 Implement theta biases\|TASK-051]], [[TASK-054 Charge-changing perturbations\|TASK-054]] |
| [[ISS-019 Fixed-block lambda semantics differ from BLaDE\|ISS-019]] | Fixed-block lambda semantics differ from BLaDE | open | low | divergence | source | [[TASK-056 Fixed-block semantics like BLaDE\|TASK-056]] |
| [[ISS-023 Restrained-atom bonded scaling rule missing\|ISS-023]] | Restrained-atom bonded scaling rule missing | open | low | divergence | source | [[TASK-057 BLaDE-style bonded scaling switches\|TASK-057]] |
| [[ISS-024 Core-only bonded terms take reference parameters\|ISS-024]] | Core-only bonded terms take reference parameters | open | low | risk | inferred | [[TASK-040 Audit the preparation layer\|TASK-040]] |
| [[ISS-025 NBFIX recovery assumes the OpenMM table convention\|ISS-025]] | NBFIX recovery assumes the OpenMM table convention | open | low | risk | source | [[TASK-040 Audit the preparation layer\|TASK-040]] |
| [[ISS-027 Solvated hybrids get wrong variant bonded parameters\|ISS-027]] | Solvated hybrids get wrong variant bonded parameters | fixed | critical | bug | confirmed | — |
| [[ISS-028 Grafted blocks clash with the environment\|ISS-028]] | Grafted blocks clash with the environment | fixed | high | bug | confirmed | — |
| [[ISS-013 Soft-core off while BLaDE examples use it\|ISS-013]] | Soft-core off while BLaDE examples use it | fixed | medium | divergence | source | [[TASK-050 Soft-core design spike\|TASK-050]] |
| [[ISS-026 Constrained atoms run below the bath temperature\|ISS-026]] | Constrained atoms run below the bath temperature | fixed | medium | bug | confirmed | [[ADR-0044 Own SHAKE in the Python driver\|ADR-0044]] |
| [[ISS-008 PME alpha recomputed from the tolerance\|ISS-008]] | PME alpha recomputed from the tolerance | fixed | low | bug | confirmed | [[TASK-037 Read PME alpha from the force\|TASK-037]] |
<!-- END GENERATED -->

