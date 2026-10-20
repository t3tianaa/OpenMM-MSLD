---
id: FEAT-022
type: feature
title: MDM2 test system
status: done
milestone: M3
implements: ["[[REQ-040 Ingest Amber, CHARMM, PDB and SDF inputs|REQ-040]]", "[[REQ-042 Map amino-acid mutation sites|REQ-042]]", "[[REQ-047 Solvate and neutralize consistently|REQ-047]]"]
components: ["[[Prep facade component]]", "[[Lambda dynamics integrator component]]"]
tasks: ["[[TASK-021 Make the MDM2 run work end to end|TASK-021]]", "[[TASK-022 Fix hybrid output artifacts|TASK-022]]", "[[TASK-023 Theta-stability sweep on MDM2|TASK-023]]", "[[TASK-033 Rerun MDM2 with reference theta parameters|TASK-033]]"]
issues: ["[[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]]", "[[ISS-018 Theta runs hot in MDM2|ISS-018]]", "[[ISS-022 Ingest does not validate geometry|ISS-022]]"]
created: 2026-08-21
updated: 2026-09-27
retrospective: true
---
# FEAT-022 — MDM2 test system

`test_systems/mdm2/`: MDM2 protein + 12-residue peptide (THR-SER-PHE-ALA-GLU-TYR-TRP-ALA-LEU-LEU-SER-PRO),
site = peptide residue 4, variants ILE/LEU/SER/VAL (+ WT), Amber ff14SB, TIP3P, ~26 k atoms,
`mdm2_run.py` (OpenCL, bond/angle unscaled, θ mass 10, friction 20, 10 000 steps).

**Caution:** the existing outputs (`out/`, 49 MB, not to be committed) include the wrong restraint
groups ([[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]]) and hot, unconverged θ ([[ISS-018 Theta runs hot in MDM2|ISS-018]]) — not scientific results.

