---
title: BLaDE bonded term scaling
type: reference
status: verified
system: blade
version: c677277
related: ["[[Bonded terms and dummy atoms in alchemy]]", "[[Bonded scaling module]]"]
updated: 2026-09-27
---
# BLaDE bonded term scaling

Source: `Msld::bonded_scaling` (`msld.cu:509-555`) and wrappers (`msld.cu:585-613`); called when
the potential is built (`src/system/potential.cxx:567, 784`); kernels in `src/bonded/bonded.cu`.

## Algorithm (per bonded term, at setup)

```
 Nsc = 2 for bond/urey/angle/dihe/impr, 3 for cmap
 collect the DISTINCT blocks of the term's atoms (descending), with this twist:
   if the term TYPE is not scaled (removescaling) and the term is not a soft bond:
       an atom's block is treated as 0 (environment) if ANY atom of the same block in this
       term is NOT a restrained atom            (check_restrained)
 error if two distinct blocks belong to the same site           (fatal)
 error if more than Nsc distinct blocks                         (fatal)
 store siteBlock[] → the kernel multiplies the term by the product of those λ's
```

So:
- scaled types: term × Π λ of its distinct non-env blocks (≤ 2, CMAP ≤ 3);
- unscaled types: term at full strength — **except** terms whose same-block atoms are *all*
  restrained atoms: those stay scaled (duplicated backbone atoms, see
  [[BLaDE atom restraints and soft bonds]]);
- soft bonds (`msld softbond`) are always scaled (and softened).

Kernel side (`bonded.cu:114-121` for bonds): `U = λ_b0 λ_b1 U_term`, `∂U/∂λ_b0 = λ_b1 U_term`, etc.

1-4 pairs: `nb14_scaling` (`msld.cu:615-621`) uses the nonbonded rule and is **fatal** for two
different blocks at the same site.

Our engine: same product rule and same-site error; removescaling via `model.scale_*` flags (fewer
types); no restrained-atom exception ([[ISS-023 Restrained-atom bonded scaling rule missing|ISS-023]]); CMAP refused ([[ISS-015 Cross-site 1-4 and CMAP are refused|ISS-015]]).

