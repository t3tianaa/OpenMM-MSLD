---
id: G-3
type: goal
title: Automated system preparation
status: active
updated: 2026-09-27
---
# G-3 — Automated system preparation

From standard inputs (PDB / prmtop / psf + parameters / SDF) and a list of variants, build a
correct hybrid MSLD system: shared environment, one block per variant, consistent charges and
parameters, aligned coordinates, solvent and ions — with no hand editing.

Why: preparation is where most real-world errors enter, and it is the most time-consuming manual
step in CHARMM-based MSLD workflows ([[BLaDE T4L and HSP90 examples]]).

