---
title: Solvation
type: component
subsystem: "[[Preparation subsystem]]"
layer: L3
status: as-built
code: [msld/prep/assemble/solvate.py]
requirements: ["[[REQ-047 Solvate and neutralize consistently|REQ-047]]"]
decisions: ["[[ADR-0022 Solvation by overlay after grafting|ADR-0022]]"]
updated: 2026-09-27
---
# Solvation

`solvate(solute, padding=1.0 nm, water_model=…, …)`:

```
 1. build a pure, pre-equilibrated water box with OpenMM (empty solute → no template needed)
 2. overlay it on the solute; delete waters within `clash` of any solute atom (scipy cKDTree)
 3. neutralize: turn the waters FARTHEST from the solute into counter-ions
 4. combined = solute + solvent (solute first → solute indices unchanged)
```

Why not `Modeller.addSolvent`: it needs a template for every solute residue, and the hybrid
residue has none ([[ADR-0022 Solvation by overlay after grafting|ADR-0022]]).

The water model must match the solute force field (ff14SB → TIP3P; ff19SB → OPC; CHARMM36 →
CHARMM TIP3P with its LJ recovered by `recover_charmm_lj`, keeping ion–water NBFIX). A wrong pair is
not detected (**gap**). OPC is a 4-site model → needs virtual-site support in the integrator
([[ISS-017 Zero-mass particles break the integrator|ISS-017]]).

