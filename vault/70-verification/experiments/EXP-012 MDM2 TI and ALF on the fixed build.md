---
id: EXP-012
type: experiment
title: MDM2 TI and ALF on the fixed build
status: done
date: 2026-10-31
requirements: ["[[REQ-030 Adaptive landscape flattening|REQ-030]]", "[[REQ-060 Free energy per variant with uncertainty|REQ-060]]"]
issues: ["[[ISS-011 ALF is a heuristic and ddG is single-leg|ISS-011]]"]
related: ["[[EXP-011 MDM2 theta mass and friction screen|EXP-011]]", "[[ALF package overview]]", "[[ADR-0043 Soft-core on by default for overlap-prone pairs|ADR-0043]]"]
---
# EXP-012 — MDM2 complex-leg TI and warm-started ALF (Python engine)

Same system and θ parameters as [[EXP-011 MDM2 theta mass and friction screen|EXP-011]], with the within-block soft-core (PR #5,
ADR-0043 amendment). Outputs on the owner's Mac (`out/ti_pr5/`, `out/alf_warm/`), not committed.

## Within-block soft-core check
ILE's off-state χ1 eclipses CG2/CD1 methyl H's to 0.08 nm; with plain within-block LJ, 276 / 2 000
frames had off-state |dU/dλ| > 1e3 (max 8.8e9). With the soft-core: 0 frames, max 574. LEU and VAL
spikes gone too.

## TI (complex leg only), λ_LEU = 1−s, λ_X = s, 5 Gauss–Legendre nodes, ΔG(LEU→X) kJ/mol
VAL +29.6 ± 1.7 · WT +34.6 ± 1.4 · SER +51.7 ± 3.2 (realistically ± 5–10) · ILE +78.5 ± 3.5.
Single leg: not a ΔΔG. Used only as starting biases for ALF.

## Warm-started ALF (msld/alf.py heuristic), 15 iterations × 15 ps
Initial b = −TI (WT −34.6, ILE −78.5, LEU 0, SER −51.7, VAL −29.6). b rate 0.6 / cap 8 at the floor
(mean λ < 0.01), else 0.3 / cap 3; type-6 couplings on once every mean λ > 0.05.

| iter | mean λ WT / ILE / LEU / SER / VAL | leader changes | worst \|dp\| |
|---|---|---|---|
| 4 | .46 / .13 / .18 / .03 / .20 | 51 | 0.26 |
| 6 | .27 / .17 / .11 / .08 / .38 | 52 | 0.18 |
| 8 | .17 / .01 / .01 / .77 / .04 | 9 | 0.57 |
| 11 | .20 / .04 / .33 / .15 / .28 | 36 | 0.16 (best) |
| 15 | .04 / .17 / .56 / .03 / .20 | 41 | 0.36 |

Final b: WT −42.5, ILE −86.4, LEU −3.2, SER −70.9, VAL −27.0. Final couplings: LEU–VAL +27.4,
ILE–LEU +12.5, WT–VAL +7.9, ILE–VAL +5.3, WT–LEU +0.4, SER–VAL −2.1, WT–ILE −5.4, LEU–SER −5.9,
WT–SER −6.7, ILE–SER −8.9. T_atoms 298–300 K, T_θ 240–364 K. **Not converged.**

## Reading
- Switching is good (34–72 leader changes per iteration, all five variants visited) — a large
  improvement over every earlier run.
- But endpoints are rarely committed: λ > 0.99 ≤ 3 % per variant after iteration 8 (SER 57–66 % in
  iterations 7–8 while it dominated). ΔG needs physical-endpoint samples, so these runs mostly sample
  alchemical blends.
- b and c trade off: positive couplings climb at the cap every iteration (LEU–VAL to +27) while
  blends persist; SER couplings go negative and SER's b drifts to −71 (TI −52). The pairwise
  heuristic cannot fix endpoint commitment; the published ALF tunes the x/s endpoint terms jointly
  with b/c from pooled histograms and runs 50–100 × 100 ps cycles (≈ 30× our sampling)
  ([[ALF package overview]]).

**Decision (2026-10-31, Tetiana).** No further ALF tuning on the laptop; adopt the published ALF
algorithm at the plugin stage ([[ADR-0034 Adopt published ALF and two-leg ddG|ADR-0034]], [[TASK-046 Implement or adopt standard ALF|TASK-046]]). The iteration-11 biases are the best
starting point found so far.
