---
id: ADR-0024
type: adr
title: Home-grown ALF heuristic
status: deprecated
date: 2026-09-16
deciders: [Tetiana]
affects: ["[[ALF flattening component]]"]
requirements: ["[[REQ-030 Adaptive landscape flattening|REQ-030]]", "[[REQ-060 Free energy per variant with uncertainty|REQ-060]]"]
superseded_by: ["[[ADR-0034 Adopt published ALF and two-leg ddG|ADR-0034]]"]
retrospective: true
---
# ADR-0024 — Home-grown ALF heuristic (as built)

## What was decided
Implement flattening in three phases: fixed biases by log-occupancy updates (P1), type-6 couplings
toward the bare-softmax overlap (P2), ΔΔG from the converged biases (P3).

## Why it is deprecated
It is not the published ALF (missing skew and end-point terms, no histogram likelihood fit);
`estimate_ddg` is single-leg; the reasoning against endpoint-population estimators is doubtful
([[ISS-011 ALF is a heuristic and ddG is single-leg|ISS-011]]). Replacement: [[ADR-0034 Adopt published ALF and two-leg ddG|ADR-0034]].

