---
title: Finite differences and floating-point precision
type: theory
status: reviewed
related: ["[[Force groups and derivative routing]]", "[[OpenMM platforms and precision]]"]
updated: 2026-09-27
---
# Finite differences and floating-point precision

Central difference: `f'(λ) ≈ [U(λ+h) − U(λ−h)] / 2h`.

```
 total error ≈  truncation  +  round-off
             ≈  (h²/6)·|U'''|  +  ε_U / h
 ε_U = absolute error of one energy evaluation ≈ ε_machine · |U| (and summation error)
```

Example (our MDM2 engine, [[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]): group-0 energy |U| ~ 10⁵–10⁶ kJ/mol; fp32 ε ≈ 6·10⁻⁸ →
ε_U ≈ 0.1 kJ/mol; h = 10⁻⁴ → noise ≈ 0.1/2·10⁻⁴ ≈ **500 kJ/mol** per evaluation. That random θ
force acts like heat. Remedies: double/mixed precision, differentiate only the small λ-dependent
part (not the whole system energy), or analytic derivatives (the real fix).

Also: fixed-point accumulation (OpenMM's 64-bit force accumulation) is how GPUs sum many small
contributions without order-dependent round-off — needed for a GPU dU/dλ ([[ADR-0027 Plugin technology choices|ADR-0027]]).
