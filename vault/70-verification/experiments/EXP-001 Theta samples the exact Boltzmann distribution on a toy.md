---
id: EXP-001
type: experiment
title: Theta samples the exact Boltzmann distribution on a toy
status: done
date: 2026-09-26
requirements: ["[[REQ-016 Canonical sampling of atoms and theta|REQ-016]]"]
issues: ["[[ISS-018 Theta runs hot in MDM2|ISS-018]]"]
related: ["[[AUD-001 Engine audit of the local working copy|AUD-001]]"]
---
# EXP-001 — θ samples the exact Boltzmann distribution on a toy site (audit E1)

**Question.** Does `LambdaDynamics` (VRORV + softmax chain rule) sample the right θ/λ distribution?

**Setup.** Two-block site, only a linear bias c·λ₁, θ mass 2, friction 2 ps⁻¹, dt 1 fs, 32 replicas ×
300 k steps from random θ, Reference. Exact reference: Boltzmann average over the (θ₁, θ₂) torus.
Scripts were in the audit's scratchpad (not in the repo).

| c (kJ/mol) | ⟨λ₁⟩ sim | ⟨λ₁⟩ exact | P(λ₁>0.99) sim | exact | T_θ |
|---|---|---|---|---|---|
| 0 | 0.508 ± 0.006 | 0.500 | 0.223 ± 0.006 | 0.222 | 300 ± 2 K |
| 5 | 0.209 ± 0.006 | 0.202 | 0.062 ± 0.005 | 0.059 | 300 ± 2 K |
| 10 | 0.084 ± 0.003 | 0.079 | 0.015 ± 0.003 | 0.010 | 300 ± 2 K |

**Conclusion.** Agreement within 1–2 σ; θ exactly at 300 K on both FD and analytic paths → the
integrator and chain rule are correct; hot θ in MDM2 is a parameter/stiffness/noise problem. A
first attempt with single short runs looked badly biased — non-convergence, not a bug.

