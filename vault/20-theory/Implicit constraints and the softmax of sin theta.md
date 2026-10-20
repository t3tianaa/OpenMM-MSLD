---
title: Implicit constraints and the softmax of sin theta
type: theory
status: reviewed
related: ["[[Lambda dynamics]]", "[[Theta force by the chain rule]]", "[[BLaDE lambda from theta and theta force]]"]
updated: 2026-09-27
---
# Implicit constraints: λ as a softmax of sin θ

**In one sentence.** Instead of integrating λ (bounded, summing to 1) we integrate free variables θ
and define λ as a function of θ that always satisfies the constraints.

## The formula

```
   per site s:   w_i = exp( fnex · sin θ_i )        λ_i = w_i / Σ_{j∈s} w_j
```

- `sin θ` squeezes the unbounded θ into [−1, 1];
- `exp` makes every weight positive → every λ ≥ 0;
- dividing by the sum is a **softmax** → Σ λ = 1 automatically;
- `fnex` (usually **5.5**) sets the sharpness: large fnex → the block with the largest sin θ gets
  λ ≈ 1, the others ≈ 0, so the system spends more time near physical end states.

To reach λ_i > 0.99, θ_i must be near +π/2 (sin = +1) and every other θ near −π/2. With many
substituents this becomes rare (see FPL in [[Free energies from lambda populations]]).

## Properties worth knowing
- θ is periodic (period 2π); λ is smooth in θ.
- The uniform θ distribution does **not** give uniform λ: the softmax itself prefers end states.
  Any bias-flattening target must be measured against this *bare softmax reference*, not against
  "uniform λ" (a lesson from ALF Phase 2, see [[ALF flattening component]]).
- A **fixed** block (λ held constant, FEP-style) is excluded from the softmax; the others are
  renormalized to `1 − Σ λ_fixed` (BLaDE, [[BLaDE lambda from theta and theta force]]).
- Alternative implicit constraints exist (BLaDE also has a "piecewise / Newton" constraint,
  `msld piecewise on`); we only implement the fnex form.

## Sources
- Knight & Brooks, *J. Comput. Chem.* 32, 3423 (2011) — implicit constraints.
- BLaDE `src/msld/msld.cu:863-906` ([[BLaDE lambda from theta and theta force]]).

