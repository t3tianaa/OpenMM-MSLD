---
title: BLaDE atom restraints and soft bonds
type: reference
status: verified
system: blade
version: c677277
related: ["[[REQ-014 Atom restraints between substituents]]", "[[Atom restraint module]]"]
updated: 2026-09-27
---
# BLaDE atom restraints and soft bonds

## Commands (`msld.cu:383-443`)
- `msld restrain <selection>` and `msld atomrestraint <selection>` both push **one group = the
  atoms of that selection** onto `atomRestraints`. The `restrain` branch carries the comment
  `// NYI - checking for one atom per substituent`: the intended group is one equivalent atom per
  substituent. `msld restrain reset` clears all groups.
- (`msld rest <sel>` is an older per-atom flag array `rest[]`, separate from the groups.)
- `msld parameter krestraint <kcal/mol/Å²>` (default 59.2).

## Force (`getforce_atomRestraints_kernel`, `msld.cu:1328-1389`)

```
 for each group: centre = unweighted mean position (PBC-aware, relative to the first atom)
 for each atom i in group: U += ½ k |x_i − centre|²,   F_i = −k (x_i − centre)
```
Not λ-scaled; energy reported as `eecats` (the CHARMM name is `CATS`).

## Example use (`test/RNaseH/prep/ec2acc.inp:150-160, 228`)

```
 msld restrain site{site}consN     ! N atoms of all substituents at this site
 msld restrain site{site}consCA
 msld restrain site{site}consHA
 msld restrain site{site}consC
 msld restrain site{site}consO
 msld parameter krestraint 118.4   ! 59.2*nsubs/(nsubs-1) "to match charmm"
```
Used when each substituent carries its own copy of the backbone (backbone mutations such as
Pro/Gly). The T4L and HSP90 examples use **no** restraints.

## Interaction with bonded scaling
Terms whose same-block atoms are all restrained stay λ-scaled even under `removescaling`
([[BLaDE bonded term scaling]]).

## Soft bonds (`msld softbond <2-atom selection>`, `msld.cu:404-428`)
A bond marked soft (e.g. Pro CB–CG ring closure in RNaseH inputs) is always λ-scaled and uses
`softbondradius`, `softbondexponent`, `softnotbondexponent`. Needed to open/close the proline ring
alchemically. Not implemented in our engine.

