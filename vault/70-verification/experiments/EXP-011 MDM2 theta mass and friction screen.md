---
id: EXP-011
type: experiment
title: MDM2 theta mass and friction screen
status: done
date: 2026-10-30
requirements: ["[[REQ-016 Canonical sampling of atoms and theta|REQ-016]]", "[[REQ-017 Per-block theta mass, friction and fixing|REQ-017]]"]
issues: ["[[ISS-002 Theta mass convention differs from BLaDE|ISS-002]]", "[[ISS-018 Theta runs hot in MDM2|ISS-018]]"]
related: ["[[ADR-0038 Theta units and default theta mass|ADR-0038]]", "[[EXP-006 MDM2 theta-parameter sweep|EXP-006]]"]
---
# EXP-011 — MDM2 θ mass/friction screen on the fixed build

Solvated MDM2 (amber14, 5 variants at one site: WT = ALA, ILE, LEU, SER, VAL), clash guards on
([[EXP-010 MDM2 grafted-block clash guards|EXP-010]]), Python `LambdaDynamics` (BAOAB, dt 1 fs, atom friction 1 ps⁻¹), fnex 5.5,
shared start, short runs on a laptop (Apple OpenCL). Outputs and scripts are on the owner's Mac
(`test_systems/mdm2/out/`, not committed); `out/RESUME.md` has the per-run tables.

**Result.** BLaDE-equivalent θ mass 0.05 amu·nm² with friction 1 ps⁻¹ was stable, kept T_θ near
300 K and was the most mobile setting: 58 changes of the leading variant vs 0 with the old 10 / 20
(θ diffusion D = kT/(mγ) ≈ 0.0125 rad²/ps, i.e. θ effectively frozen). Adopted as the default
([[ADR-0038 Theta units and default theta mass|ADR-0038]]).

**Caveats.** Single short runs per setting (see the EXP-006 lesson on noisy T_θ). Atom friction 0.1
ps⁻¹ and dt 2 fs (BLaDE) were not tested — plugin stage.
