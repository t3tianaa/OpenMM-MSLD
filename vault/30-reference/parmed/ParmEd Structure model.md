---
title: ParmEd Structure model
type: reference
status: verified
system: parmed
version: 4.3.1
related: ["[[Ingest component]]", "[[Grafting and term transplant]]"]
updated: 2026-09-27
---
# ParmEd `Structure` model

ParmEd (`parmed` 4.3.1) is a Python library that reads/writes Amber, CHARMM, GROMACS and other
formats into one in-memory `Structure`, and converts it to an OpenMM `System`. Our prep layer uses
it as the common representation ([[ADR-0015 ParmEd Structure as prep common representation|ADR-0015]]).

```
 Structure
  ├─ atoms[]        name, type (string), atom_type (AtomType: LJ ε, Rmin/2, ε14, Rmin14/2, NBFIX),
  │                 charge (e), mass, atomic_number, residue, xx/xy/xz (Å), idx
  ├─ residues[]     name, number, chain, atoms
  ├─ bonds / angles / dihedrals / impropers / urey_bradleys / cmaps / rb_torsions …
  │                 each term references atoms + a *type* object (force constants)
  ├─ bond_types / angle_types / dihedral_types / … (parameter tables, shared by terms)
  ├─ adjusts        1-4 pair exceptions ("adjusts")
  ├─ box            [a, b, c, α, β, γ] in Å / degrees, or None
  └─ createSystem(nonbondedMethod, …) → openmm.System
```

Units: **Å and kcal/mol** inside ParmEd; OpenMM uses nm and kJ/mol — convert at the boundary.

Useful facts (Verified in `parmed/structure.py`):
- `copy.copy(structure)` calls `Structure.__copy__` (line 408) → `copy()` (line 414), a full copy
  of atoms, terms and types — safe to modify the copy.
- `structure_a + structure_b` (`__add__`, line 3578) concatenates, keeping `a`'s indices first —
  used by solvation so solute indices stay stable.
- `has_NBFIX()` (line 1954) decides whether `createSystem` builds a tabulated LJ force.

