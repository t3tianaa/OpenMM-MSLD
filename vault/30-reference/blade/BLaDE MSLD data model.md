---
title: BLaDE MSLD data model
type: reference
status: verified
system: blade
version: c677277
related: ["[[MSLD model component]]", "[[BLaDE overview]]"]
updated: 2026-09-27
---
# BLaDE MSLD data model

Source: `src/msld/msld.h`, `Msld::Msld()` (`msld.cu:19-100`), `Msld::initialize` (`msld.cu:681-795`).

```cpp
class Msld {
  int blockCount;          // incl. block 0 = environment
  int *atomBlock;          // atom → block
  int *lambdaSite;         // block → site (site 0 = env)
  real *lambdaBias;        // fixed linear bias per block
  real_x *theta; real_v *thetaVelocity; real *thetaMass; real *thetaFriction;
  real *lambdaCharge;      // net charge per block (computed in initialize)
  int siteCount, *blocksPerSite, *siteBound;   // contiguous block ranges per site
  real gamma = 1 ps⁻¹;  real fnex = 5.5;
  bool scaleTerms[6];      // bond, urey, angle, dihe, impr, cmap (default all true)
  VariableBias *variableBias;   // {i, j, type, l0, k, n}
  θ-bias arrays (collective k, n; independent k);  soft bonds;  atomRestraints (vector of groups)
  bool useSoftCore=false, useSoftCore14=false;  int msldEwaldType=2;
  real kRestraint = 59.2 kcal/mol/Å²;  charge-restraint constants;  soft-bond parameters
  bool fix;  bool *blockFixed;   // FEP mode / per-block fixed
  // alternative "piecewise" implicit constraint (new_implicit, theta0, well_width, …)
};
```

`initialize` checks (same as our `MSLDModel.finalize`): blocks ordered by consecutive sites; site 0
has exactly one block; each site ≥ 2 blocks unless a single fixed block. It also computes
`lambdaCharge[b] = Σ q` over the block's atoms, and sets θ mass and velocity to 0 for fixed blocks
(the integrator skips DOFs whose `1/√m` is not finite).

Defaults worth copying: `fnex = 5.5`, θ friction 1 ps⁻¹, θ mass given per block in `initialize`
(examples use 5), `kRestraint = 59.2 kcal/mol/Å²`, soft-core off (but examples turn it on),
`msldEwaldType = 2`, all bonded types scaled (examples remove most).

