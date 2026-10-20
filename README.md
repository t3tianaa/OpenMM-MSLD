# msld — Multi-Site λ-Dynamics for OpenMM

A from-scratch native implementation of multi-site λ-dynamics (MSLD) for OpenMM,
using [BLaDE](https://github.com/RyanLeeHayes/BLaDE) as the reference/validation code.

MSLD lets several chemical variants of a molecule share one simulation and
compete: a coupling variable λ decides how "present" each variant is, and λ
itself moves during the run (driven by an unconstrained variable θ), so the
system samples which variants are favorable instead of simulating each separately.

**Force-field agnostic.** The engine transforms any OpenMM `System` — **Amber**
(the production target), CHARMM, or OpenFF. CHARMM is used *only* to validate the
engine against BLaDE (BLaDE reads only CHARMM).

## Status — engine complete (Amber + CHARMM); prep pipeline end-to-end (33 test files green)

Done and tested:
- **Energy scaling** — bonds, angles, torsions, CHARMM harmonic impropers +
  Urey-Bradley, PME electrostatics, LJ (Amber + CHARMM tabulated/NBFIX), 1-4
  exceptions, within-block electrostatics (BLaDE-linear), same-site exclusions
  (λ=1 reproduces the base System to machine precision).
- **λ-dynamics** — θ→λ softmax, combined VRORV/BAOAB Langevin over atoms + θ,
  fixed + variable (ALF) biases, atom restraints (CATS), SHAKE/RATTLE constraints.
- **Prep** (`msld/prep/`) — a staged system builder: ingest → map → align + graft →
  charge renorm → solvate → System, in three sub-packages (Amber + CHARMM), with a
  one-call façade `build_msld_system(...)`. Amino-acid variants are supplied as plain
  monomer residues (no caps).

Not yet: trajectory I/O, the BLaDE cross-check, θ biases, CMAP scaling, soft-core,
and the performance plugin. All documentation (design, decisions, open work, history) lives in the
Obsidian vault in **`vault/`**; start at `vault/Home.md`.

**This is a correctness tool**, not production: it runs on **Reference/CPU/OpenCL/CUDA**,
the θ-force uses analytic derivatives plus a partial finite difference of only the
group-0 remainder (electrostatics + biases; Tier 0), and soft-core is off. Production
speed/fidelity is the Tier-2 C++/CUDA plugin.

## Environment

```bash
conda activate msld          # openmm 8.5 + numpy (see env/environment.yml)
```

## Run the tests

```bash
conda activate msld
for t in tests/test_*.py; do python "$t"; done
```

## Minimal usage

```python
import openmm as mm
from msld.model import MSLDModel
from msld.builder import scale_msld_system
from msld.integrator import LambdaDynamics

# `system` is any OpenMM System; `positions` its coordinates
model = MSLDModel(system.getNumParticles())
model.add_block(site=1, atoms=[...])     # substituent A at site 1
model.add_block(site=1, atoms=[...])     # substituent B at site 1
model.finalize()
scale_msld_system(system, model)         # in place: scales forces by lambda

ctx = mm.Context(system, mm.VerletIntegrator(0.001),
                 mm.Platform.getPlatform("Reference"))
ctx.setPositions(positions)

dyn = LambdaDynamics(ctx, model, temperature=300.0, timestep=0.001)
dyn.step(1000)
print(dyn.get_lambdas())                 # per-block lambda (sum = 1 per site)
```

## Layout

```
msld/         the package
  model.py       MSLD data model (sites/blocks/theta, classifiers, softmax)
  builder.py     System + MSLDModel -> block-scaled System (scale_msld_system)
  forces.py      the scaled force builders (bonded, PME, LJ, 1-4, biases, restraints)
  integrator.py  LambdaDynamics: theta-force + combined VRORV Langevin (+ constraints)
  prep/          staged system builder (ParmEd):
    ingest/        DataIngestPipeline (files -> parametrized Structure) + NBFIX recovery
    mapping/       CoreMapping · AminoAcidBackboneMapper · MCSMapper · HybridBlueprint
    assemble/      align · HybridStructureBuilder · charges · solvate · system · hub
tests/        one test file per feature (33, all green)
test_systems/ real input structures for the end-to-end tests (e.g. mdm2/)
vault/        project knowledge base (Obsidian): start at vault/Home.md
```

## Key idea

Integrate θ (unconstrained); derive λ per site by softmax
`λ_i = exp(fnex·sin θ_i) / Σ_j exp(fnex·sin θ_j)`. Forces give ∂U/∂λ_b; the
integrator chain-rules to ∂U/∂θ and does a VRORV Langevin step on θ sharing the
atoms' timestep. (∂U/∂λ is analytic for the derivative-exposing `Custom*Force`s and
finite-difference for the group-0 remainder: the `NonbondedForce` and the biases.)
