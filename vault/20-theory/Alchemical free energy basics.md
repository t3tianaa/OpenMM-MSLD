---
title: Alchemical free energy basics
type: theory
status: reviewed
related: ["[[Lambda dynamics]]", "[[Free energy estimators]]", "[[Thermodynamic cycles for relative free energies]]"]
updated: 2026-09-27
---
# Alchemical free energy basics

**In one sentence.** To get the free-energy difference between molecules A and B, we simulate a
non-physical path that gradually turns A into B, controlled by a coupling parameter λ.

## The idea

Nature cannot turn a leucine into an isoleucine, but a simulation can. We write a potential that
mixes both end states:

```
   U(λ) = (1 − λ)·U_A + λ·U_B          λ = 0 → pure A,  λ = 1 → pure B
```

Because free energy is a state function, the path does not matter — only the end states. Any
smooth, non-physical path gives the right ΔG if it is sampled well enough.

## Two classic ways with fixed λ

- **Free energy perturbation (FEP)** — Zwanzig: `ΔG = −kT ln ⟨exp(−(U_B − U_A)/kT)⟩_A`. In practice
  split into windows λ = 0, 0.1, …, 1 and chain them.
- **Thermodynamic integration (TI)** — `ΔG = ∫₀¹ ⟨∂U/∂λ⟩_λ dλ`, integrated numerically over windows.

Both keep λ **fixed** in each window: one simulation per window, one set of windows per pair of
molecules. For N molecules that is O(N) or O(N²) calculations.

## Where λ-dynamics differs

λ-dynamics makes λ a **dynamic variable** that moves during one simulation, so the simulation
itself spends time near the end states in proportion to exp(−G/kT) — see [[Lambda dynamics]] and
[[Multisite lambda dynamics]].

## Pitfalls that matter for us
- **End-point catastrophe** — at λ → 0 a vanishing atom's LJ core disappears and other atoms can
  overlap it; forces and ∂U/∂λ diverge. Cure: soft-core ([[Soft-core potentials]]).
- **Dummy atoms** — atoms that vanish keep their bonded terms so they stay attached; this does not
  change ΔG if handled consistently in both legs ([[Bonded terms and dummy atoms in alchemy]]).
- **Net charge changes** break PME/finite-size assumptions ([[Net charge changes in alchemical calculations]]).

## Sources
- Zwanzig, R. W. *J. Chem. Phys.* 22, 1420 (1954) — FEP.
- Kirkwood, J. G. *J. Chem. Phys.* 3, 300 (1935) — TI.
- Mey, A. S. J. S. et al. "Best Practices for Alchemical Free Energy Calculations", *Living J.
  Comp. Mol. Sci.* 2, 18378 (2020).

