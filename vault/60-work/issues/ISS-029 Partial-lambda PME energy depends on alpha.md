---
id: ISS-029
type: issue
title: Partial-lambda PME energy depends on alpha
status: open
kind: risk
severity: medium
confidence: confirmed
source: "[[EXP-013 Plugin PME against a plain Ewald sum|EXP-013]]"
affects: ["[[MSLD energy function spec]]"]
requirements: ["[[REQ-020 Accurate dU-dlambda for every term|REQ-020]]"]
fixed_by: []
found: 2026-11-09
updated: 2026-11-09
---
# ISS-029 — Partial-lambda PME energy depends on alpha

**Verified** (`python/tests/test_ewald_reference.py` in openmm-ld): with the [[MSLD energy function spec]], the total
energy at partial λ under PME changes with the Ewald splitting parameter α when a block has within-block pairs. On the
oracle toy (Coulomb only, λ = 0.3, 0.1, 0.6 at site 1, 0.5, 0.5 at site 2), α from 2.5 to 4.0 nm⁻¹ moves the energy from
−59.346 to −59.556 kJ/mol without soft-core and spreads it over 0.10 kJ/mol with soft-core. With no within-block
pairs and no soft-core the same sum is constant to 13 digits, so this is the spec and not a numerical error.

**Cause (Inferred from the spec's terms):** a within-block pair carries λ in direct space and λ² in reciprocal space, so α
decides how much of it scales each way. Soft-core direct space adds a similar mismatch.

**Source:** the spec says BLaDE uses the same convention; not yet checked by running BLaDE.

## What to do
- Every partial-λ comparison under PME has to use the same α, BLaDE included ([[TASK-043 BLaDE fixed-lambda cross-check|TASK-043]]).
- Open question: does the α dependence matter for free energies on real systems, where within-block pairs are few and
  the same α is used throughout? Not measured.
