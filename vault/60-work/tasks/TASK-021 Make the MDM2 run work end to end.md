---
id: TASK-021
type: task
title: Make the MDM2 run work end to end
status: done
kind: fix
priority: P0
milestone: M3
feature: "[[FEAT-022 MDM2 test system|FEAT-022]]"
issues: ["[[ISS-022 Ingest does not validate geometry|ISS-022]]"]
created: 2026-09-15
done: 2026-09-15
retrospective: true
---
# TASK-021 — Make the MDM2 run work end to end

Empty metrics → causes: corrupt OXT coordinate, no minimization, stiff θ. Fixes: corrected the PDB,
added `LambdaDynamics.minimize`, switched to OpenCL (380× faster than Reference), made exclusions
identical across nonbonded forces (CPU/OpenCL), turned bond/angle scaling off in the script
([[EXP-007 MDM2 first end-to-end run and benchmark|EXP-007]]).

