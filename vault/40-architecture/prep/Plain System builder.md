---
title: Plain System builder
type: component
subsystem: "[[Preparation subsystem]]"
layer: L3
status: as-built
code: [msld/prep/assemble/system.py]
requirements: ["[[REQ-049 Prep hands off a plain System and a model|REQ-049]]", "[[REQ-048 No bonded term between same-site blocks|REQ-048]]"]
decisions: ["[[ADR-0016 Prep emits a plain System|ADR-0016]]"]
updated: 2026-09-27
---
# Plain System builder

`HybridSystemBuilder.build(structure, blueprint)`: runs the cross-variant guard, then
`structure.createSystem(nonbondedMethod = PME if boxed else NoCutoff, …)`. ParmEd-native →
lossless, NBFIX rebuilt from types ([[ParmEd createSystem mapping to OpenMM forces]]).

Deliberately **no** same-site exclusions and no λ changes: the System stays a faithful parameter
container so the master invariant is testable ([[ADR-0016 Prep emits a plain System|ADR-0016]]). `is_solvated` / `strip_solvent`
support the "assemble dry, solvate after" policy.

Open: cutoff, switching distance, dispersion correction and constraints come from ParmEd defaults
unless passed; they should be explicit, recorded settings ([[REQ-031 Reproducible runs|REQ-031]]).

