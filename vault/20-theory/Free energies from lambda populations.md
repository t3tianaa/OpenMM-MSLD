---
title: Free energies from lambda populations
type: theory
status: reviewed
related: ["[[Multisite lambda dynamics]]", "[[Free energy estimators]]", "[[REQ-030 Adaptive landscape flattening]]"]
updated: 2026-09-27
---
# Free energies from λ populations

**In one sentence.** The free energy of molecule *l* is −kT times the log of the fraction of frames
in which every site shows *l*'s substituent, minus the bias that was applied to that end state.

## Formula

```
 G_E(l) = −kT · ln ⟨ Π_s Θ(λ_{s,i_l}(t) − λ_c) ⟩_t  −  U_bias({λ}_l)
```

- `Θ(x)` = 1 if x > 0 else 0 → "is this substituent fully present?" (λ_c = 0.99, sometimes 0.8)
- `Π_s` — all sites must be physical at once
- `⟨…⟩_t` — fraction of frames
- `−kT ln` — Boltzmann: probability → free energy
- `U_bias({λ}_l)` — the bias energy at that end state (λ = 1 for l's substituents, 0 otherwise);
  subtracting it removes the effect of the bias.

`ΔG_E(l₁ → l₂) = G_E(l₂) − G_E(l₁)` within one environment; ΔΔG from two environments
([[Thermodynamic cycles for relative free energies]]).

![[Pasted image 20260714171934.png|600]]
*(figure kept from the original notes)*

## Fraction of physical ligands (FPL)

```
 FPL = Σ_l ⟨ Π_s Θ(λ_{s,i_l} − λ_c) ⟩_t        = fraction of frames that are usable
```

- FPL ≥ 0.01 is usually workable; > 0.5 may signal too few transitions.
- With the bare fnex softmax, a site with 2 substituents has FPL ≈ 0.44, 3 → 0.28, 9 → < 0.01, and
  it roughly halves per additional substituent; sites multiply (two sites at 0.01 → 0.0001).
  θ biases counter this ([[Biasing potentials in MSLD]]).

![[Pasted image 20260714174028.png|500]]
*(figure kept from the original notes)*

## Estimator notes
- The simple counting estimator is unbiased only with enough **transitions** between end states;
  single short runs are meaningless ([[EXP-001 Theta samples the exact Boltzmann distribution on a toy|EXP-001]]).
- Better estimators reweight all frames (WHAM/MBAR on λ), which ALF does for production
  analysis ([[Free energy estimators]], [[ALF package overview]]).
- An endpoint-population readout is *not* distorted by the softmax: with no energy differences all
  blocks at a site have the same end-point probability by symmetry. (This corrects a claim in
  `msld/alf.py`, see [[ISS-011 ALF is a heuristic and ddG is single-leg|ISS-011]].)

## Sources
- Knight & Brooks 2011 (JCTC 7, 2728); Hayes et al. 2017 (JPCB 121, 3626). FPL numbers from the
  θ-bias work of Hayes and co-workers (citation to verify, [[TASK-076 Pin literature citations|TASK-076]]).

