---
title: MSLD energy function spec
type: contract
status: frozen
layer: L2
requirements: ["[[REQ-020 Accurate dU-dlambda for every term|REQ-020]]", "[[REQ-011 Soft-core for alchemical nonbonded|REQ-011]]", "[[REQ-016 Canonical sampling of atoms and theta|REQ-016]]"]
decisions: ["[[ADR-0043 Soft-core on by default for overlap-prone pairs|ADR-0043]]", "[[ADR-0038 Theta units and default theta mass|ADR-0038]]", "[[ADR-0035 Gate plugin work|ADR-0035]]"]
updated: 2026-10-31
---
# MSLD energy function spec (what the plugin must reproduce)

Frozen 2026-10-31 at sync branch `msld-phase1-sync-2026-09-27` after PR #5. This is the as-built
energy of the Python engine (`msld/forces.py`), validated at partial λ by the independent NumPy
oracle `tests/msld_oracle.py` (1e-8, [[TASK-067 NumPy partial-lambda oracle tests|TASK-067]]). **Plugin S1 must reproduce
`tests/data/oracle_toy.json`.** Units: nm, kJ/mol, e, rad, ps; KE = 138.935456 (OpenMM ONE_4PI_EPS0).

## λ from θ
λ_b = exp(fnex·sin θ_b) / Σ_{c ∈ site} exp(fnex·sin θ_c), fnex = 5.5; block 0 (environment) has
λ = 1. dU/dθ_i = λ_i·fnex·cos θ_i·(dU/dλ_i − Σ_{j ∈ site} λ_j·dU/dλ_j).

## Pair classes (atoms i, j; b(i) = block, 0 = environment)
| class | L |
|---|---|
| both environment | 1 (plain, never soft-cored) |
| same block b (1-5+ pairs) | λ_b |
| environment + block b | λ_b |
| blocks b, c at different sites | λ_b·λ_c |
| different blocks of the same site | excluded entirely (also from PME) |

1-2 and 1-3 pairs are excluded; 1-4 pairs only interact through their 1-4 term.

## Nonbonded, L < 1 (soft-core α = 0.5, σ_q = 0.3 nm; α = 0 = plain linear scaling)
- **LJ (Beutler):** U = L·4ε·(1/s² − 1/s), s = (r/σ)⁶ + α(1 − L); Lorentz–Berthelot σ, ε (CHARMM
  NBFIX: per-pair σ⁶ = a²/b, 4ε = b²/a² from ParmEd's acoef/bcoef tables). Same cutoff/switch as the
  NonbondedForce. **No long-range dispersion correction** (deferred).
- **Coulomb, real space:** U = L·KE·q_i q_j·g(r_sc), r_sc = (r⁶ + α(1 − L)σ_q⁶)^(1/6), g = 1/r
  (NoCutoff), erfc(α_E r)/r (PME, α_E exactly the NonbondedForce's), or reaction field.
- **Coulomb, reciprocal space (PME):** charges q_i·λ_b(i) on the grid. So env–block pairs carry λ_b,
  cross-site λ_bλ_c and **within-block λ_b²** in reciprocal space — as BLaDE. Only the real-space
  part is linear in λ_b within a block.
- In the Python engine this is: NonbondedForce with charge offsets (λ_b q), a within-block real-space
  correction (λ − λ²)·KE·qq·g(r) and a soft-core correction L·KE·qq·[g(r_sc) − g(r)]. The plugin
  should compute the sum directly.

## 1-4 terms
U = L·[KE·qq₁₄/r + 4ε₁₄((σ₁₄/r)¹² − (σ₁₄/r)⁶)] with L as above, **no soft-core**. A 1-4 between
blocks of different sites, or of the same site, is not supported (raises).

## Bonded
Each bond/angle/torsion/improper is multiplied by the product of the distinct non-environment λ's of
its atoms (≤ 2 factors; a term spanning two blocks of one site is illegal). Per-type switches
`scale_bond`, `scale_angle`, `scale_torsion` (BLaDE removescaling); MDM2 runs use bonds and angles
unscaled. Bonded terms stay as stock OpenMM custom forces in the plugin era.

## Biases (ALF)
U = Σ_b c_b·λ_b + Σ variable (i, j, type, l0, k): type 6 k·λ_iλ_j; type 8 k·λ_iλ_j/(λ_i + l0)
(l0 = 0.017); type 10 k·λ_j·(1 − exp(l0·λ_i)) (l0 = −5.56). Sign is **+** (published ALF writes
the negatives; see [[ALF package overview]]).

## Restraints
Optional, off by default (PR #2): 0.5·k·Σ|x_i − x̄|² per group, not λ-scaled.

## Dynamics (Python engine)
VRORV Langevin on atoms and θ, dt 1 fs, atom friction 1 ps⁻¹ (BLaDE uses 0.1), SHAKE/RATTLE on
constraints. θ mass 0.05 amu·nm², θ friction 1 ps⁻¹ per block ([[ADR-0038 Theta units and default theta mass|ADR-0038]]). dU/dλ is analytic
for everything except the NonbondedForce part (finite difference, h = 1e-2, exact because that part
is quadratic in λ); the plugin replaces the finite difference with the analytic kernel derivative.

## Not covered by the oracle
PME reciprocal space at partial λ (only NoCutoff is checked), NBFIX tables, cutoffs and switching.
The plugin's Reference platform should add an Ewald-sum or Python-engine comparison for these.
