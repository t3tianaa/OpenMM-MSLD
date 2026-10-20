---
title: Verification strategy
type: verification
status: active
updated: 2026-09-27
---
# Verification strategy

How we know the code is right, from cheapest to strongest:

```
 level 1  unit tests            one feature, toy systems, self-consistency (FD vs analytic)   ✓ 33 files
 level 2  invariants            master invariant λ=1 ≡ base; exclusion parity; iso-charge       ✓
 level 3  independent oracle    NumPy MSLD energy at random partial λ (NoCutoff)                ✗ FEAT-045
 level 4  reference engine      BLaDE per-term energies/dU/dλ at partial λ; λ statistics         ✗ FEAT-030
 level 5  physics               θ samples Boltzmann (toy ✓ EXP-001); T_θ = T in real systems ✗
 level 6  science               published ΔΔG reproduced (T4L, HSP90); Amber vs FEP/TI           ✗ FEAT-041
```

Rules:
- A requirement is `verified` only at level ≥ 3 for physics requirements ([[Conventions]]).
- Measurements go in `EXP` notes with setup, numbers, uncertainty and a reproduce command.
- Statistics: never judge θ/λ behaviour on one short run; use independent replicas from a shared
  start ([[EXP-001 Theta samples the exact Boltzmann distribution on a toy|EXP-001]] lesson, [[EXP-006 MDM2 theta-parameter sweep|EXP-006]] lesson).
- Precision: validate in double (Reference) first; fp32 results need a tolerance argument.

See [[Test catalog]] for what each test file checks and [[Requirements index]] for coverage.

