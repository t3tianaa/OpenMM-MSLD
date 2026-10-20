---
title: Free energy estimation component
type: component
subsystem: "[[Analysis subsystem]]"
layer: L2
status: planned
requirements: ["[[REQ-060 Free energy per variant with uncertainty|REQ-060]]", "[[REQ-061 Relative ddG from two legs|REQ-061]]", "[[REQ-063 Combinatorial multi-site free energies|REQ-063]]"]
decisions: ["[[ADR-0034 Adopt published ALF and two-leg ddG|ADR-0034]]"]
updated: 2026-09-27
---
# Free energy estimation component (planned)

- End-state estimator: `G(l) = −kT ln P(all sites of l above λ_c) − U_bias(l)` with block-bootstrap
  errors ([[Free energies from lambda populations]]).
- Reweighting estimator pooling runs with different biases (WHAM/MBAR in λ-space) — the ALF
  production approach ([[Free energy estimators]]).
- Two-leg cycle → ΔΔG with propagated uncertainty ([[Thermodynamic cycles for relative free energies]]).
- Multi-site: joint end states for all combinations; rarely visited ones via reweighting.
Decision on estimator and whether to reuse ALF's analysis code: [[ADR-0034 Adopt published ALF and two-leg ddG|ADR-0034]].

