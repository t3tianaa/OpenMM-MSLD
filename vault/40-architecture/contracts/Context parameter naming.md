---
title: Context parameter naming
type: contract
status: as-built
code: [msld/forces.py]
updated: 2026-09-27
---
# Data contract: Context global parameter names

| name | owner | meaning |
|---|---|---|
| `lambda{b}` (b ≥ 1) | every scaled force touching block b | λ of block b; default 1.0 |
| `biascoef{b}` | `MSLDBias` | fixed linear bias coefficient of block b |
| `biask{m}` | `MSLDBias` | k of the m-th variable bias |

Force names: `MSLDLJ_b`, `MSLDLJ_b_c`, `MSLDWBElec_b`, `MSLDBias`, `MSLDAtomRestraint`, and the
custom bonded forces per signature. `add_scaled_charmm_lj` ignores forces whose name starts with
`MSLD`. Force groups: 1 = analytic, 0 = finite-difference remainder
([[Force groups and derivative routing]]).

