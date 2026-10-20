---
id: ADR-0023
type: adr
title: Restraint groups per block centroid
status: deprecated
date: 2026-08-10
deciders: [Tetiana]
affects: ["[[Atom restraint module]]", "[[Mapping component]]"]
requirements: ["[[REQ-014 Atom restraints between substituents|REQ-014]]"]
superseded_by: ["[[ADR-0033 Atom restraints group equivalent atoms|ADR-0033]]"]
retrospective: true
---
# ADR-0023 — Atom restraints: one group per block, held to its own centroid (as built — WRONG)

## What was decided
"CATS" restraints were read as "keep a switched-off substituent near its centroid", implemented as
one group per block containing all its atoms, on by default in prep.

## Why it is deprecated
BLaDE's groups are equivalent atoms across substituents ([[BLaDE atom restraints and soft bonds]]);
our groups squeeze each side chain toward a point and distort all variants ([[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]]). Replacement:
[[ADR-0033 Atom restraints group equivalent atoms|ADR-0033]].

