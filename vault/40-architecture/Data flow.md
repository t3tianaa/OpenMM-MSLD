---
title: Data flow
type: architecture
status: as-built
updated: 2026-09-27
---
# Data flow

```
 FILES                     PREPARATION                                              SIMULATION
 ─────                     ───────────                                              ──────────
 env: pdb/prmtop/psf ──▶ ingest ──▶ pmd.Structure (env)
 variants: pdb/sdf   ──▶ ingest ──▶ pmd.Structure (per variant) ─┐
                                                                  ▼
                          mapping: Mapper.get_mapping(ref, variants) → CoreMapping (residue-local)
                                                                  ▼
                          assembly: graft (align + append + transplant) → hybrid Structure
                                    + HybridBlueprint (global indices, one CoreMapping per site)
                                  → charges: average env, renormalize blocks, iso-charge guard
                                  → solvate (optional): overlay water, ions (solute indices kept)
                                  → HybridSystemBuilder: Structure.createSystem → plain System
                                                                  ▼
                          HybridSystemBundle {structure, system, mapping}  ── save() → artifacts
                                                                  │
                      bundle.to_model() → MSLDModel ──────────────┤
                                                                  ▼
                          scale_msld_system(system, model): rewrite forces, λ globals, groups
                                                                  ▼
                          Context(system, integrator, platform) + LambdaDynamics(model)
                                  loop: θ → λ (softmax) → set λ globals → forces + dU/dλ
                                        → dU/dθ (chain rule) → VRORV step (atoms + θ)
                                                                  ▼
                          reporters: λ/energy CSV, DCD (+PDB)       ALF: re-tune bias globals
                                                                  ▼
                                                   ANALYSIS (planned): G per variant, ΔΔG, diagnostics
```

Units at boundaries: ParmEd Å / kcal/mol inside prep; OpenMM nm / kJ/mol / ps from the System on.
Index spaces: residue-local (mapper) → global hybrid (assembler) → same indices in System and
MSLDModel; solvation appends after the solute so solute indices never change.

