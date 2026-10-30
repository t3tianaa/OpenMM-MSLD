---
id: AUD-002
type: audit
title: OpenMM 8.6 impact on MSLD
status: done
date: 2026-10-29
related: ["[[ADR-0042 OpenMM multistate samplers for fixed-lambda cross-checks|ADR-0042]]", "[[TASK-078 Fixed-lambda replica-exchange cross-check|TASK-078]]", "[[ISS-012 No validation at partial lambda|ISS-012]]"]
---
# AUD-002 — OpenMM 8.6 (8.6.0 / 8.6.1) impact on MSLD (2026-10-29)

Source: `audits/OPENMM_8.6_AUDIT_2026-10-29.md` in the Claude project files (full record, with the demo
script `rex_demo.py`). Read-only: release notes plus the `8.5.2..8.6.1` source diff, compared with branch
`msld-phase1-sync-2026-09-27` (`0b37a63`).

## Summary
- **Nothing breaks.** All 33 test scripts: same results on 8.5.2 and 8.6.1 (32 pass; `test_ingest` failed on both
  only because openff was missing in the test sandbox). Reference/CPU only, no GPU tested.
- **Plugin still needed.** `NonbondedForce` gained no parameter derivatives, so the electrostatic FD
  ([[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]), the Python driver ([[ADR-0012 Python driver integrator instead of CustomIntegrator|ADR-0012]]) and no-NPT ([[ISS-009 NPT impossible with the Python driver|ISS-009]]) are unchanged.
- **New `ReplicaExchangeSampler` / `ExpandedEnsembleSampler`** (`openmm.app`). Not a drop-in for MSLD (they call
  `integrator.step()`; θ lives in Python), but they enable a fixed-λ HREX + MBAR cross-check on our own
  Hamiltonian with the stock integrator, NPT and constraints → [[ADR-0042 OpenMM multistate samplers for fixed-lambda cross-checks|ADR-0042]], [[TASK-078 Fixed-lambda replica-exchange cross-check|TASK-078]].
  Toy demo: our λ globals work as state keys, energies match a manual evaluation exactly, exchanges and the
  barostat work.
- **Plugin design point:** if `MSLDIntegrator` keeps θ/vθ in Context state, BP-REX comes for free from the sampler
  ([[Production plugin architecture]], S3).
- Smaller: CustomNonbondedForce LRC cache (helps fixed-λ runs only, not continuous λ; relevant to
  [[ADR-0039 Dispersion correction handling|ADR-0039]]); GPU barostat coordinate-jump fix (#5326, use ≥ 8.6 for GPU NPT); per-particle barostat
  scaling (reference for [[TASK-049 Interim NPT in the Python driver|TASK-049]]); GPU PME speed-ups; Modeller ion-cutoff fix (no effect on prep).
- Side finding: `forces.py:617` claims the LRC is unsupported with interaction groups. OpenMM has supported that
  since 2013.
- No effect on the prep-review issues.
