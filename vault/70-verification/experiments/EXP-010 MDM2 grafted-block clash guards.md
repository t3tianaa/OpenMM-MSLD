---
id: EXP-010
type: experiment
title: MDM2 grafted-block clash guards
status: done
date: 2026-10-30
requirements: ["[[REQ-026 Energy minimization at fixed lambda|REQ-026]]"]
issues: ["[[ISS-028 Grafted blocks clash with the environment|ISS-028]]"]
related: []
---
# EXP-010 — MDM2 grafted-block clash guards

Solvated MDM2 build (amber14, 26 320 atoms), CPU platform, `minimize(max_iterations=5000)` with
`relax_blocks` + `check_endpoints`. Script `/tmp/msld_theta_check/mdm2_prep_guard_check.py`.

| | fix_clashes=False | fix_clashes=True |
|---|---|---|
| worst contact as built | ILE HD13–MET38 SD 0.115 nm; LEU HB31–GLU90 H 0.073; SER HB22–GLU90 H 0.123; VAL 0.134 | ILE HG21–SER87 HG 0.160; VAL HG11–MET38 SD 0.192; LEU, SER none |
| rotamer applied | — | ILE χ1 240° + CB–CG1 240°; LEU χ1 120°; SER χ1 120°; VAL χ1 120° |
| endpoint E before minimize, rel. WT (kJ/mol) | ILE +245 677, LEU +535 500, SER +1 145, VAL +108 | ILE +71, LEU +148, SER +40, VAL +331 |
| endpoint gap after minimize (kJ/mol) | WT 0, ILE 36.9, LEU 7.6, SER 35.4, VAL 18.5 | LEU 0, WT 52.9, VAL 63.2, SER 99.6, ILE 138.8 |
| check_endpoints | passes | passes |

Reading (Inferred): with `relax_blocks` the per-endpoint minimization alone removes these MDM2
clashes; the rotamer search removes them before any minimization, so the build no longer depends on
a local minimizer escaping a 0.07–0.15 nm overlap. The rotamer chosen is the least clashing, not the
lowest energy, so after minimization the endpoint gaps differ (0–139 vs 0–37 kJ/mol); both are
ordinary chemistry-sized gaps that ALF absorbs.
