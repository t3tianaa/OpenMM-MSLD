---
title: MSLD model component
type: component
subsystem: "[[Simulation subsystem]]"
layer: L2
status: as-built
code: [msld/model.py]
requirements: ["[[REQ-001 Represent sites, blocks and environment|REQ-001]]", "[[REQ-002 Lambda from theta with implicit constraints|REQ-002]]", "[[REQ-004 Configurable bonded scaling per term type|REQ-004]]", "[[REQ-012 Fixed and variable lambda biases|REQ-012]]", "[[REQ-014 Atom restraints between substituents|REQ-014]]", "[[REQ-017 Per-block theta mass, friction and fixing|REQ-017]]"]
decisions: ["[[ADR-0005 Lambda as softmax of fnex sin theta|ADR-0005]]", "[[ADR-0014 Bonded scaling on by default|ADR-0014]]"]
issues: ["[[ISS-002 Theta mass convention differs from BLaDE|ISS-002]]", "[[ISS-019 Fixed-block lambda semantics differ from BLaDE|ISS-019]]"]
updated: 2026-09-27
---
# MSLD model component — `msld/model.py`

## Purpose
Pure-Python data model of an MSLD setup, mirroring BLaDE's `Msld` class
([[BLaDE MSLD data model]]). No OpenMM objects (imports lazily only in `scale_system`).

## Content (see [[MSLD model data contract]])
- `Block(index, site, atoms, theta0, theta_velocity0, theta_mass=5.0, theta_friction=1.0,
  lambda_bias=0.0, fixed=False)`; block 0 = environment.
- `VariableBias(i, j, type, l0, k, n)` — BLaDE LDBV.
- `MSLDModel(n_atoms, fnex=5.5)`: `blocks`, `atom_block[]`, `variable_biases`,
  `scale_bond / scale_angle / scale_torsion` (removescaling; impropers follow torsion),
  `bias_flattening`, `atom_restraints` (list of groups), `k_restraint = 24769 kJ/mol/nm²`.

## Behaviour
- `add_block(site, atoms, **block_kw)`: atoms in range, not already owned.
- `finalize()`: blocks ordered by consecutive sites; site 0 exactly one block; each site ≥ 2 blocks
  or one fixed block; computes `site_bound`, `n_sites` (BLaDE `initialize`).
- `classify_bonded(atoms)` → `[]` env-only, `[b]`, `[b, c]` (different sites); raises for same-site.
- `classify_pair(i, j)` → `("env",)`, `("single", b)`, `("product", b, c)`, `("exclude",)`.
- `lambda_from_theta(theta)` — per-site softmax of `fnex·sin θ` ([[Implicit constraints and the softmax of sin theta]]).
- `scale_system(system)` = `builder.scale_msld_system(system, self)`.

## Gaps
- θ mass/friction defaults (5 / 1) copied as numbers from BLaDE, but the unit meaning differs
  ([[ISS-002 Theta mass convention differs from BLaDE|ISS-002]], [[BLaDE units and theta mass]]).
- `fixed` blocks: θ frozen but λ still from the softmax; BLaDE uses the given λ and renormalizes
  the rest ([[ISS-019 Fixed-block lambda semantics differ from BLaDE|ISS-019]]).
- Only 3 removescaling switches (BLaDE has 6) ([[REQ-004 Configurable bonded scaling per term type|REQ-004]]).
- No θ biases, soft-core flags, soft bonds, charge restraints, ewald-type option.

