---
title: BLaDE pressure coupling
type: reference
status: verified
system: blade
version: c677277
related: ["[[Pressure control and the Monte Carlo barostat]]", "[[OpenMM barostat mechanics]]"]
updated: 2026-09-27
---
# BLaDE pressure coupling

Source: `src/update/pressure.cu:114-180`; called at the start of `State::update` every `freqnpt`
steps (`update.cu:237`).

```
 E_old = potential energy (incl. λ biases, restraints)
 scale box uniformly (orthogonal boxes only) → recompute forces/energy → E_new
 N  = atoms − constraints (counted per constraint cluster)
 dW = E_new − E_old + P·(V_new − V_old) − N kT ln(V_new/V_old)
 accept if rand < exp(−dW/kT), else restore positions
```
θ and λ are untouched by the move. Examples use `freqnpt 100`; the doc recommends ≤ 10 for bulk
dynamics and an rms volume move ≈ √V·1 Å³.

