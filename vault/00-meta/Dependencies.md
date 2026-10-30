---
title: Dependencies
type: meta
status: active
updated: 2026-10-29
---
# Dependencies

Declared in `env/environment.yml` (conda env `msld`). Versions measured on 2026-10-29 on
MacBook-Pro-Tetiana-2: OpenMM **8.6.1**, ParmEd **4.3.1**, RDKit **2025.09.6**, NumPy **2.4.6**,
Python 3.11.15. **Verified.** Platforms: Reference, CPU, OpenCL (`openmm.testInstallation` passes).

**2026-10-29:** `openmm` is pinned to **8.6.1** in `env/environment.yml` ([[AUD-002 OpenMM 8.6 impact on MSLD|AUD-002]]).
The Mac env was updated from 8.5.2 ([[TASK-079 Update the Mac env to OpenMM 8.6.1|TASK-079]]); all 33 tests pass on
8.6.1, as they did on 8.5.2 (2026-09-27).

| package | used for | used in |
|---|---|---|
| openmm | the MD engine: `System`, forces, `Context`, `app` | engine + prep |
| numpy | arrays, Langevin maths, Kabsch SVD | engine + prep |
| parmed | common `Structure`; Amber/CHARMM readers; term transplant; NBFIX recovery | prep only |
| scipy | `cKDTree` for water clash detection | prep (solvate) |
| rdkit | SDF reading; maximum common substructure | prep (ingest, MCS mapper) |
| openmmforcefields + openff-toolkit | GAFF / OpenFF templates for SDF ligands (imported lazily for speed) | prep (ingest) |
| AmberTools (`antechamber`, `sqm`) | AM1-BCC charges for GAFF (a binary, not a Python import) | prep (ingest) |

Rules (from earlier decisions, see [[ADR-0030 Hard dependencies and a ParmEd-free engine|ADR-0030]]):
- The **engine** (`msld/model.py`, `builder.py`, `forces.py`, `integrator.py`) needs only
  openmm + numpy. Prep dependencies must not leak into it.
- A needed package is a **hard dependency**: add it to `env/environment.yml` and install it. No
  "optional import with install hint" fallbacks. Lazy imports are allowed only for start-up speed.
- Tests are self-running scripts (`python tests/test_x.py`); pytest is not installed.
- Plugin work will need `swig` (not yet installed) — see [[FEAT-033 Analytic nonbonded plugin force|FEAT-033]].

Hardware facts (from `PLUGIN_PLAN.md` §1, verified 2026-09-23): Apple M4, OpenCL works in
**single** precision only; mixed/double fail; CUDA impossible on the Mac. Production target is a
CUDA cluster ([[ADR-0027 Plugin technology choices|ADR-0027]]).
