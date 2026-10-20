---
title: BLaDE cross-validation harness
type: component
status: planned
layer: L2
requirements: ["[[REQ-070 Agree with BLaDE on a shared CHARMM system|REQ-070]]", "[[REQ-052 Import a BLaDE or CHARMM MSLD setup|REQ-052]]"]
decisions: ["[[ADR-0002 BLaDE is the reference and validation oracle|ADR-0002]]", "[[ADR-0036 Same-site reciprocal-space convention|ADR-0036]]"]
updated: 2026-09-27
---
# BLaDE cross-validation harness (planned, [[FEAT-030 BLaDE cross-validation harness|FEAT-030]])

```
 CHARMM system (psf + prm + crd) + MSLD spec (selections, sites, biases, flags)
        │                                  │
        ▼                                  ▼
 BLaDE: run energy / run test alchemical   our engine: import spec → MSLDModel ([[REQ-052 Import a BLaDE or CHARMM MSLD setup|REQ-052]])
   (CUDA machine, AKMA or NMPS build)        scale_msld_system on the CharmmPsfFile System
        │                                  │
        └──────────── compare at λ grid ───┘
   per term: bonded, UB, impropers, CMAP, direct elec, direct vdW, recip, self, exclusions, 1-4,
             biases, restraints — energy and every ∂U/∂λ_b
```

Plan:
1. System: `T4L_peptide` (1 site × 6) or a smaller dipeptide; then HSP90 (2 sites) for cross-site
   terms.
2. Settings aligned: same cutoffs, PME grid/α, **vfswitch** in OpenMM ([[TASK-070 CHARMM force switching for the cross-check|TASK-070]]), soft-core off
   first, then on; same-site PME convention accounted for ([[ADR-0036 Same-site reciprocal-space convention|ADR-0036]]).
3. λ grid: all-ones (master), each end state, λ = 0.5 pairs, random interior points.
4. Tolerances: 1e-5 relative in double precision per term (Reference vs BLaDE double build), looser
   for fp32 builds.
5. Then dynamics: λ histograms and ⟨∂U/∂λ⟩ from matched short runs.

Needs a CUDA machine for BLaDE ([[TASK-042 Get BLaDE running with reference data|TASK-042]]).

