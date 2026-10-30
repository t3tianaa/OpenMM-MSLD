---
id: FEAT-001
type: feature
title: MSLD data model
status: done
milestone: M1
implements: ["[[REQ-001 Represent sites, blocks and environment|REQ-001]]", "[[REQ-002 Lambda from theta with implicit constraints|REQ-002]]"]
components: ["[[MSLD model component]]"]
decisions: ["[[ADR-0005 Lambda as softmax of fnex sin theta|ADR-0005]]"]
tasks: ["[[TASK-003 Implement the MSLD data model|TASK-003]]"]
issues: ["[[ISS-019 Fixed-block lambda semantics differ from BLaDE|ISS-019]]"]
created: 2026-07-27
updated: 2026-09-27
retrospective: true
---
# FEAT-001 — MSLD data model

Sites, blocks, θ state, softmax, term classifiers, biases and restraint lists in pure Python
(`msld/model.py`), mirroring BLaDE's `Msld`. Done; small gaps in fixed-block semantics
([[ISS-019 Fixed-block lambda semantics differ from BLaDE|ISS-019]]) and θ units ([[ISS-002 Theta mass convention differs from BLaDE|ISS-002]]).

