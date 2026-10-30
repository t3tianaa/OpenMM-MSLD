---
id: ADR-0037
type: adr
title: Whitelist force types
status: proposed
date: 2026-09-27
deciders: [Tetiana]
affects: ["[[Force scaling component]]"]
requirements: ["[[REQ-022 Refuse unsupported input loudly|REQ-022]]"]
retrospective: false
---
# ADR-0037 — Whitelist force types; raise on anything else touching alchemical atoms (proposed)

## Context
`_check_unhandled` only rejects CMAP. GB forces, RBTorsionForce, AMOEBA, pre-existing custom forces
or a second NonbondedForce touching alchemical atoms would stay at full strength silently
([[ISS-005 Unsupported force types silently unscaled|ISS-005]]).

## Proposed decision
Maintain an explicit whitelist: HarmonicBond/Angle, PeriodicTorsion, CustomTorsion (CHARMM
impropers, recognized expression), NonbondedForce (one), CHARMM tabulated CustomNonbondedForce
(recognized), CMMotionRemover, barostats, our own MSLD forces. Any other force with a particle in an
alchemical block → raise with the force name. Forces touching only env atoms are allowed.

