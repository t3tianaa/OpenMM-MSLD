---
title: Ewald summation and PME
type: theory
status: reviewed
related: ["[[PME with lambda-scaled charges]]", "[[Reaction-field electrostatics]]", "[[BLaDE PME reciprocal space and exclusions]]"]
updated: 2026-09-27
---
# Ewald summation and particle-mesh Ewald (PME)

**In one sentence.** Long-range Coulomb in a periodic box is split into a short-range screened part
(summed directly, with a cutoff) and a smooth long-range part (summed in Fourier space), plus
self and exclusion corrections.

## The split

```
 1/r = erfc(α r)/r      +      erf(α r)/r
       short range              smooth, long range
       direct space             reciprocal space

 E_elec = E_direct + E_recip + E_self + E_excl

 E_direct = ½ Σ_{i≠j, not excluded, r<rc} k q_i q_j erfc(α r_ij)/r_ij
 E_recip  = (1/2V) Σ_{k≠0} (4π/k²) e^{−k²/4α²} |S(k)|²,   S(k) = Σ_i q_i e^{i k·r_i}
 E_self   = −(α/√π) k Σ_i q_i²
 E_excl   = −Σ_{excluded pairs} k q_i q_j erf(α r_ij)/r_ij       (remove what E_recip added)
```

k = Coulomb constant (138.935 kJ·nm/mol/e²). E_recip is a **quadratic form in the charges**:
`E_recip = ½ Σ_ij q_i q_j A_ij(r)`, where A_ij couples *every* pair, even i = j and excluded pairs;
that is why self and exclusion corrections are needed.

## PME
Charges are spread onto a grid with B-splines (order 4–8), FFT, multiplied by the Ewald kernel,
inverse FFT, and the potential/forces are gathered back with the same splines. Cost O(N log N).
α and the grid size set the accuracy (OpenMM derives them from `ewaldErrorTolerance` unless set
explicitly).

## Why it matters for MSLD
Reciprocal space has **no per-pair knob**; alchemical scaling can only act on charges →
[[PME with lambda-scaled charges]].

## Sources
- Essmann, U. et al. "A smooth particle mesh Ewald method." *J. Chem. Phys.* 103, 8577 (1995)
  (doi:10.1063/1.470117, cited in BLaDE `doc/citations`).
- Darden, T.; York, D.; Pedersen, L. *J. Chem. Phys.* 98, 10089 (1993).

