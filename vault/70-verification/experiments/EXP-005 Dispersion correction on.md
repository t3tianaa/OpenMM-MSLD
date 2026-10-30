---
id: EXP-005
type: experiment
title: Dispersion correction on
status: done
date: 2026-09-26
requirements: ["[[REQ-024 Dispersion correction preserved|REQ-024]]", "[[REQ-023 Lambda one reproduces the base system|REQ-023]]"]
issues: ["[[ISS-007 Dispersion correction removed for the whole system|ISS-007]]"]
related: ["[[AUD-001 Engine audit of the local working copy|AUD-001]]"]
---
# EXP-005 — Dispersion correction on (audit E5)

Toy with dispersion correction on: scaled λ = 1 gives 290.1636 vs base 290.1659 kJ/mol — the master
invariant breaks because the correction is removed for the whole system.

