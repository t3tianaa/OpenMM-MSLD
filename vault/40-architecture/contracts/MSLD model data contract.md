---
title: MSLD model data contract
type: contract
status: as-built
code: [msld/model.py]
updated: 2026-09-27
---
# Data contract: `MSLDModel`

| field | type / unit | meaning |
|---|---|---|
| `n_atoms` | int | size of the System |
| `fnex` | float (5.5) | softmax sharpness |
| `blocks[b]` | `Block` | index, site, atoms, theta0 (rad), theta_velocity0 (rad/ps), theta_mass (amu·nm²/rad² in effect, [[ISS-002 Theta mass convention differs from BLaDE\|ISS-002]]), theta_friction (ps⁻¹), lambda_bias (kJ/mol), fixed |
| `atom_block[a]` | int | block of atom a (0 = env) |
| `variable_biases` | list of `VariableBias(i, j, type, l0, k [kJ/mol], n)` | types 6/8/10 |
| `scale_bond`, `scale_angle`, `scale_torsion` | bool (default True) | removescaling |
| `bias_flattening` | bool | create tunable bias globals for all blocks |
| `atom_restraints` | list[list[int]] | restraint groups (see [[ADR-0033 Atom restraints group equivalent atoms\|ADR-0033]]) |
| `k_restraint` | kJ/mol/nm² (24 769) | per-atom restraint constant |
| after `finalize()`: `n_sites`, `blocks_per_site`, `site_bound` | | BLaDE-style bookkeeping |

Blocks must be added in site order. Changing a model after `scale_system` has no effect on the
System except via Context parameters (λ, bias coefficients).

