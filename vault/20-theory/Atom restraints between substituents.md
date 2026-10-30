---
title: Atom restraints between substituents
type: theory
status: reviewed
related: ["[[BLaDE atom restraints and soft bonds]]", "[[Hybrid and multiple topologies]]"]
updated: 2026-09-27
---
# Atom restraints between substituents

**In one sentence.** When several substituents at a site each carry their *own copy* of an atom
that is physically "the same place" (e.g. the backbone N of a proline and of an alanine variant),
harmonic restraints hold those copies together so the alternatives stay superimposed.

## Group definition — the key point

```
 restraint group g = { atom a in substituent 1, the equivalent atom in substituent 2, … }
                     (ONE atom per substituent; all at the same site)
 energy: U_g = ½ k Σ_{i∈g} | x_i − x̄_g |²,   x̄_g = mean position of the group
 identity: ½ k Σ_i |x_i − x̄|² = (k / 2N) Σ_{i<j} |x_i − x_j|²
```

It is **not** "all atoms of one substituent restrained to that substituent's own centroid" — that
would squeeze a side chain toward a point and fight its bonded terms. BLaDE's `msld restrain` code
comment literally says "NYI – checking for one atom per substituent", and its RNaseH inputs build
groups like `site{n}consN` = the N atoms of all substituents ([[BLaDE atom restraints and soft bonds]]).

## When they are used
- Backbone mutations (Gly/Pro) where each substituent carries its own backbone copy.
- Some ligand setups with duplicated core atoms.
- **Not** for plain side-chain mutations with a shared backbone (T4L, HSP90 examples use none).

## Parameters
k = 59.2 kcal/mol/Å² = 24 769 kJ/mol/nm² per atom (BLaDE default). The RNaseH input uses 118.4 =
59.2·n/(n−1) "to match CHARMM, because CHARMM is scaled by 59.2/(nsubs−1)". Restraints are not
λ-scaled.

## Our status
Our engine's math is right, but prep builds the wrong groups (per-block centroid) and turns them on
by default ([[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]], [[ADR-0033 Atom restraints group equivalent atoms|ADR-0033]]).

