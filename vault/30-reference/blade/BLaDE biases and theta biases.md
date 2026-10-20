---
title: BLaDE biases and theta biases
type: reference
status: verified
system: blade
version: c677277
related: ["[[Biasing potentials in MSLD]]", "[[Bias module]]"]
updated: 2026-09-27
---
# BLaDE biases and θ biases

## Fixed bias (`msld.cu:1000-1040`)
`U = Σ_b lambdaBias[b]·λ_b`; `∂U/∂λ_b = lambdaBias[b]`. Set by the 6th argument of
`msld initialize`.

## Variable biases (`getforce_variableBias_kernel`, `msld.cu:1042-1129`)

| type | energy | ∂U/∂λ_i | ∂U/∂λ_j |
|---|---|---|---|
| 6 | `k λi λj` | `k λj` | `k λi` |
| 8 | `k λi λj/(λi + l0)` | `k l0 λj/(λi+l0)²` | `k λi/(λi+l0)` |
| 10 | `k λj (1 − e^{l0 λi})` | `−k l0 λj e^{l0 λi}` | `k (1 − e^{l0 λi})` |
| 1 | `k (λi − l0)^n` if λi < l0 | … | 0 |
| 2 | `k (λi − l0)^n` if λi > l0 | … | 0 |
| 3 | `k (λi − λj)^n` | … | … |
| 4 | flat-bottom well | … | 0 |
| 5 | `−k λi` | `−k` | 0 |
| 7 | `k λi(1−λi)/(λi+l0)` | … | 0 |
| 9 | `k λj (1 − ((λi+l0)/l0)^n)` | … | … |
| 11 | `k λi^{l0} λj^n` | … | … |
| 12 | `k λi λj^n/(λi+l0)` | … | … |

The parser accepts types 1–12 (`msld.cu:239-258`); ALF uses 6, 8 (l0 = 0.017), 10 (l0 = −5.56).
Our engine implements 6, 8, 10 with the same formulas (checked in the audit).

## θ biases (`msld.cu:1155-1204`, parser `msld.cu:259-329`)
- **collective** (per site, parameters k, n):
  `n₊ = Σ(½ sin φ + ½)^n`, `n₋ = Σ(−½ sin φ + ½)^n`,
  `U = ½k[(n₊ − 1)² + (n₋ − (N−1))²]`, φ = ANGSTROM·θ.
- **independent** (per site, parameter k): `U = Σ_i k(1 − s_i⁴)`, `s_i = ½ − ½ sin φ_i`.
  `auto Ns T` solves `k ← ½ ln(¼·k·Ns²·π/2)` by 50 fixed-point iterations, clamps at 0, then
  multiplies by k_B T (`msld.cu:300-322`).
- Piecewise-constraint extras: flat-bottom harmonic on θ and a target-count bias (`msld.cu:1206-1276`).

θ biases act directly on θ (`thetaForce`), not through λ.

