---
title: ParmEd round trips and NBFIX loss
type: reference
status: verified
system: parmed
version: 4.3.1
related: ["[[Lennard-Jones, combining rules and NBFIX]]", "[[Ingest component]]", "[[ADR-0018 Two ingest modes and NBFIX recovery|ADR-0018]]"]
updated: 2026-09-27
---
# ParmEd ⇄ OpenMM round trips and NBFIX loss

```
 ParmEd ──createSystem──▶ OpenMM       LOSSLESS: LJ (incl. NBFIX) rebuilt from atom types
 OpenMM ──load_topology──▶ ParmEd      LOSSY for CHARMM: the tabulated-LJ CustomNonbondedForce is
                                       dropped with "Unsupported Force type" (topsystem.py:203)
```

So a CHARMM system created by OpenMM's `ForceField` (Mode A ingest) or a CHARMM water box loses
its LJ when converted to ParmEd. Our `prep/ingest/recover.py:recover_charmm_lj` rebuilds per-type
LJ from the table diagonal and adds NBFIX where the off-diagonal deviates from Lorentz–Berthelot.

## Two table conventions — a trap (Verified 2026-09-27)

| producer | energy expression | table content |
|---|---|---|
| OpenMM `app.ForceField` (`forcefield.py:2942-2960`) | `acoef/r^12 − bcoef/r^6` | A = 4εσ¹², B = 4εσ⁶ |
| ParmEd `Structure.createSystem` (`structure.py:2913-2934`) | `(a/r6)^2 − b/r6` | a = √ε·Rmin⁶ (= √A), b = 2ε·Rmin⁶ |

`recover_charmm_lj` assumes the **OpenMM** convention (A/B). It is correct where it is used today
(after OpenMM ForceField), but would silently produce wrong LJ if ever called on a ParmEd-built
System ([[ISS-025 NBFIX recovery assumes the OpenMM table convention|ISS-025]]). The engine's `add_scaled_charmm_lj` copies whatever expression it finds, so it
is safe with both.

