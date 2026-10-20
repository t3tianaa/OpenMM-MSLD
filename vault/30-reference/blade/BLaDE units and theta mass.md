---
title: BLaDE units and theta mass
type: reference
status: draft
system: blade
version: c677277
related: ["[[BLaDE lambda from theta and theta force]]", "[[Langevin dynamics and BAOAB splitting]]", "[[ISS-002 Theta mass convention differs from BLaDE|ISS-002]]"]
updated: 2026-09-27
---
# BLaDE units and θ mass — an **open question**

BLaDE compiles in one of two unit systems (`src/main/defines.h:37-88`):

| build | define | length | energy | time | `ANGSTROM` | `SOFTCORERADIUS` |
|---|---|---|---|---|---|---|
| AKMA (CHARMM units) | `CHARMM_UNITS` | Å | kcal/mol | AKMA ≈ 48.9 fs | 1.0 | 4.0 |
| NMPS (GROMACS units) | — | nm | kJ/mol | ps | 0.1 | 0.4 |

Which one is "the default" depends on how BLaDE is built: `src/CMakeLists.txt:12` defaults
`UNITS` to **NMPS**, but the `CompileOptions.sh` helper defaults to **AKMA** (`--gromacs` switches
to NMPS). Inside CHARMM, BLaDE always uses CHARMM units.

## Why it matters
θ enters λ as `sin(ANGSTROM·θ)`, and θ is integrated with mass `thetaMass` (amu) in the build's
units. The same input number therefore means different dynamics:

```
 AKMA:  angle φ = θ,       KE = ½ m θ̇² [kcal/mol, θ̇ per AKMA time]
        → in OpenMM units (kJ/mol, ps, rad): m_eff ≈ m · 4.184 · (0.04889)² ≈ 0.0100 · m
 NMPS:  angle φ = 0.1·θ,   KE = ½ m θ̇² [kJ/mol, θ̇ per ps]
        → m_eff = m / 0.1² = 100 · m
 ours:  angle φ = θ (rad), KE = ½ m θ̇² [kJ/mol, ps]  → m_eff = m
```

With the usual input m = 5, the effective θ mass is ≈ 0.05 (AKMA) or 500 (NMPS) in our units — a
factor 10⁴ apart. **Inferred** from the source; not yet checked by running BLaDE. The audit
([[AUD-001 Engine audit of the local working copy|AUD-001]], F2) assumed the NMPS build and concluded our θ (mass 10) is ~50× too light. If BLaDE
is normally run in AKMA units, the opposite conclusion follows.

## What to do
Resolve before changing defaults or drawing conclusions about "hot θ" ([[TASK-032 Resolve BLaDE theta units|TASK-032]]):
1. check which build the BLaDE authors use for published runs (CHARMM-integrated = AKMA);
2. run the same toy site in both builds and compare θ oscillation periods;
3. then choose our default θ mass so our dynamics match the reference build ([[ADR-0038 Theta units and default theta mass|ADR-0038]]).

Note: CHARMM λ-dynamics masses are usually quoted in amu·Å² — consistent with the AKMA reading.

