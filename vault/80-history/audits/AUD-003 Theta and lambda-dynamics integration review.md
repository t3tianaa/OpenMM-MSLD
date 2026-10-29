---
id: AUD-003
type: audit
title: Theta and lambda-dynamics integration review
status: done
date: 2026-10-29
related: ["[[ISS-026 Constrained atoms run below the bath temperature|ISS-026]]", "[[ISS-013 Soft-core off while BLaDE examples use it|ISS-013]]", "[[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]]"]
---
# AUD-003 — θ and λ-dynamics integration review (2026-10-29)

Numerical review of `LambdaDynamics` on a PME TIP3P toy (Reference, CPU, Apple OpenCL) and on MDM2
(OpenCL). Scripts and logs: project files `audits/theta/`.

## Correct
- λ = softmax(fnex·sin θ) and the chain rule: analytic dU/dθ equals FD of total U to 4 decimals.
- Hybrid dU/dλ equals FD of total U (Reference): nothing λ-dependent is dropped.
- BAOAB ordering of θ and atoms; NVE conserves H = Kx + Kθ + U (no extra drift from θ).

## Found
1. Constrained atoms ran ~30 K cold → [[ISS-026 Constrained atoms run below the bath temperature|ISS-026]], fixed by [[ADR-0044 Own SHAKE in the Python driver|ADR-0044]].
2. Endpoint trap: switched-off blocks fill with solvent (same-site pairs are correctly excluded),
   dU/dλ 1e5–1e6, λ never returns; MDM2's "hot θ" is a ~20,000 K transient during the initial λ
   collapse, unchanged by FD step or dt → [[ADR-0043 Soft-core on by default for overlap-prone pairs|ADR-0043]].
3. FD noise is roundoff ∝ 1/h, 17.7 kJ/mol rms at 27k atoms on fp32 OpenCL → [[ADR-0045 Analytic biases and a large FD step|ADR-0045]].
4. Smaller: `Block.fixed` freezes θ not λ (doc fixed); cached forces must be invalidated after
   outside changes (`invalidate_forces()`); no atom-temperature diagnostic (`atom_temperature()` added).
