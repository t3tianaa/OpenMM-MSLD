---
title: 1-4 exception scaling module
type: component
subsystem: "[[Simulation subsystem]]"
layer: L3
status: partial
code: [msld/forces.py]
requirements: ["[[REQ-009 1-4 pair scaling|REQ-009]]"]
decisions: ["[[ADR-0007 Charges scaled by NonbondedForce offsets|ADR-0007]]", "[[ADR-0028 Refuse what cannot be scaled|ADR-0028]]"]
issues: ["[[ISS-015 Cross-site 1-4 and CMAP are refused|ISS-015]]"]
updated: 2026-09-27
---
# 1-4 exception scaling module — `add_scaled_14_exceptions`

For each `NonbondedForce` exception with non-zero chargeProd or ε that involves an alchemical atom:
`classify_pair` → `single` b: set base (qq, ε) to 0 and add
`addExceptionParameterOffset("lambda_b", k, qq, 0, ε)` → linear λ_b (both elec and LJ 1-4, incl.
CHARMM ε14 and 1-4 NBFIX). `product` (cross-site) → raises `NotImplementedError` ([[ISS-015 Cross-site 1-4 and CMAP are refused|ISS-015]]);
`exclude` (same site) → raises (illegal topology, same as BLaDE's fatal error).

dU/dλ: finite difference (NonbondedForce, group 0).

