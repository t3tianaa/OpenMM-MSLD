---
title: Charge renormalization
type: component
subsystem: "[[Preparation subsystem]]"
layer: L3
status: as-built
code: [msld/prep/assemble/charges.py]
requirements: ["[[REQ-046 Consistent charges across variants|REQ-046]]"]
decisions: ["[[ADR-0021 Charge averaging, renormalization, iso-charge guard|ADR-0021]]"]
updated: 2026-09-27
---
# Charge renormalization

Three jobs (`ChargeRenormalization.apply(structure, mapping, variants)`, in place):

1. **Average env charges.** Each shared atom gets the per-atom mean of its charge across variants
   (Amber RESP charges differ per residue; CHARMM backbone charges already agree). Spread > 0.5 e
   → raise (not really a shared atom).
2. **Renormalize each block** so env + block has an integer net charge: the residual
   `target − raw_net` is spread over the block's atoms equally (`SpreadRenormalizer`, default) or
   by |q| (`ProportionalRenormalizer`). Env charges never change here.
3. **Iso-charge guard.** All variants at a site must reach the **same** integer net charge; else
   raise — charge-changing perturbations are not supported ([[Net charge changes in alchemical calculations]]).

`BufferAwareRenormalizer` tolerates `buffer_atoms` (env atoms allowed per-variant charges) in the
accounting; true per-variant buffer charges would need the buffer atom duplicated into each block
([[TASK-068 Buffer atom duplication|TASK-068]]).

Worked example (from the original notes; env atoms 0, 1; site blocks A = {2, 3}, B = {4}):
![[Pasted image 20260813140304.png|400]]
![[Pasted image 20260813140349.png]]
![[Pasted image 20260813140528.png|400]]
![[Pasted image 20260813140610.png|400]]
![[Pasted image 20260813140628.png]]

Open idea (from the notes): refit charges (RESP) for hybrid cores instead of averaging.

