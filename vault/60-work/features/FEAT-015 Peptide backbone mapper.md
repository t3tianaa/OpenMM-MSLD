---
id: FEAT-015
type: feature
title: Peptide backbone mapper
status: done
milestone: M3
implements: ["[[REQ-042 Map amino-acid mutation sites|REQ-042]]"]
components: ["[[Mapping component]]"]
decisions: ["[[ADR-0019 Core defined by identity and equal LJ|ADR-0019]]", "[[ADR-0020 Variants as monomer residues|ADR-0020]]"]
tasks: ["[[TASK-015 Prep redesign phases A to I|TASK-015]]"]
created: 2026-08-19
updated: 2026-09-27
retrospective: true
---
# FEAT-015 — Peptide backbone mapper

`AminoAcidBackboneMapper`: core by name + LJ; backbone-mutation flag. Done for side-chain
mutations; backbone mutations need duplicated backbones + restraints + soft bonds (future).

