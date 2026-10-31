---
title: ALF package overview
type: reference
status: partial
system: alf
version: not pinned
related: ["[[REQ-030 Adaptive landscape flattening]]", "[[ALF flattening component]]"]
updated: 2026-10-31
---
# ALF package overview (partly studied 2026-10-31)

The ALF Python package (github.com/RyanLeeHayes/ALF, Hayes and co-workers) automates adaptive
landscape flattening for CHARMM and BLaDE: it writes the bias variables (`variables*.inp`, e.g.
`cs1s1s1s2` coefficients used by `cb7.inp`), runs short simulations, analyses λ trajectories, updates
b, c, x, s, and finally analyses production runs.

**Not yet studied in this project.** Before replacing our heuristic ([[ADR-0034 Adopt published ALF and two-leg ddG|ADR-0034]]) we must read and
document ([[TASK-074 Study the ALF package|TASK-074]]):
- the file layout and loop (initial flattening, short → long iterations, production);
- the exact objective used to update biases (likelihood / WHAM), regularization, damping;
- the λ histogram binning and the cutoff for end states;
- the production free-energy estimator and how uncertainties are computed;
- whether it can drive OpenMM directly (then we could call it rather than re-implement).


## Findings (2026-10-31, from the public source; MIT licence)
Read: `alf/GetEnergy.py`, `GetFreeEnergy5.py`, `SetVars.py`, `runflat.py`, `postprocess.py`, README.
**Not read** (fetch failed): `alf/RunWham.py`, `linear2018.py`, the `wham/` and `dca/` C/CUDA —
the histogram model itself is unverified.

**Bias energy** (`GetEnergy`, physical sign; the CHARMM variables carry −c, −x, −s):
E = −Σ b_k λ_k − Σ c_jk λ_j λ_k − Σ x_jk (1 − e^(−5.56 λ_j)) λ_k − Σ s_jk λ_j/(λ_j + 0.017) λ_k
(`bcxs2018`; `bcxstu2026` uses α = 0.012 and adds t, u terms). x and s are directional (j, k and
k, j are separate). Our engine already has these as types 6, 10 (l0 = −5.56) and 8 (l0 = 0.017).

**Update per cycle.** Reweight the current + 4 previous cycles to the current biases; build 1D λ
profiles (400 bins) and 2D pair profiles (20 × 20); linear model of the profiles in the bias
increments; quadratic penalty on deviation from flat; solve C·Δ = V. Regularisation C_ii += cut_i⁻²
with cuts b 2, c 8, x 2, s 1 (inter-site c 2, x 0.5, s 0.5); whole step scaled so max |Δ_i/cut_i| ≤ 1.5.
Cumulative sums; gauge = first block of each site. Units kcal/mol (CHARMM) — inferred.

**Schedule (README).** 50–100 cycles of 100 ps (first 25 ps discarded; ~200 for Arg), then ~10 × 1 ns,
then production 5 independent duplicates (e.g. 5 × 5, 20, 100 ns). No automatic convergence test.
Restart each cycle from a random one of the last 5 runs. Production ΔG: histogram estimator with
endpoint cutoff λ > 0.99, bootstrap over duplicates.

**Driving it from our engine (option 3).** Needs λ written in CHARMM `.lmd` or BLaDE XDR format and
the `variables*.inp` / pycharmm YAML read back; the `engine` string is hard-coded (charmm, bladelib,
blade, pycharmm). Porting the update (option 2) is the likely route; validate against ALF on the
same λ data.
