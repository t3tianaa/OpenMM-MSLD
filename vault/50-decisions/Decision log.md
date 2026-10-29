---
title: Decision log
type: meta
status: active
updated: 2026-09-27
---
# Decision log (ADR index)

Architecture Decision Records. Rules: one decision per ADR; `accepted` ADRs are not edited, only
superseded ([[Conventions]]). An ADR becomes `superseded` only when its replacement is `accepted`;
a decision known to be wrong but not yet replaced is `deprecated`. ADR-0001…0030 were **reconstructed on 2026-09-27** from git history,
the old documents and earlier Claude session memory (`retrospective: true`); dates are best
estimates. ADR-0031+ are current.

| ADR | decision | status |
|---|---|---|
| [[ADR-0001 Build MSLD natively in OpenMM\|ADR-0001]] | Build MSLD natively in OpenMM | accepted |
| [[ADR-0002 BLaDE is the reference and validation oracle\|ADR-0002]] | BLaDE is the reference and validation oracle | accepted |
| [[ADR-0003 Amber is the production force field target\|ADR-0003]] | Amber is the production force field; CHARMM for validation | accepted |
| [[ADR-0004 Correctness first in Python on stock OpenMM\|ADR-0004]] | Correctness first: Python engine on stock OpenMM | accepted |
| [[ADR-0005 Lambda as softmax of fnex sin theta\|ADR-0005]] | λ = softmax of fnex·sin θ | accepted |
| [[ADR-0006 Bonded scaling via grouped custom forces\|ADR-0006]] | Bonded scaling by grouped custom forces | accepted |
| [[ADR-0007 Charges scaled by NonbondedForce offsets\|ADR-0007]] | Charges scaled by NonbondedForce parameter offsets | accepted |
| [[ADR-0008 LJ scaled by grouped CustomNonbondedForces\|ADR-0008]] | LJ scaled by grouped CustomNonbondedForces | accepted |
| [[ADR-0009 Within-block real-space electrostatics linear\|ADR-0009]] | Within-block real-space elec made linear (λ), reciprocal λ² | accepted |
| [[ADR-0010 Same-site pairs excluded in every nonbonded force\|ADR-0010]] | Same-site pairs excluded in every nonbonded force | accepted (reciprocal part reopened by ADR-0036) |
| [[ADR-0011 Master invariant as the primary gate\|ADR-0011]] | Master invariant λ = 1 ≡ base as the primary gate | accepted |
| [[ADR-0012 Python driver integrator instead of CustomIntegrator\|ADR-0012]] | Python driver integrator instead of CustomIntegrator | accepted |
| [[ADR-0013 Tier 0 analytic dU-dlambda via force groups\|ADR-0013]] | Tier 0: analytic dU/dλ via force groups, FD only group 0 | accepted |
| [[ADR-0014 Bonded scaling on by default\|ADR-0014]] | Bonded scaling on by default; production turns bond/angle off | accepted (replacement proposed: ADR-0041) |
| [[ADR-0015 ParmEd Structure as prep common representation\|ADR-0015]] | ParmEd Structure as prep's common representation | accepted |
| [[ADR-0016 Prep emits a plain System\|ADR-0016]] | Prep emits a plain System; engine applies all MSLD changes | accepted |
| [[ADR-0017 Staged prep pipeline\|ADR-0017]] | Staged prep pipeline (ingest → map → assemble) | accepted |
| [[ADR-0018 Two ingest modes and NBFIX recovery\|ADR-0018]] | Two ingest modes; prefer lossless; recover NBFIX | accepted |
| [[ADR-0019 Core defined by identity and equal LJ\|ADR-0019]] | Core = same name/graph position AND same LJ; MCS for ligands | accepted |
| [[ADR-0020 Variants as monomer residues\|ADR-0020]] | Variants are monomer residues parametrized with ignoreExternalBonds | accepted |
| [[ADR-0021 Charge averaging, renormalization, iso-charge guard\|ADR-0021]] | Average env charges, renormalize blocks, refuse charge changes | accepted |
| [[ADR-0022 Solvation by overlay after grafting\|ADR-0022]] | Solvate by overlay after grafting | accepted |
| [[ADR-0023 Restraint groups per block centroid\|ADR-0023]] | Atom restraints: one group per block, to its own centroid | deprecated (known wrong; replacement ADR-0033 proposed) |
| [[ADR-0024 Home-grown ALF heuristic\|ADR-0024]] | Home-grown ALF heuristic (fixed + coupling biases) | deprecated (replacement ADR-0034 proposed) |
| [[ADR-0025 Soft-core off in the first version\|ADR-0025]] | Soft-core off in the first version | superseded by ADR-0043 |
| [[ADR-0026 Tier 2 plugin with scope S0 to S4\|ADR-0026]] | Tier 2: C++ plugin with scope S0–S4 | accepted (gated by ADR-0035) |
| [[ADR-0027 Plugin technology choices\|ADR-0027]] | Plugin technology: common compute layer, Reference first, SWIG; Mac dev / CUDA prod | accepted |
| [[ADR-0028 Refuse what cannot be scaled\|ADR-0028]] | Refuse what cannot be scaled (CMAP, cross-site 1-4, charge change) | accepted (extended by ADR-0037) |
| [[ADR-0029 Tests as self-running scripts\|ADR-0029]] | Tests as self-running scripts, one file per feature | accepted |
| [[ADR-0030 Hard dependencies and a ParmEd-free engine\|ADR-0030]] | Hard dependencies; engine stays ParmEd-free | accepted |
| [[ADR-0031 Project knowledge system in an Obsidian vault\|ADR-0031]] | Project knowledge system: Obsidian vault in git, ADRs, IDs | accepted |
| [[ADR-0032 Three subsystems preparation simulation analysis\|ADR-0032]] | Three subsystems: preparation, simulation, analysis | accepted |
| [[ADR-0033 Atom restraints group equivalent atoms\|ADR-0033]] | Atom restraints group equivalent atoms across substituents | proposed |
| [[ADR-0034 Adopt published ALF and two-leg ddG\|ADR-0034]] | Adopt the published ALF and a two-leg ΔΔG analysis | proposed |
| [[ADR-0035 Gate plugin work\|ADR-0035]] | Gate plugin work behind the θ-unit check and a BLaDE cross-check | proposed |
| [[ADR-0036 Same-site reciprocal-space convention\|ADR-0036]] | Same-site reciprocal-space convention | proposed |
| [[ADR-0037 Whitelist force types\|ADR-0037]] | Whitelist force types; raise on anything else touching alchemical atoms | proposed |
| [[ADR-0038 Theta units and default theta mass\|ADR-0038]] | θ units and default θ mass/friction equivalent to BLaDE | proposed |
| [[ADR-0039 Dispersion correction handling\|ADR-0039]] | Dispersion correction handling | proposed |
| [[ADR-0040 Supported nonbonded methods\|ADR-0040]] | Supported nonbonded methods: PME and NoCutoff only | proposed |
| [[ADR-0041 Default bonded scaling follows BLaDE practice\|ADR-0041]] | Default bonded scaling follows BLaDE removescaling practice | proposed |
| [[ADR-0043 Soft-core on by default for overlap-prone pairs\|ADR-0043]] | Soft-core on by default for overlap-prone pairs | accepted |
| [[ADR-0044 Own SHAKE in the Python driver\|ADR-0044]] | Own SHAKE in the Python driver | accepted |
| [[ADR-0045 Analytic biases and a large FD step\|ADR-0045]] | Analytic biases and a large FD step | accepted |

Dataview (live, needs the plugin):
```dataview
TABLE status, date, retrospective
FROM "50-decisions"
WHERE type = "adr"
SORT id ASC
```

