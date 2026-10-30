---
title: Assembly component
type: component
subsystem: "[[Preparation subsystem]]"
layer: L2
status: as-built
code: [msld/prep/assemble/]
requirements: ["[[REQ-044 Multiple sites per system|REQ-044]]", "[[REQ-045 Place variant coordinates in the shared frame|REQ-045]]", "[[REQ-046 Consistent charges across variants|REQ-046]]", "[[REQ-047 Solvate and neutralize consistently|REQ-047]]", "[[REQ-048 No bonded term between same-site blocks|REQ-048]]", "[[REQ-049 Prep hands off a plain System and a model|REQ-049]]", "[[REQ-050 Inspectable prep artifacts|REQ-050]]"]
decisions: ["[[ADR-0016 Prep emits a plain System|ADR-0016]]", "[[ADR-0017 Staged prep pipeline|ADR-0017]]", "[[ADR-0021 Charge averaging, renormalization, iso-charge guard|ADR-0021]]", "[[ADR-0022 Solvation by overlay after grafting|ADR-0022]]"]
updated: 2026-09-27
---
# Assembly component

## Purpose
Build the real hybrid system from the env structure, the variant structures and the per-site
mappings, and hand it to the engine.

## Interfaces
```python
HybridSystemAssembler(mapper=…, aligner=…, renormalizer=…, system_builder=…)
    .assemble(env_structure, [SiteSpec…], renormalize=True, solvate=False, solvate_kwargs=None)
    -> HybridSystemBundle
```

## Sub-steps (each its own note)

```
 2.1 graft      [[Grafting and term transplant]] + [[Coordinate alignment]]
 2.2 charges    [[Charge renormalization]]
 2.3 solvate    [[Solvation]]                     (optional; pre-solvated input is stripped first)
 2.4 system     [[Plain System builder]]
 save           [[Hybrid inspection artifacts]]
```

Output: [[HybridSystemBundle]] = {structure, system, mapping (HybridBlueprint with global indices,
recomputed for the solvated atom count), reports}.

## Why this order
Grafting works on a dry solute (templates and alignment are simpler), charges must be final before
the System is built, and solvation after grafting keeps solute indices stable so the mapping stays
valid ([[ADR-0022 Solvation by overlay after grafting|ADR-0022]]).

## As-built status
`test_hybrid_builder` (the gate: WT block fully on reproduces the original peptide energy to
3e-15), `test_hybrid_system`, `test_renorm`, `test_prep_charges`, `test_prep_solvate`,
`test_prep_cross_variant`, `test_hybrid_output`.

