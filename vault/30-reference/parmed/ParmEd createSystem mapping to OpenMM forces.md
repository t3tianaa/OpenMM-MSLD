---
title: ParmEd createSystem mapping to OpenMM forces
type: reference
status: verified
system: parmed
version: 4.3.1
related: ["[[Force field functional forms]]", "[[Plain System builder]]"]
updated: 2026-09-27
---
# ParmEd `createSystem` → OpenMM forces

| ParmEd terms | OpenMM force |
|---|---|
| bonds | `HarmonicBondForce` |
| urey_bradleys | a second `HarmonicBondForce` |
| angles | `HarmonicAngleForce` |
| dihedrals (periodic, incl. Amber impropers) | `PeriodicTorsionForce` |
| impropers (CHARMM harmonic) | `CustomTorsionForce` |
| cmaps | `CMAPTorsionForce` |
| charges + LJ (no NBFIX) | `NonbondedForce` (LB) |
| LJ with NBFIX | tabulated `CustomNonbondedForce` (a/b √-form, see [[ParmEd round trips and NBFIX loss]]) + ε = 0 in `NonbondedForce` |
| adjusts (1-4) | `NonbondedForce` exceptions (and CHARMM 1-4 LJ via exceptions) |

Our `prep/assemble/system.py:HybridSystemBuilder.build` calls `structure.createSystem`, choosing PME
when a box exists, else NoCutoff ([[Plain System builder]]). The engine then dispatches on these
force classes ([[Force scaling component]]).

