---
id: ISS-013
type: issue
title: Soft-core off while BLaDE examples use it
status: fixed
kind: divergence
severity: medium
confidence: source
source: "[[AUD-001 Engine audit of the local working copy|AUD-001]]"
affects: ["[[Lennard-Jones scaling module]]", "[[Electrostatics scaling module]]"]
requirements: ["[[REQ-011 Soft-core for alchemical nonbonded|REQ-011]]"]
fixed_by: ["[[TASK-050 Soft-core design spike|TASK-050]]"]
found: 2026-09-26
updated: 2026-10-29
---
# ISS-013 — Soft-core is off, while BLaDE's examples run with it on (audit F12)

`DEFERRED.md` said "BLaDE also runs soft-core-off often"; BLaDE's HSP90, T4L and T4L_peptide examples
all use `msld softcore on`. For overlapping side-chain/ligand variants it is normally on
([[Soft-core potentials]]).

**Update 2026-10-29 (AUD-003).** Soft-core LJ + direct-space Coulomb now on by default ([[ADR-0043 Soft-core on by default for overlap-prone pairs|ADR-0043]]). Not yet for tabulated CHARMM/NBFIX LJ.
