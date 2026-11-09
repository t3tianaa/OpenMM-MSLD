---
id: ISS-030
type: issue
title: Prep is not reproducible without a seed
status: open
kind: risk
severity: low
confidence: confirmed
source: "[[Production plugin architecture]]"
affects: ["[[Assembly component]]"]
requirements: []
fixed_by: []
found: 2026-11-09
updated: 2026-11-09
---
# ISS-030 — Prep is not reproducible without a seed

**Verified** (10 MDM2 builds): `Modeller.addHydrogens` places hydrogens at random before minimizing them (OpenMM
`app/modeller.py`, Python's `random`), so two builds of the same input can differ. On MDM2 only THR86:H2 and H3 vary, between
two positions about 0.14 nm apart. System XML and all other positions stay identical. With `random.seed(n)` before the build,
repeated builds are identical.

**Inferred:** the two positions are the same geometry with the two hydrogens' labels swapped. Not confirmed.

## What to do
Seed the build for any comparison between runs. Other systems may have more such atoms; not checked.
