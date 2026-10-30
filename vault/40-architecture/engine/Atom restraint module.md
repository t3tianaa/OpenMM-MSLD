---
title: Atom restraint module
type: component
subsystem: "[[Simulation subsystem]]"
layer: L3
status: partial
code: [msld/forces.py, msld/prep/mapping/core.py]
requirements: ["[[REQ-014 Atom restraints between substituents|REQ-014]]"]
decisions: ["[[ADR-0023 Restraint groups per block centroid|ADR-0023]]", "[[ADR-0033 Atom restraints group equivalent atoms|ADR-0033]]"]
issues: ["[[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]]", "[[ISS-023 Restrained-atom bonded scaling rule missing|ISS-023]]"]
updated: 2026-09-27
---
# Atom restraint module — `add_atom_restraints`

For each group in `model.atom_restraints` with n ≥ 2 atoms: pairwise `CustomBondForce("0.5*kr*r^2")`
with `kr = k_restraint / n` for every pair — identical to BLaDE's
`½k Σ|x_i − x̄|²` by the centroid identity ([[Atom restraints between substituents]]). Not λ-scaled.

**The math is right; the groups are wrong.** Prep (`model_from_mappings(add_restraints=True)`,
default) creates one group per **block containing all of its atoms**. BLaDE's groups are
**equivalent atoms across substituents** ([[BLaDE atom restraints and soft bonds]]). Effect: each
side chain is squeezed toward its own centroid with 24 769 kJ/mol/nm² per atom — ≈ 500 kJ/mol per
atom for a 0.2 nm spread, distorting every variant ([[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]]). Target design ([[ADR-0033 Atom restraints group equivalent atoms|ADR-0033]]):
- groups = {atom a in block 1, equivalent atom in block 2, …} from the mapping's core
  correspondence, only where substituents carry duplicated core atoms;
- default off for plain side-chain mutations (no duplicated atoms);
- `k` configurable; note BLaDE/CHARMM scaling differences (59.2 vs 59.2·n/(n−1)).

Also missing: the pairwise form costs O(n²) bonds per group (fine for small n).

