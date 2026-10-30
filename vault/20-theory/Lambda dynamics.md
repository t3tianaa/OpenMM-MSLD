---
title: Lambda dynamics
type: theory
status: reviewed
related: ["[[Multisite lambda dynamics]]", "[[Implicit constraints and the softmax of sin theta]]"]
sources: [Kong and Brooks 1996, Knight and Brooks 2009]
updated: 2026-09-27
---
# λ-dynamics

**In one sentence.** Give λ a fictitious mass and let it move under the force −∂U/∂λ together with
the atoms, so the simulation samples λ from its Boltzmann distribution.

## The idea

In FEP/TI we set the dial λ ourselves. In λ-dynamics the dial moves by itself. To move under the
laws of mechanics a coordinate needs a **mass**; so λ (or a variable that defines it) becomes an
extra particle with a made-up mass `m_λ`. This is an **extended Lagrangian**:

```
   L = Σ_atoms ½ m_i ẋ_i²  +  ½ m_λ λ̇²  −  U(x, λ)
```

Newton / Lagrange then gives, for the λ particle, `m_λ λ̈ = −∂U/∂λ`. A thermostat keeps λ at
temperature T like any atom. The simulation then samples the joint distribution
`p(x, λ) ∝ exp(−U(x, λ)/kT)`; the marginal `p(λ) ∝ exp(−G(λ)/kT)`, so the time spent near each end
state measures its free energy:

```
   ΔG(A→B) = −kT ln (P_B / P_A)
```

## Why a Lagrangian view helps

Lagrangian mechanics works for any coordinate, not only Cartesian positions, and new moving parts
can be added simply by adding their kinetic and potential terms to L. This is exactly what
λ-dynamics does.

## Practical issues (all handled in MSLD)
- λ must stay in [0, 1] and, with several states, sum to 1 → implicit constraints via θ
  ([[Implicit constraints and the softmax of sin theta]]).
- λ spends most time at intermediate values unless the landscape is shaped → biases and ALF
  ([[Biasing potentials in MSLD]], [[Adaptive landscape flattening]]).
- The λ force must be accurate every step → ∂U/∂λ for every term ([[REQ-020 Accurate dU-dlambda for every term|REQ-020]]).
- λ's mass sets its timescale; too light → fast oscillation, integration error, "hot" θ; too heavy
  → slow transitions ([[BLaDE units and theta mass]]).

## Sources
- Kong, X.; Brooks, C. L. III. "λ-dynamics: A new approach to free energy calculations."
  *J. Chem. Phys.* 105, 2414 (1996).
- Knight, J. L.; Brooks, C. L. III. "λ-Dynamics free energy simulation methods."
  *J. Comput. Chem.* 30, 1692 (2009).

