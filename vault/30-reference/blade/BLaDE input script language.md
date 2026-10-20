---
title: BLaDE input script language
type: reference
status: verified
system: blade
version: c677277
related: ["[[BLaDE overview]]", "[[BLaDE T4L and HSP90 examples]]"]
updated: 2026-09-27
---
# BLaDE input script language

Source: `doc/MAIN.txt`; parser `src/msld/msld.cu:152-468` for the `msld` class. **Verified.**

A line = `class keyword args…`; `!` starts a comment; case sensitive. Classes in dependency order:

```
variables set dir ../test/T4L_peptide            ! variables, {name} substitution, if/while
parameters file {dir}/../toppar/par_all36_prot.prm
structure file psf {dir}/T4L_prep/minimized.psf  ! PSF built by CHARMM (BLaDE cannot build)
structure shake hbond
selection define site1sub2 and selection site1 atomnames CBA HB1A HB2A HB3A   ! prefix operators
msld nblocks 6                                   ! must come first in the msld class
msld call 1 site1sub1                            ! assign selection → block
msld initialize 1 1 1.5 0.0 5.0 0.0 0.0          ! block site θ θvel θmass fixedbias charge
msld removescaling bond angle                    ! do not λ-scale these bonded types
msld softcore on / msld softcore14 off
msld bias 1 2 6 0.0 {c12} 0                      ! i j type l0 k n
msld gamma 1.0                                   ! θ friction, ps⁻¹
msld fnex 5.5
msld restrain <sel> / msld atomrestraint <sel>   ! one restraint group per selection
msld softbond <sel of 2 atoms>
msld fix on                                      ! FEP: θ in initialize is the fixed λ
msld ewaldtype 1|2|3                             ! PME exclusion convention (default 2)
msld thetabias collective|independent nsites|set|auto …
coordinates file crd …; coordinates box X 0 0 0 Y 0 0 0 Z; coordinates velocity 300
run setvariable dt 0.002 / T / gamma (atoms) / nsteps / rcut / rswitch / invbetaewald /
               orderewald / gridspace / freqnpt / pressure / fnmlmd / freqlmd / fnmcpi / fnmcpo …
run dynamics | run energy | run minimize
```

Notes:
- `msld gamma` is the **θ** friction; `run setvariable gamma` is the **atom** friction.
- Only PME electrostatics and **vfswitch** vdW are supported; orthogonal boxes only.
- The λ trajectory (`fnmlmd`, every `freqlmd` steps) is the main scientific output.
- BLaDE cannot generate topologies: CHARMM prepares the hybrid PSF (patches graft each substituent,
  bonded terms between substituents are deleted) — see [[BLaDE T4L and HSP90 examples]].

