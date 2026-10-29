---
id: ISS-001
type: issue
title: Atom restraint groups have the wrong meaning
status: investigating
kind: bug
severity: high
confidence: source
source: "[[AUD-001 Engine audit of the local working copy|AUD-001]]"
affects: ["[[Atom restraint module]]", "[[Mapping component]]"]
requirements: ["[[REQ-014 Atom restraints between substituents|REQ-014]]"]
fixed_by: ["[[TASK-031 Rebuild atom restraint groups|TASK-031]]"]
found: 2026-09-26
updated: 2026-10-29
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

**Update 2026-10-29 (AUD-003).** Confirmed on MDM2: with the per-block groups on, a switched-off side
chain (own LJ scaled to ~0) is pulled onto its centroid and its full-strength intra-block LJ and 1-4
terms reach ~1e6 kJ/mol. With them off (and ISS-027 fixed) the off-state dU/dλ is tens of kJ/mol and
the variants mix. `model_from_mappings(add_restraints=...)` now defaults to False (ADR-0033 step 3);
equivalent-atom groups are still to do (TASK-031).
