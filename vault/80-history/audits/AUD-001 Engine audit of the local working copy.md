---
id: AUD-001
type: audit
title: Engine audit of the local working copy
status: done
date: 2026-09-26
related: ["[[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]]", "[[ISS-012 No validation at partial lambda|ISS-012]]"]
---
# AUD-001 — Engine audit of the local working copy (2026-09-26)

Source file: `AUDIT_2026-09-26.md` in the repository root (kept as the original record). Read-only
audit of branch `msld-phase1` on MacBook-Pro-Tetiana-2, judged against MSLD physics and BLaDE source
(`msld.cu`, `nbdirect.cu`, `nbrecip.cu`, `defines.h`, HSP90 example). Prep layer not covered.

## Summary
- Git: nothing since 2026-08-14 committed ([[ISS-020 Recent work is uncommitted on one laptop|ISS-020]]).
- Tests: 33 files pass; coverage caveats ([[ISS-012 No validation at partial lambda|ISS-012]]).
- Findings → issues:

| audit id | issue | severity |
|---|---|---|
| F1 | [[ISS-001 Atom restraint groups have the wrong meaning\|ISS-001]] restraint groups wrong | high |
| F2 | [[ISS-002 Theta mass convention differs from BLaDE\|ISS-002]] θ mass convention (corrected in the vault: unit build unresolved) | high |
| F3 | [[ISS-003 Within-block correction wrong for cutoff methods\|ISS-003]] within-block correction for cutoff methods | medium |
| F4 | [[ISS-004 CHARMM NBFIX systems fail on CPU\|ISS-004]] CHARMM NBFIX on CPU | medium |
| F5 | [[ISS-005 Unsupported force types silently unscaled\|ISS-005]] unsupported forces unscaled | medium |
| F6 | [[ISS-006 Same-site PME differs from BLaDE and docs are backwards\|ISS-006]] same-site PME vs BLaDE | medium |
| F7 | [[ISS-007 Dispersion correction removed for the whole system\|ISS-007]] dispersion correction | low-medium |
| F8 | [[ISS-008 PME alpha recomputed from the tolerance\|ISS-008]] PME α | low |
| F9 | [[ISS-009 NPT impossible with the Python driver\|ISS-009]] NPT | known |
| F10 | [[ISS-010 Finite-difference dU-dlambda noisy in single precision\|ISS-010]] FD noise | medium |
| F11 | [[ISS-011 ALF is a heuristic and ddG is single-leg\|ISS-011]] ALF heuristic | medium |
| F12 | [[ISS-013 Soft-core off while BLaDE examples use it\|ISS-013]], [[ISS-014 Bonded scaling defaults differ from BLaDE\|ISS-014]], [[ISS-015 Cross-site 1-4 and CMAP are refused\|ISS-015]], [[ISS-016 Theta biases and charge restraints missing\|ISS-016]], [[ISS-017 Zero-mass particles break the integrator\|ISS-017]] | mixed |

- Experiments: [[EXP-001 Theta samples the exact Boltzmann distribution on a toy|EXP-001]]…[[EXP-005 Dispersion correction on|EXP-005]].
- Confirmed correct: softmax and chain rule; VRORV coefficients; pair-scaling rules; 1-4 linear
  offsets; PME self λ²; restraint math; bias formulas 6/8/10; master invariant on Reference and
  OpenCL toys.

## Recommended order (from the audit, now in [[Roadmap]] M4/M5)
1. secure the work ([[TASK-030 Commit and push the local state to a branch|TASK-030]]); 2. fix restraint groups and rerun MDM2 with reference θ
parameters ([[TASK-031 Rebuild atom restraint groups|TASK-031]], [[TASK-032 Resolve BLaDE theta units|TASK-032]], [[TASK-033 Rerun MDM2 with reference theta parameters|TASK-033]]); 3. small engine fixes ([[FEAT-047 Engine hardening|FEAT-047]]);
4. BLaDE fixed-λ cross-check ([[TASK-043 BLaDE fixed-lambda cross-check|TASK-043]]); 5. standard ALF + two-leg ΔΔG ([[TASK-046 Implement or adopt standard ALF|TASK-046]],
[[TASK-047 Two-leg ddG estimator|TASK-047]]); 6. only then the plugin ([[ADR-0035 Gate plugin work|ADR-0035]]).

## Corrections made while building the vault
- F2 assumed BLaDE's NMPS build; BLaDE's own build script defaults to AKMA, where the conclusion flips
  → marked unresolved ([[BLaDE units and theta mass]]).
