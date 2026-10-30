---
title: Bonded scaling module
type: component
subsystem: "[[Simulation subsystem]]"
layer: L3
status: as-built
code: [msld/forces.py]
requirements: ["[[REQ-003 Scale bonded terms by block lambdas|REQ-003]]", "[[REQ-004 Configurable bonded scaling per term type|REQ-004]]"]
decisions: ["[[ADR-0006 Bonded scaling via grouped custom forces|ADR-0006]]", "[[ADR-0014 Bonded scaling on by default|ADR-0014]]", "[[ADR-0041 Default bonded scaling follows BLaDE practice|ADR-0041]]"]
issues: ["[[ISS-014 Bonded scaling defaults differ from BLaDE|ISS-014]]", "[[ISS-023 Restrained-atom bonded scaling rule missing|ISS-023]]"]
updated: 2026-09-27
---
# Bonded scaling module

Functions: `add_scaled_bonds` (`HarmonicBondForce`, incl. CHARMM Urey–Bradley which is a 2nd
`HarmonicBondForce`), `add_scaled_angles`, `add_scaled_torsions` (`PeriodicTorsionForce`, incl.
Amber impropers), `add_scaled_impropers` (CHARMM harmonic `CustomTorsionForce`: reads its energy
expression and re-adds terms grouped by signature).

```
 for each term:  sig = model.classify_bonded(atoms)          [] → leave in base force
                                                             [b] or [b, c] → move
 group terms by signature → ONE Custom*Force per signature, expression "lambda_b[*lambda_c]*<base form>"
 zero the constant of the moved term in the base force (keeps indices)
 _register_lambdas(force, sig): addGlobalParameter + addEnergyParameterDerivative
```

Why group by signature: the λ prefactor is a constant expression per force, so OpenMM's
`addEnergyParameterDerivative` gives exact analytic dU/dλ ([[ADR-0006 Bonded scaling via grouped custom forces|ADR-0006]]).

Worked example from the original notes (6 atoms, 2 sites × 2 blocks):
![[Pasted image 20260731125937.png|300]]
![[Pasted image 20260731130031.png|380]]
![[Pasted image 20260731130103.png|450]]
![[Pasted image 20260731130312.png|600]]
![[Pasted image 20260731130422.png|500]]
![[Pasted image 20260731130538.png|400]]

Gaps: switches are coarser than BLaDE's (bond/angle/torsion; UB follows bonds? impropers follow
torsions) ([[REQ-004 Configurable bonded scaling per term type|REQ-004]]); no restrained-atom exception ([[ISS-023 Restrained-atom bonded scaling rule missing|ISS-023]]); default "scale everything"
differs from BLaDE practice ([[ISS-014 Bonded scaling defaults differ from BLaDE|ISS-014]], [[ADR-0041 Default bonded scaling follows BLaDE practice|ADR-0041]]); CMAP refused ([[ISS-015 Cross-site 1-4 and CMAP are refused|ISS-015]]).

