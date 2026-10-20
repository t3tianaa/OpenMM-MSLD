---
id: ISS-001
type: issue
title: Atom restraint groups have the wrong meaning
status: open
kind: bug
severity: high
confidence: source
source: "[[AUD-001 Engine audit of the local working copy|AUD-001]]"
affects: ["[[Atom restraint module]]", "[[Mapping component]]"]
requirements: ["[[REQ-014 Atom restraints between substituents|REQ-014]]"]
fixed_by: ["[[TASK-031 Rebuild atom restraint groups|TASK-031]]"]
found: 2026-09-26
updated: 2026-09-27
---
# ISS-001 — Atom restraint groups have the wrong meaning (audit F1)

**Symptom.** Each block's side chain is pulled toward its own centroid with k = 24 769 kJ/mol/nm² per
atom (≈ 500 kJ/mol per atom for a typical 0.2 nm spread), fighting bonded terms and distorting every
variant's geometry.

**Cause.** `prep/mapping/core.py:model_from_mappings` (`add_restraints=True`, default) adds one group
per block containing **all** its atoms; `forces.add_atom_restraints` then restrains them to their
centroid. BLaDE groups are **equivalent atoms across substituents** — one atom per substituent
(`msld.cu:383-403` comment "one atom per substituent"; RNaseH inputs `site{n}consN`, …)
([[BLaDE atom restraints and soft bonds]]).

**Impact.** Every MDM2 run so far (`mdm2_run.py` uses the default) includes this distortion.

**Fix.** [[ADR-0033 Atom restraints group equivalent atoms|ADR-0033]] → [[TASK-031 Rebuild atom restraint groups|TASK-031]]: default off now; equivalent-atom groups from the core
correspondence where substituents duplicate atoms.

