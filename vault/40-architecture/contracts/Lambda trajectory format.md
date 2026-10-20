---
title: Lambda trajectory format
type: contract
status: as-built
code: [msld/io.py]
updated: 2026-09-27
---
# Data contract: λ trajectory (CSV)

```
 step,time_ps,potential_kJ,theta_temp_K,<label block 1>,<label block 2>,…
 100,0.1,-123456.7,812.3,0.93,0.02,0.05
```
Labels: variant names from the mapping (`s{k}:{name}` when several sites), else `lambda{b}`.
Written by `LambdaTrajectoryWriter`, read by `io.read_trajectory`.

Target additions ([[REQ-027 Trajectory, lambda and energy output|REQ-027]], [[REQ-031 Reproducible runs|REQ-031]]): θ values, a header block with run metadata (git
commit, versions, platform/precision, seed, all MSLD parameters, bias coefficients), and an
optional BLaDE-compatible `.lmd` writer for use with ALF analysis tools.
