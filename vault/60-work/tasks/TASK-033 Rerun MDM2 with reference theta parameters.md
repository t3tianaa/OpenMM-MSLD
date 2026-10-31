---
id: TASK-033
type: task
title: Rerun MDM2 with reference theta parameters
status: done
kind: experiment
priority: P0
milestone: M4
feature: "[[FEAT-022 MDM2 test system|FEAT-022]]"
issues: ["[[ISS-018 Theta runs hot in MDM2|ISS-018]]", "[[ISS-002 Theta mass convention differs from BLaDE|ISS-002]]"]
depends_on: ["[[TASK-031 Rebuild atom restraint groups|TASK-031]]", "[[TASK-032 Resolve BLaDE theta units|TASK-032]]"]
refs: ["[[Lambda dynamics integrator component]]"]
created: 2026-09-27
updated: 2026-10-31
---
# TASK-033 — Rerun MDM2 with reference-equivalent θ mass/friction and measure T_θ

Without restraints ([[TASK-031 Rebuild atom restraint groups|TASK-031]]), with the θ mass/friction from [[TASK-032 Resolve BLaDE theta units|TASK-032]] (and atom friction 0.1
ps⁻¹ like BLaDE). Several independent runs from a shared start, long enough for statistics; record
T_θ, λ histograms, transitions. Record as a new EXP. Limit threads/GPU use; ask before long runs.
Decides whether the plugin is needed for thermostatting ([[ADR-0035 Gate plugin work|ADR-0035]]).


**Done (2026-10-31)** as a short screen, not the multi-run statistics asked for (laptop budget): [[EXP-011 MDM2 theta mass and friction screen|EXP-011]]. Atom friction 0.1 ps⁻¹ not tested. θ thermalizes, so the plugin is not needed for thermostatting.
