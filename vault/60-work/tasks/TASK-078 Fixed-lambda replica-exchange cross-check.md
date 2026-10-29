---
id: TASK-078
type: task
title: Fixed-lambda replica-exchange cross-check
status: todo
kind: test
priority: P1
milestone: M5
feature: "[[FEAT-041 Amber validation vs FEP or TI|FEAT-041]]"
issues: ["[[ISS-012 No validation at partial lambda|ISS-012]]"]
refs: ["[[ADR-0042 OpenMM multistate samplers for fixed-lambda cross-checks|ADR-0042]]", "[[AUD-002 OpenMM 8.6 impact on MSLD|AUD-002]]", "[[Free energy estimators]]", "[[Free energies from lambda populations]]"]
depends_on: ["[[TASK-031 Rebuild atom restraint groups|TASK-031]]", "[[TASK-079 Update the Mac env to OpenMM 8.6.1|TASK-079]]"]
created: 2026-10-29
updated: 2026-10-29
---
# TASK-078 — Fixed-λ HREX + MBAR vs MSLD on the same Hamiltonian

## Goal
Get each variant's ΔG on MDM2 from OpenMM 8.6's `ReplicaExchangeSampler` over fixed λ-vectors (stock integrator),
and compare it with the MSLD λ-population ΔG from the same scaled System.

## Read first
- [[ADR-0042 OpenMM multistate samplers for fixed-lambda cross-checks|ADR-0042]]; demo `rex_demo.py` (Claude project files, `audits/`).

## Acceptance criteria
- [ ] Toy (one site, two one-atom blocks): HREX ΔG agrees with MSLD ΔG within error.
- [ ] MDM2 site: HREX ΔG per variant (MBAR, with uncertainty) agrees with MSLD λ-population ΔG (fixed biases
      subtracted) within error.
- [ ] Runs with H-bond constraints and `MonteCarloBarostat` (NPT); MSLD comparison in NVT at the HREX mean volume
      until [[ISS-009 NPT impossible with the Python driver|ISS-009]] is fixed.
- [ ] Script and results recorded as an experiment note.

## Plan
1. States: λ-vectors along each block-0→block-k path, same-site λ sum to 1, denser near the endpoints (no soft-core).
2. `ReplicaExchangeReporter(energy=True, volume=True, checkpoints=True)`; MBAR (pymbar) on `energy.csv`.
3. Same restraint, bias and bonded-scaling settings as the MSLD run.

## Log
- 2026-10-29 — created from AUD-002; mechanics verified on a toy (agent).
