---
title: Net charge changes in alchemical calculations
type: theory
status: reviewed
related: ["[[BLaDE charge restraints]]", "[[Ewald summation and PME]]"]
updated: 2026-09-27
---
# Net charge changes in alchemical calculations

- With PME, a non-neutral box is implicitly neutralized by a uniform background charge; if the net
  charge changes with λ, the free energy picks up finite-size and background artefacts that do not
  cancel between legs.
- Remedies: co-alchemical ions (turn an ion on as a charge vanishes), analytical corrections
  (Rocklin et al., doi:10.1063/1.4826261), or restraints on the total λ-weighted charge.
- BLaDE implements three charge-restraint forms (`kChargeRestraint1/2/3`, [[BLaDE charge restraints]]).

MSLD with equal-charge variants avoids the problem: if every variant at a site has the same net
charge, Σ_b λ_b Q_b is constant because Σλ = 1. Hence our rule: refuse sites whose variants differ
in net charge ([[ADR-0021 Charge averaging, renormalization, iso-charge guard|ADR-0021]]), and make each variant's charge an exact integer by renormalization.

