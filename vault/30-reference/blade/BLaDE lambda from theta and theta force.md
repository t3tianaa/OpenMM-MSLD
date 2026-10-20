---
title: BLaDE lambda from theta and theta force
type: reference
status: verified
system: blade
version: c677277
related: ["[[Implicit constraints and the softmax of sin theta]]", "[[Theta force by the chain rule]]", "[[BLaDE units and theta mass]]"]
updated: 2026-09-27
---
# BLaDE: λ from θ and the θ force

## λ from θ — `calc_lambda_from_theta_kernel` (`msld.cu:863-906`)

```cpp
for each site i:                         // one GPU thread per site
  fixsum = Σ_{fixed j} theta[j]           // for a fixed block, "theta" holds its λ
  for non-fixed j: w_j = exp(fnex * sin(theta[j]*ANGSTROM)); norm += w_j
  Rfrac = 1 - fixsum
  lambda[j] = fixed ? theta[j] : w_j * Rfrac / norm
```

Called after every integration step (`update.cu:303`), so each step's forces use the new λ.
With `msld fix on` the kernels are skipped and λ is copied from θ directly (`msld.cu:910-935`).

## θ force — `calc_thetaForce_from_lambdaForce_kernel` (`msld.cu:937-985`)

```cpp
if (blockFixed[i]) return;
dynamic_sum = Σ_{non-fixed j in site} lambda[j]*lambdaForce[j]
fi = lambdaForce[i] - dynamic_sum/Rfrac
fi *= lambda[i] * fnex * cos(ANGSTROM*theta[i]) * ANGSTROM
thetaForce[i] += fi
```

Same chain rule as [[Theta force by the chain rule]], with fixed blocks removed and the
`ANGSTROM` factor (the derivative of `sin(ANGSTROM·θ)`). `lambdaForce` = +∂U/∂λ accumulated by all
force kernels (BLaDE stores forces as **+**∂U/∂x).

## The `ANGSTROM` factor
`ANGSTROM` = 1 in the CHARMM-unit (AKMA) build and 0.1 in the GROMACS-unit (NMPS) build
(`defines.h:47,73`). So the "angle" used in `sin` is θ in AKMA but 0.1·θ in NMPS. This changes the
meaning of the θ mass between builds — see [[BLaDE units and theta mass]].

## Differences from our engine
- Our fixed blocks keep θ frozen but λ still comes from the softmax ([[ISS-019 Fixed-block lambda semantics differ from BLaDE|ISS-019]]).
- We use radians directly (no ANGSTROM factor).
- BLaDE also has a "piecewise" implicit constraint (Newton solve, `msld.cu:797-861`); we do not.

