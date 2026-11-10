---
id: EXP-013
type: experiment
title: Plugin PME against a plain Ewald sum
status: done
date: 2026-11-09
requirements: ["[[REQ-020 Accurate dU-dlambda for every term|REQ-020]]"]
issues: ["[[ISS-029 Partial-lambda PME energy depends on alpha|ISS-029]]"]
related: ["[[MSLD energy function spec]]", "[[Production plugin architecture]]"]
---
# EXP-013 — Plugin PME against a plain Ewald sum

Independent reference for partial-λ PME, closing the gap listed under "Not covered by the oracle" in the
[[MSLD energy function spec]]. Code: `python/tests/ewald_reference.py` and `test_ewald_reference.py` in openmm-ld: a direct
k-space sum from the spec, NumPy only, complex-step dU/dλ.

**The reference on its own:** NaCl Madelung constant to 1e-12; total independent of α to 1e-11 where theory requires it;
k-sum converged to below 1e-11 kJ/mol.

**Against the plugin:** oracle toys (24 atoms, 5 blocks, 2 sites, normal and overlap geometry) in a 3.2 nm box, cutoff
1.0 nm, 4 λ vectors each, same α and cutoff on both sides, so the difference is the PME grid error.

| Ewald tolerance | α (nm⁻¹) | grid | max energy error, normal / overlap (kJ/mol) | max dU/dλ error, normal / overlap (kJ/mol) |
|---|---|---|---|---|
| 5e-4 | 2.628 | 26 | 2.9e-3 / 1.3e-2 | 5.1e-3 / 1.3e-2 |
| 1e-5 | 3.289 | 71 | 3.8e-5 / 1.4e-4 | 4.4e-5 / 9.2e-5 |
| 1e-6 | 3.622 | 123 | 2.9e-6 / 2.5e-6 | 2.5e-6 / 6.1e-5 |
| 1e-7 | 3.927 | 211 | 2.7e-7 / 8.3e-7 | 2.0e-7 / 4.6e-5 |

**Reading:** the error falls with the tolerance as PME should, so partial-λ PME implements the spec. The dU/dλ error on the
overlap geometry stops falling near 5e-5, on a dU/dλ of order 1e4–1e6 kJ/mol; that is rounding on huge numbers (Inferred).

**Limit:** this checks the plugin against the spec, not the spec against the physics or BLaDE ([[TASK-043 BLaDE fixed-lambda cross-check|TASK-043]]). Not covered:
reaction field at partial λ, NBFIX, forces (those rest on finite differences of the energy).
