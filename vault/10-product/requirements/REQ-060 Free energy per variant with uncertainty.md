---
id: REQ-060
type: requirement
title: Free energy per variant with uncertainty
area: analysis
priority: must
status: partial
derives_from: ["[[G-5 Meaningful analysis|G-5]]"]
satisfied_by: ["[[FEAT-040 Free-energy analysis subsystem|FEAT-040]]"]
decisions: ["[[ADR-0034 Adopt published ALF and two-leg ddG|ADR-0034]]"]
created: 2026-09-16
updated: 2026-09-27
retrospective: true
---
# REQ-060 — Free energy per variant with uncertainty

**Statement.** From λ trajectories (and the applied biases), estimate the relative free energy of
every variant / combination with a statistical uncertainty, using the standard estimator
`G = −kT ln P(λ > λ_c) − U_bias` or a reweighting estimator (WHAM/MBAR)
([[Free energies from lambda populations]], [[Free energy estimators]]).

Status: only a converged-bias readout exists (`alf.estimate_ddg`), and its uncertainty is the
spread of the bias history ([[ISS-011 ALF is a heuristic and ddG is single-leg|ISS-011]]).

