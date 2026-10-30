---
title: Alchemical scaling rules in MSLD
type: theory
status: reviewed
related: ["[[Multisite lambda dynamics]]", "[[PME with lambda-scaled charges]]", "[[Bonded terms and dummy atoms in alchemy]]"]
updated: 2026-09-27
---
# Alchemical scaling rules in MSLD

**In one sentence.** Each energy term is multiplied by the λ's of the blocks its atoms belong to,
with one exception: atoms of different blocks at the same site never interact.

## Nonbonded pairs (direct space)

| atom i | atom j | factor | why |
|---|---|---|---|
| env | env | 1 | environment is always present |
| env | block b | λ_b | block present with weight λ_b |
| block b | block b | **λ_b** (not λ_b²) | both atoms appear and disappear *together*, so the pair is present with weight λ_b |
| block b (site s) | block c (site t ≠ s) | λ_b · λ_c | independent sites: joint weight |
| block b (site s) | block c (same site s) | **0** | mutually exclusive alternatives, overlap in space |

This is exactly BLaDE `nbdirect.cu:244-253` ([[BLaDE nonbonded direct space]]). It applies to LJ
and Coulomb alike.

## Bonded terms

A bonded term (2–4 atoms; CMAP 8 atoms) is multiplied by the **product of the distinct** block λ's
among its atoms. One block → λ_b; blocks at two different sites → λ_b λ_c. A term joining two
blocks of the same site is **illegal** (such a term cannot exist in a valid hybrid topology). Term
types can be excluded from scaling ("removescaling") — see [[Bonded terms and dummy atoms in alchemy]].

## Electrostatics in reciprocal space (PME)

Reciprocal space cannot scale individual pairs; it can only scale **charges**. With charges
q_i → λ_b(i) q_i, every pair gets λ_i λ_j — including within-block pairs (λ², not λ) and same-site
pairs (λ_b λ_c, not 0). How those two defects are corrected is a convention choice
([[PME with lambda-scaled charges]]).

## 1-4 pairs
Scale like other pairs; a 1-4 pair across two blocks of the same site is illegal.

## Restraints and biases
Atom restraints are **not** scaled ([[Atom restraints between substituents]]). Biases depend only
on λ ([[Biasing potentials in MSLD]]).

