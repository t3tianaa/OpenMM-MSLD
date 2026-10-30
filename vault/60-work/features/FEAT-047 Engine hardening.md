---
id: FEAT-047
type: feature
title: Engine hardening
status: planned
milestone: M4
implements: ["[[REQ-022 Refuse unsupported input loudly|REQ-022]]", "[[REQ-024 Dispersion correction preserved|REQ-024]]", "[[REQ-025 Supported nonbonded methods are correct|REQ-025]]", "[[REQ-018 Holonomic constraints and virtual sites|REQ-018]]"]
components: ["[[Force scaling component]]", "[[Lambda dynamics integrator component]]"]
decisions: ["[[ADR-0037 Whitelist force types|ADR-0037]]", "[[ADR-0039 Dispersion correction handling|ADR-0039]]", "[[ADR-0040 Supported nonbonded methods|ADR-0040]]"]
tasks: ["[[TASK-034 Add same-site exclusions to CHARMM LJ copies|TASK-034]]", "[[TASK-035 Whitelist force types|TASK-035]]", "[[TASK-036 Preserve env-env dispersion correction|TASK-036]]", "[[TASK-037 Read PME alpha from the force|TASK-037]]", "[[TASK-038 Refuse reaction-field cutoff methods|TASK-038]]", "[[TASK-039 Handle zero-mass particles in the integrator|TASK-039]]"]
issues: ["[[ISS-003 Within-block correction wrong for cutoff methods|ISS-003]]", "[[ISS-004 CHARMM NBFIX systems fail on CPU|ISS-004]]", "[[ISS-005 Unsupported force types silently unscaled|ISS-005]]", "[[ISS-007 Dispersion correction removed for the whole system|ISS-007]]", "[[ISS-008 PME alpha recomputed from the tolerance|ISS-008]]", "[[ISS-017 Zero-mass particles break the integrator|ISS-017]]"]
created: 2026-09-27
updated: 2026-09-27
---
# FEAT-047 — Engine hardening (audit fixes)

The small engine fixes from [[AUD-001 Engine audit of the local working copy|AUD-001]]: CHARMM exclusions, force whitelist, dispersion correction,
PME α, supported nonbonded methods, zero-mass particles.
