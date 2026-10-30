---
id: REQ-023
type: requirement
title: Lambda one reproduces the base system
area: engine
priority: must
status: verified
derives_from: ["[[G-2 Physically correct MSLD|G-2]]"]
satisfied_by: ["[[FEAT-002 Bonded term scaling|FEAT-002]]", "[[FEAT-003 Electrostatics scaling|FEAT-003]]", "[[FEAT-004 Lennard-Jones scaling|FEAT-004]]", "[[FEAT-005 1-4 exception scaling|FEAT-005]]"]
verified_by: ["test_master"]
decisions: ["[[ADR-0011 Master invariant as the primary gate|ADR-0011]]"]
created: 2026-08-05
updated: 2026-09-27
retrospective: true
---
# REQ-023 — λ = 1 reproduces the base system

**Statement.** With every block's λ = 1 (and all biases/restraints off), the scaled System shall
reproduce the unscaled base System's energy and forces to machine precision (~1e-12 relative).
This is the **master invariant** ([[Invariants]]).

Note: "λ = 1 for every block" is not a physical state (per site Σλ = 1), so this invariant checks
the *bookkeeping*, not the partial-λ physics. It is necessary but far from sufficient ([[ISS-012 No validation at partial lambda|ISS-012]]).

## Acceptance criteria
- [x] AC1 — `test_master` ~1e-13 on Reference and OpenCL toys.
- [ ] AC2 — also with dispersion correction on ([[ISS-007 Dispersion correction removed for the whole system|ISS-007]]).

