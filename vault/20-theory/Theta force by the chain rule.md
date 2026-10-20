---
title: Theta force by the chain rule
type: theory
status: reviewed
related: ["[[Implicit constraints and the softmax of sin theta]]", "[[Lambda dynamics]]"]
updated: 2026-09-27
---
# θ force by the chain rule

**In one sentence.** Forces give ∂U/∂λ; the integrator needs ∂U/∂θ; the softmax Jacobian turns one
into the other with a "competition" term.

## Derivation (one site)

```
 λ_j = w_j / Z,  w_j = e^{f sin θ_j},  Z = Σ_k w_k,  f = fnex
 ∂λ_j/∂θ_i = f cos θ_i · λ_i (δ_ij − λ_j)

 ∂U/∂θ_i = Σ_j (∂U/∂λ_j)(∂λ_j/∂θ_i)
         = λ_i · f · cos θ_i · ( d_i − Σ_j λ_j d_j )          d_j ≡ ∂U/∂λ_j
                                  \__/   \_________/
                                  own    site average
```

## Meaning of the competition term

Raising θ_i turns block i on **and** turns its site-mates off (Σλ = 1). So θ_i does not feel its
absolute d_i; it feels whether block i is better or worse than the **λ-weighted average** of its
site. The factor cos θ_i vanishes at θ = ±π/2: at a clean end state the θ-force is zero — which is
why a θ that has collapsed to an end state looks "cold" even when the thermostat is wrong
([[EXP-006 MDM2 theta-parameter sweep|EXP-006]]).

With fixed blocks (BLaDE): the average runs over the non-fixed blocks and is divided by
`R = 1 − Σ λ_fixed`.

## Sign conventions
BLaDE stores f = **+**∂U/∂x and subtracts it in the kick; OpenMM uses F = −∂U/∂x. Flip signs when
moving formulas between them ([[BLaDE integrator and update loop]]).

## Where it lives
Ours: `msld/integrator.py:LambdaDynamics.dUdtheta`. BLaDE: `msld.cu:937-985`.
Tested by finite differences in `test_integrator`.

