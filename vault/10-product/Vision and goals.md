---
title: Vision and goals
type: product
status: active
updated: 2026-09-27
---
# Vision and goals

**Vision.** A trusted, open MSLD toolkit on OpenMM that takes a biomolecular system and a list of
chemical variants, prepares the hybrid system, runs λ-dynamics efficiently on GPUs, and reports
relative free energies with honest uncertainties — validated against BLaDE and conventional
methods.

## Goals

| ID | goal | measure of success |
|---|---|---|
| [[G-1 Free energies for many variants at once\|G-1]] | Relative free energies for many variants in one simulation | ΔΔG for a published MSLD benchmark reproduced within error |
| [[G-2 Physically correct MSLD\|G-2]] | Physically correct MSLD, equivalent to the reference implementation | per-term energies and dU/dλ match BLaDE at partial λ |
| [[G-3 Automated system preparation\|G-3]] | Automated, force-field-aware system preparation | a new system from standard inputs with no hand editing |
| [[G-4 Production performance\|G-4]] | Production performance | ns/day comparable to plain OpenMM MD on GPU, NPT |
| [[G-5 Meaningful analysis\|G-5]] | Meaningful analysis and chemical-space exploration | ΔG, ΔΔG, uncertainty, convergence report for every run |
| [[G-6 Traceable engineering process\|G-6]] | Traceable, maintainable engineering for humans and agents | every requirement traced to code, tests and decisions |

```
          G-1 free energies for many variants
           ▲            ▲             ▲
   G-2 correct     G-3 prep      G-5 analysis
           ▲
      G-4 performance               G-6 process (supports all)
```

The three subsystems of the architecture follow directly from G-1: prepare the system (G-3), run
MSLD (G-2, G-4), analyse the results (G-5). See [[ADR-0032 Three subsystems preparation simulation analysis|ADR-0032]] and [[Architecture overview]].

