---
title: Free energy estimators
type: theory
status: draft
related: ["[[Free energies from lambda populations]]", "[[REQ-030 Adaptive landscape flattening]]"]
updated: 2026-09-27
---
# Free energy estimators

| estimator | input | notes |
|---|---|---|
| counting (histogram) | fraction of frames in each end state | simple; needs many transitions |
| exponential averaging (Zwanzig) | ΔU samples | biased for large ΔU |
| TI | ⟨∂U/∂λ⟩ at fixed λ | needs quadrature over windows |
| BAR / MBAR | energies of samples evaluated in all states | minimum-variance; MBAR generalizes BAR (Shirts & Chodera 2008) |
| WHAM | histograms from several biased runs | the classic way to combine biased λ runs; used for ALF production analysis (to verify, [[TASK-074 Study the ALF package\|TASK-074]]) |

For MSLD, samples from several runs with different biases (ALF iterations, replicas) can be pooled
by reweighting in λ space, because the bias is a known function of λ. Uncertainty: bootstrap over
independent replicas or blocks of time; never over correlated frames as if independent.

Sources: Shirts, M. R.; Chodera, J. D. *J. Chem. Phys.* 129, 124105 (2008). Kumar, S. et al.
*J. Comput. Chem.* 13, 1011 (1992) (WHAM).

