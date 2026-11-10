---
id: EXP-014
type: experiment
title: MDM2 NVE drift diagnosis
status: done
date: 2026-11-09
requirements: ["[[REQ-016 Canonical sampling of atoms and theta|REQ-016]]"]
issues: []
related: ["[[Production plugin architecture]]"]
---
# EXP-014 — MDM2 NVE drift diagnosis

Details and all numbers: `docs/nve_drift.md` and `diagnostics/drift_mdm2.py` in openmm-ld, branch `drift-diagnosis`.

**Result (Verified):** from one frame equilibrated for 8 ps, 10 ps of NVE at 1 fs with zero friction drifts −0.10 ± 0.14 kJ/mol/ps with θ free and +0.22 ±
0.13 at a fixed endpoint, out of about −268,000 kJ/mol. The 22–25 kJ/mol/ps measured earlier came from fits to the first fractions of a picosecond after
minimization: energy rises about 120 kJ/mol in 0.1 ps, then settles.

Plugin and stock `NonbondedForce` behave alike at an endpoint. With atoms frozen, θ conserves energy to 0.002 kJ/mol rms, improving with dt. The padded
neighbour list and constraint tolerance make no visible difference.

**Open:** the mechanism of the 120 kJ/mol jump at the start. A drift much below 0.3 kJ/mol/ps can't be ruled out.
