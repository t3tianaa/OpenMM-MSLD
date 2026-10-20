---
title: Adaptive landscape flattening
type: theory
status: draft
related: ["[[Biasing potentials in MSLD]]", "[[ALF package overview]]", "[[ALF flattening component]]"]
sources: [Hayes et al 2017]
updated: 2026-09-27
---
# Adaptive landscape flattening (ALF)

**In one sentence.** An iterative procedure that runs short MSLD simulations, looks at the λ
distributions, and updates the bias parameters until the alchemical landscape is flat — then the
converged biases (plus a final reweighting) give the free energies.

## The loop

```
   biases (b, c, x, s) = 0
   repeat:
      run a short MSLD simulation (or several replicas)
      collect λ samples (every ~10 steps)
      build 1-D λ histograms per block and 2-D histograms per block pair
      choose bias changes Δb, Δc, Δx, Δs that would make the (reweighted) histograms flat
      update biases; lengthen simulations as the landscape flattens
   until end states are sampled evenly and transitions are frequent
   production: long runs with fixed biases → free energies by reweighting (WHAM/MBAR on λ)
```

## Bias families fitted

Per block: fixed linear `b_i`. Per block pair at the same site: quadratic `c_ij` (type 6), skew
`x_ij` (type 10, l0 = −5.56), end-point `s_ij` (type 8, l0 = 0.017); the skew and end-point terms
are applied in both directions (i,j) and (j,i) — see the generated BLaDE input `test/HSP90/cb7.inp`
([[BLaDE T4L and HSP90 examples]]).

## How the update is computed (to be verified)

The published method estimates the bias change from the current λ histograms by reweighting the
samples from recent iterations with trial biases and choosing the change that makes the target
(flat) distribution most likely, with regularization to keep updates stable. Later versions of the
ALF package use likelihood maximization over several past iterations. **Status: the exact
objective, regularization and schedule must be read from the ALF source before we implement it**
([[TASK-074 Study the ALF package|TASK-074]], [[ALF package overview]]).

## What our code does instead (as of 2026-09-27)

`msld/alf.py` implements a home-grown heuristic: `b += rate·kT·ln(p/p_target)` and a type-6 coupling
nudged toward the bare-softmax overlap. It recovers injected ΔG on toys but it is **not** ALF
([[ISS-011 ALF is a heuristic and ddG is single-leg|ISS-011]], [[ADR-0024 Home-grown ALF heuristic|ADR-0024]], proposed replacement [[ADR-0034 Adopt published ALF and two-leg ddG|ADR-0034]]).

## Pitfalls
- The flat target must account for the softmax's own preference for end states (a uniform-λ
  target drives the coupling the wrong way — found the hard way, [[EXP-009 Heuristic ALF on toys|EXP-009]]).
- Short runs give noisy histograms → updates must be damped; judge convergence on many
  iterations.

## Sources
- Hayes, R. L.; Armacost, K. A.; Vilseck, J. Z.; Brooks, C. L. III. *J. Phys. Chem. B* 121, 3626
  (2017).
- ALF package: github.com/RyanLeeHayes/ALF (not yet studied in this project).

