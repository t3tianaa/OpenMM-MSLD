---
title: Kabsch superposition
type: theory
status: reviewed
related: ["[[Coordinate alignment]]"]
updated: 2026-09-27
---
# Kabsch superposition

Optimal rigid rotation + translation that minimizes RMSD between two paired point sets.

```
 center P (mobile) and Q (target);  H = Pᵀ Q;  U S Vᵀ = svd(H)
 d = sign(det(V Uᵀ));   R = V · diag(1, 1, d) · Uᵀ;   t = q̄ − R p̄
```

The `d` term prevents a mirror image. Needs ≥ 3 non-collinear points. Source: Kabsch, W.
*Acta Cryst.* A32, 922 (1976). Our implementation: `prep/assemble/align.py:kabsch`.

