---
id: ISS-028
type: issue
title: Grafted blocks clash with the environment
status: fixed
kind: bug
severity: high
confidence: confirmed
source: "[[AUD-003 Theta and lambda-dynamics integration review|AUD-003]]"
affects: ["[[Assembly component]]", "[[Grafting and term transplant]]"]
requirements: ["[[REQ-026 Energy minimization at fixed lambda|REQ-026]]"]
fixed_by: []
found: 2026-10-30
updated: 2026-10-30
---
# ISS-028 — Grafted blocks clash with the environment

**Symptom.** On MDM2 (peptide ALA→ILE/LEU/SER/VAL) λ_ILE and λ_SER never left 0 in ALF, while their
biases ran to −45 kJ/mol. As built, ILE CD1 sat 0.147 nm (HD13 0.115 nm) from MET38 SD, LEU HB31
0.073 nm from GLU90 H, SER HB22 0.123 nm from GLU90 H. Endpoint energies of the unminimized build:
ILE +2.5e5, LEU +5.4e5 kJ/mol above WT. Minimizing at partial λ does not remove it: soft-core hides
the clash (ILE stayed ~3e5 above the others).

**Cause.** `prep/assemble/structure.py` places each variant's block by backbone alignment in the
rotamer of the variant file; nothing checked it against the environment.

**Fix.** Three layers (Verified on MDM2, [[EXP-010 MDM2 grafted-block clash guards|EXP-010]]):
1. `prep/assemble/clash.py:relieve_clashes`, run by `HybridSystemAssembler.assemble(fix_clashes=True)`
   (default) before solvation: every clashing non-reference block tries the staggered rotamers of
   χ1 and of its first-shell bonds and keeps the lowest clash score; remaining clashes deeper than
   0.03 nm warn; all are in `bundle.reports["clashes"]`.
2. `LambdaDynamics.relax_blocks` (from `minimize`): each block minimized alone at its own endpoint.
3. `LambdaDynamics.check_endpoints` (from `minimize`): warns above a 1e3 kJ/mol endpoint gap, raises
   above 1e4, naming the block and its closest non-excluded contact.
Tests: `test_clash` (rotamer relief, H-bond/1-4 exemptions, endpoint check), `test_minimize`.

**Limits.** Rotamers are rigid 0/120/240° steps about χ1 and first-shell bonds only (no χ3+, no
backbone moves, no ring flips); a block bonded to two env atoms (proline-like) is not rotated.
