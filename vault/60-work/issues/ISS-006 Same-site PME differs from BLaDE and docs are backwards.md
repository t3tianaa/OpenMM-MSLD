---
id: ISS-006
type: issue
title: Same-site PME differs from BLaDE and docs are backwards
status: open
kind: divergence
severity: medium
confidence: source
source: "[[AUD-001 Engine audit of the local working copy|AUD-001]]"
affects: ["[[Electrostatics scaling module]]", "[[BLaDE cross-validation harness]]"]
requirements: ["[[REQ-006 Same-site pairs never interact|REQ-006]]", "[[REQ-007 PME electrostatics at partial lambda|REQ-007]]", "[[REQ-070 Agree with BLaDE on a shared CHARMM system|REQ-070]]"]
fixed_by: ["[[TASK-044 Decide the same-site PME convention|TASK-044]]"]
found: 2026-09-26
updated: 2026-09-27
---
# ISS-006 — Same-site PME treatment differs from BLaDE's default; docs describe it backwards (audit F6)

We exclude same-site pairs; OpenMM's exclusion correction then removes their reciprocal interaction:
competing variants feel **zero** electrostatics. BLaDE's default `msldEwaldType = 2` does not
correct same-site pairs, so they keep λ_bλ_c q q erf(βr)/r ([[BLaDE PME reciprocal space and exclusions]]).
`DEFERRED.md` said "partial-λ same-site reciprocal cross-talk is the known approximation" — our code
has no cross-talk; BLaDE does.

Also: the within-block "linear" correction is real-space only; for close pairs most energy is
reciprocal (λ²), e.g. a 0.6 nm pair has ~1 % real-space share → E(0.5) = −59.7 vs −58.9 for pure λ².
Consistent with BLaDE, not a bug, but the docs overstated "within-block is linear".

Decision needed: [[ADR-0036 Same-site reciprocal-space convention|ADR-0036]].

