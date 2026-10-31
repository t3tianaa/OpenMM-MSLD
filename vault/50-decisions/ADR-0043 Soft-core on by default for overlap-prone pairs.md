---
id: ADR-0043
type: adr
title: Soft-core on by default for overlap-prone pairs
status: accepted
date: 2026-10-29
deciders: [Tetiana]
affects: ["[[Lennard-Jones scaling module]]", "[[Electrostatics scaling module]]"]
requirements: ["[[REQ-011 Soft-core for alchemical nonbonded|REQ-011]]"]
supersedes: ["[[ADR-0025 Soft-core off in the first version|ADR-0025]]"]
superseded_by: []
retrospective: false
---
# ADR-0043 — Soft-core on by default for overlap-prone pairs

## Context
ADR-0025 assumed "U linear in λ keeps dU/dλ bounded". It does not: dU/dλ_b is the unscaled
interaction of block b with its partners, and solvent moves into a switched-off block. Measured in
[[AUD-003 Theta and lambda-dynamics integration review|AUD-003]]: off blocks reach 1e5–1e6 kJ/mol (water
toy and MDM2), λ never returns from an endpoint, and the MDM2 site collapses to WT in ~0.3 ps with a
~20,000 K θ transient. An LJ-only soft-core prototype crashed (NaN): without the r⁻¹² wall the
λ-scaled charges collapse onto opposite charges, so Coulomb needs soft-core as well.

## Options
1. **Keep linear scaling** — variants cannot switch; populations are meaningless.
2. **LJ soft-core only** — unstable (NaN), see above.
3. **LJ + direct-space Coulomb soft-core now, reciprocal space unchanged** — possible with custom
   forces; the plugin (S4) can later replace the correction.

## Decision
Option 3, on by default (`model.softcore_alpha = 0.5`, `model.softcore_sigma_q = 0.3` nm).
Block↔env and cross-site block↔block pairs use
- LJ: U = L·4ε[1/s² − 1/s], s = (r/σ)⁶ + α(1−L) (Beutler), in the existing `MSLDLJ_*` forces;
- Coulomb: a correction force `MSLDSCElec_*` adding L·KE·q₁q₂[g(r_sc) − g(r)] on top of the λ-scaled
  NonbondedForce, r_sc = (r⁶ + α(1−L)σ_q⁶)^(1/6), g the force's real-space kernel (erfc for PME/Ewald,
  1/r, or reaction field).
~~Within-block pairs stay plain (held by the block's bonded terms).~~ **Amended 2026-10-31:**
within-block (1-5+) pairs are soft-cored too (L = λ_b), LJ and direct-space Coulomb, as BLaDE does
(`nbdirect.cu`: rSoft = R·(1−λ_b) for a same-block pair). A switched-off block has its torsions and
1-4s off as well, so on MDM2 the ILE side chain folded onto itself and its plain within-block LJ put
1e4–6e4 kJ/mol spikes into dU/dλ_ILE (off-state p99 2.8e4), which kicked θ_ILE back off.
`softcore_alpha = 0` restores the old linear scaling.

## Consequences
- λ = 1 (all λ ∈ {0, 1}) energies are unchanged; master invariant holds (test_softcore, test_master).
- dU/dλ of an overlapped off block drops from 1e33 to ~20 kJ/mol in test_softcore.
- dU/dλ stays analytic for the new terms. The NonbondedForce FD part still contains the plain
  Coulomb whose large derivative the correction cancels; exact in double, roundoff-limited in fp32.
- Tabulated CHARMM/NBFIX LJ is not soft-cored yet (a warning is raised).
- Energies at intermediate λ differ from earlier runs; old ALF biases need relearning.

## Links
[[Soft-core potentials]], [[FEAT-031 Soft-core|FEAT-031]], [[ISS-013 Soft-core off while BLaDE examples use it|ISS-013]].
