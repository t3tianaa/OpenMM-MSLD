---
title: Maximum common substructure mapping
type: theory
status: reviewed
related: ["[[Mapping component]]", "[[RDKit MCS]]"]
updated: 2026-09-27
---
# Maximum common substructure (MCS) mapping

The largest subgraph present in every molecule of a series. For relative free energies it defines
the shared core; the rest of each molecule is its perturbed group.

Choices that matter: atom comparison (element only vs atom type), bond comparison (order vs any),
ring rules (`ringMatchesRingOnly`, `completeRingsOnly` keep rings whole), and optional filters
(e.g. core atoms must have identical LJ parameters because MSLD does not scale the core). A core
that cuts through a ring is invalid for MSLD's pendant-substituent model and must be refused.

Tool: RDKit `rdFMCS` ([[RDKit MCS]]).

