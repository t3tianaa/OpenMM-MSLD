---
title: Thermodynamic cycles for relative free energies
type: theory
status: reviewed
related: ["[[Alchemical free energy basics]]", "[[Free energies from lambda populations]]"]
updated: 2026-09-27
---
# Thermodynamic cycles for relative free energies

**In one sentence.** A measurable ΔΔG (binding or folding) is the difference of two alchemical
ΔG's computed in two environments.

```
            ΔG_bind(A)
   P + A ─────────────▶ P·A
     │                    │
     │ ΔG_solv(A→B)       │ ΔG_complex(A→B)        (alchemical, simulated)
     ▼                    ▼
   P + B ─────────────▶ P·B
            ΔG_bind(B)

   ΔΔG_bind(A→B) = ΔG_bind(B) − ΔG_bind(A) = ΔG_complex(A→B) − ΔG_solv(A→B)
```

- Binding: legs = bound complex, free ligand (or free peptide) in water.
- Folding / stability: legs = folded protein, unfolded reference (often a short capped peptide).

For MSLD every leg is one simulation that samples all variants; ΔG_leg(A→B) = G_leg(B) − G_leg(A)
([[Free energies from lambda populations]]). The biases need not be the same in the two legs,
because each leg subtracts its own bias.

**Why it matters for us.** `alf.estimate_ddg` today returns a single-environment ΔG and calls it
ΔΔG ([[ISS-011 ALF is a heuristic and ddG is single-leg|ISS-011]]). The analysis subsystem must implement the two-leg cycle ([[REQ-061 Relative ddG from two legs|REQ-061]]).

![[Pasted image 20260714160342.png|500]]
*(figure kept from the original notes)*

