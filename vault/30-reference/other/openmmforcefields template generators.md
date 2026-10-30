---
title: openmmforcefields template generators
type: reference
status: verified
system: openmmforcefields
version: env msld
related: ["[[Ingest component]]"]
updated: 2026-09-27
---
# openmmforcefields template generators

`GAFFTemplateGenerator(molecules=…, forcefield="gaff-2.11")` and
`SMIRNOFFTemplateGenerator(molecules=…, forcefield="openff-2.2.0")` create residue templates on the
fly for small molecules given as `openff.toolkit.Molecule` (read from SDF). Register with
`ForceField.registerTemplateGenerator(gen.generator)`. GAFF computes AM1-BCC charges with AmberTools
`antechamber`/`sqm` (must be on PATH; our code prepends the env `bin/`). Heavy import (~1.5 s incl.
PyTorch), so we import it lazily ([[ADR-0030 Hard dependencies and a ParmEd-free engine|ADR-0030]]).
