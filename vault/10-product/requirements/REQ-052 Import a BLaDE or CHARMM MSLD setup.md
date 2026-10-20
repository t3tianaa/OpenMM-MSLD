---
id: REQ-052
type: requirement
title: Import a BLaDE or CHARMM MSLD setup
area: validation
priority: must
status: proposed
derives_from: ["[[UC-3 Validate the engine against BLaDE|UC-3]]"]
satisfied_by: ["[[FEAT-030 BLaDE cross-validation harness|FEAT-030]]"]
created: 2026-09-27
updated: 2026-09-27
---
# REQ-052 — Import a BLaDE / CHARMM MSLD setup

**Statement.** Read a CHARMM psf + parameters + a BLaDE-style MSLD description (block atom
selections, sites, θ initial values, biases, removescaling, restraints, soft-core flags) into an
`MSLDModel`, so the **same** system can run in BLaDE and in our engine ([[BLaDE input script language]]).

