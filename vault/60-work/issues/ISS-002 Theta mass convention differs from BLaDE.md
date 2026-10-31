---
id: ISS-002
type: issue
title: Theta mass convention differs from BLaDE
status: fixed
kind: divergence
severity: high
confidence: inferred
source: "[[AUD-001 Engine audit of the local working copy|AUD-001]]"
affects: ["[[MSLD model component]]", "[[Lambda dynamics integrator component]]"]
requirements: ["[[REQ-016 Canonical sampling of atoms and theta|REQ-016]]", "[[REQ-017 Per-block theta mass, friction and fixing|REQ-017]]"]
fixed_by: ["[[TASK-032 Resolve BLaDE theta units|TASK-032]]", "[[TASK-033 Rerun MDM2 with reference theta parameters|TASK-033]]"]
found: 2026-09-26
updated: 2026-10-31
---
# ISS-002 — θ mass convention differs from BLaDE (audit F2, corrected)

**Claim in the audit.** BLaDE computes `sin(θ·ANGSTROM)`; in the NMPS (GROMACS-unit) build
ANGSTROM = 0.1, so a BLaDE θ mass m equals 100·m in our radian units; BLaDE's m = 5 ≈ 500 here,
while MDM2 uses 10 — θ ~50× too light, 20× more friction → possibly the whole "hot θ" problem.

**Correction (2026-09-27).** BLaDE also builds in AKMA (CHARMM) units, where ANGSTROM = 1 and the time
unit is ≈ 48.9 fs; there m = 5 is ≈ 0.05 in our units — the *opposite* direction. `CompileOptions.sh`
defaults to AKMA; `CMakeLists.txt` defaults to NMPS; inside CHARMM it is AKMA
([[BLaDE units and theta mass]]). So we do not yet know whether our θ is too light or too heavy.

**Impact.** Conclusions about θ temperature, the need for the plugin, and parameter defaults all
depend on this.

**Next.** [[TASK-032 Resolve BLaDE theta units|TASK-032]] (resolve units) then [[TASK-033 Rerun MDM2 with reference theta parameters|TASK-033]] (MDM2 rerun with reference-equivalent
parameters); decision [[ADR-0038 Theta units and default theta mass|ADR-0038]].


**Resolved (2026-10-31).** Production BLaDE is the AKMA build: m = 5 amu·Å² = 0.05 amu·nm² in our
units, i.e. our old masses 5–40 were 100–800× too heavy, not too light. Defaults changed
([[ADR-0038 Theta units and default theta mass|ADR-0038]]); verified on MDM2 in [[EXP-011 MDM2 theta mass and friction screen|EXP-011]].
