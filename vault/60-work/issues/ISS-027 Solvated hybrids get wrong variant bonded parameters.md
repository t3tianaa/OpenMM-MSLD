---
id: ISS-027
type: issue
title: Solvated hybrids get wrong variant bonded parameters
status: fixed
kind: bug
severity: critical
confidence: confirmed
source: "[[AUD-003 Theta and lambda-dynamics integration review|AUD-003]]"
affects: ["[[Assembly component]]", "[[Grafting and term transplant]]"]
requirements: ["[[REQ-041 Lossless parameters including NBFIX|REQ-041]]"]
fixed_by: []
found: 2026-10-29
updated: 2026-10-29
---
# ISS-027 — Solvated hybrids get wrong variant bonded parameters

**Symptom.** In the solvated MDM2 hybrid every ILE bond had r0 = 0.109 nm (C–C included), every
angle k = 292.88, and every ILE 1-4 pair the same C–H LJ. Without solvent the parameters were right.

**Cause.** `prep/assemble/merge.py:_TypeCache.get` appended `copy.copy(type)` to the hybrid's type
list without re-owning it, so the copy's `.idx` still indexed the variant's own list.
`solvate()` copies the Structure, and ParmEd rebuilds each term from `base.<types>[t.idx]`, which
picked an unrelated environment type. Bonds, angles, dihedrals (and any other transplanted type).

**Impact.** Every solvated build before 2026-10-29, including all MDM2 runs: variant side chains had
wrong geometry; together with [[ISS-001 Atom restraint groups have the wrong meaning|ISS-001]] they
collapsed when switched off (dU/dλ ~1e6 kJ/mol), which no soft-core can fix.

**Fix.** `base_list.claim()` after each append; regression test
`test_build.test_solvated_build_keeps_variant_bonded_parameters` (fails on the old code).
