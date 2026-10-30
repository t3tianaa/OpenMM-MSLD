---
title: CHARMM BLOCK and MSLD
type: reference
status: draft
system: charmm
version: not pinned
related: ["[[BLaDE overview]]"]
updated: 2026-09-27
---
# CHARMM BLOCK and MSLD (stub)

CHARMM's `BLOCK` module is the original MSLD implementation; BLaDE mirrors its keywords:
`Call` (assign selection to block), `LDIN` (initial θ, velocity, mass, fixed bias), `RMLA`
(= removescaling), `MSLD` (fnex), `SOFT` (soft-core), `PMEL` (PME λ treatment: on/ex/nn ⇔
BLaDE `ewaldtype` 1/2/3), `LDBI`/`LDBV` (variable biases), `CATS` (atom restraints), `SOBO`
(soft bonds), `FFIX` (fixed λ). Source: comments in BLaDE `msld.cu` and `doc/MAIN.txt`.

Not studied further; BLaDE is the reference we compare against.

