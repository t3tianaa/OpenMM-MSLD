---
id: EXP-006
type: experiment
title: MDM2 theta-parameter sweep
status: done
date: 2026-09-16
requirements: ["[[REQ-016 Canonical sampling of atoms and theta|REQ-016]]"]
issues: ["[[ISS-018 Theta runs hot in MDM2|ISS-018]]", "[[ISS-002 Theta mass convention differs from BLaDE|ISS-002]]"]
related: ["[[FEAT-022 MDM2 test system|FEAT-022]]"]
---
# EXP-006 — MDM2 θ-parameter sweep (dry, bond/angle unscaled, minimized)

**Result.** Stability fully solved by `scale_bond = scale_angle = False` + minimization: nothing blows
up for θ mass 5–40, friction 2–20 ps⁻¹, FD step 1e-4…3e-2, dt 0.25–1 fs. But T_θ was governed by
friction alone: ≈ 8 000 K (γ = 2), 2 400 K (10), 1 400 K (20) while θ explores; it drops to a few
hundred K only after λ collapses to an end point (cos θ → 0 kills the θ force). Mass, FD step and dt
had no reproducible effect.

**Conclusion at the time.** "θ cannot reach 300 K with the FD engine; the plugin is the fix." Now
questioned: θ masses tested (5–40) are ≪ the NMPS-equivalent 500 or ≫ the AKMA-equivalent 0.05; the
sweep never covered either reference regime ([[ISS-002 Theta mass convention differs from BLaDE|ISS-002]]); Apple OpenCL fp32 FD noise ([[ISS-010 Finite-difference dU-dlambda noisy in single precision|ISS-010]])
may be the heat source.

**Lesson.** Single short T_θ runs are very noisy and fake "sweet spots" (a lucky h = 1e-2 → 276 K);
only shared-start multi-thousand-step comparisons were reproducible.

