---
title: Biasing potentials in MSLD
type: theory
status: reviewed
related: ["[[REQ-030 Adaptive landscape flattening]]", "[[BLaDE biases and theta biases]]"]
updated: 2026-09-27
---
# Biasing potentials in MSLD

**In one sentence.** Artificial energy terms in λ (or θ) that flatten the landscape so the
simulation visits every end state and crosses between them.

## Why biases are needed

Variants differ by tens to thousands of kJ/mol in ∂U/∂λ. Unbiased, λ rolls to the most favourable
variant and stays there, or sticks at an intermediate. Populations are then useless. A bias equal
to −G(λ) makes the landscape flat; then all states are visited and the *bias itself* reveals G.

## λ biases (BLaDE / CHARMM `LDBV` types)

| name in ALF | BLaDE type | energy | shape |
|---|---|---|---|
| b (fixed) | fixed linear | `b_i λ_i` | shifts end-state free energies |
| c (quadratic) | **6** | `k λ_i λ_j` | barrier between i and j (0 at end points) |
| s (end-point) | **8**, l0 = 0.017 | `k λ_i λ_j / (λ_i + l0)` | sharp term near λ_i → 0 |
| x (skew) | **10**, l0 = −5.56 | `k λ_j (1 − exp(l0 λ_i))` | asymmetric shape |

(BLaDE also implements types 1–5, 7, 9, 11, 12; ALF uses 6/8/10. Formulas and derivatives:
`msld.cu:1042-1129`, [[BLaDE biases and theta biases]].)

## θ biases (for many substituents)

With many substituents the chance that exactly one θ is "up" is small (low FPL). Two θ biases:

```
 counters:  n₊ = Σ_i (½ sin θ_i + ½)^n      n₋ = Σ_i (−½ sin θ_i + ½)^n
 collective:  U = (k/2)(n₊ − 1)² + (k/2)(n₋ − (N_s − 1))²      "exactly one up, the rest down"
 independent: U = Σ_i k (1 − s_i⁴),  s_i = ½ − ½ sin θ_i       "each θ likes to be down"
```

(BLaDE code: `msld.cu:1155-1204`. The old notes wrote the independent form as −b·s⁴; BLaDE adds the
constant k, which does not change forces.) The independent coefficient can be chosen
automatically so that about two θ are "up" on average; for 2–3 substituents no positive solution
exists and it is 0. BLaDE's `auto` iteration is `k ← ½ ln(¼ k N² π/2)` (`msld.cu:316`; note
the ¼ differs from the formula in the old notes — check against the paper, [[TASK-076 Pin literature citations|TASK-076]]).

Reported effect: FPL held at 0.16–0.21 for 10–30 substituents with the collective bias.

## Sources
- Hayes et al. 2017 (ALF, JPCB 121, 3626) — bias families.
- θ-bias paper by Hayes and co-workers (citation to verify, [[TASK-076 Pin literature citations|TASK-076]]).
