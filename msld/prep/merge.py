"""Merge per-variant topologies into one combined topology with ParmEd.

Input: for each variant, a ParmEd `Structure` that already contains the shared
environment + that one variant's block, fully parametrized and co-framed (same
coordinates for the shared atoms). We take the first variant as the base (it already
holds env + block0 + all their bonded terms), then for every other variant we:

  * map its env atoms onto the base env atoms (by position in `env_indices`),
  * append its block atoms as new atoms,
  * copy over only the bonded terms that touch one of its block atoms.

Because every input holds exactly one variant, a bonded term connecting two different
variants can never appear.

The result carries a `CoreMapping` whose indices are already in the combined system, so
it feeds straight into `model_from_mappings`.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field

import parmed as pmd

from .charges import average_env_charges
from .mapping import CoreMapping


@dataclass
class VariantInput:
    """One variant to merge.

    name         : variant label (becomes the block name).
    structure    : ParmEd Structure = shared env + this variant's block.
    env_indices  : atom indices in `structure` that are the shared environment, in a
                   fixed order. Position i must mean the same shared atom in every
                   variant (that is how env atoms correspond across variants).
    """
    name: str
    structure: "pmd.Structure"
    env_indices: list[int]

    def block_indices(self) -> list[int]:
        env = set(self.env_indices)
        return [i for i in range(len(self.structure.atoms)) if i not in env]


@dataclass
class MergeResult:
    structure: "pmd.Structure"          # the combined topology
    mapping: CoreMapping                 # env/blocks in combined indices
    index_maps: dict = field(default_factory=dict)   # variant name -> {src idx: combined idx}
    env_charge_report: object = None     # EnvChargeReport, if env charges were averaged


# helpers
def _term_atoms(term):
    """Atoms referenced by a ParmEd bonded term (2 to 5 of them)."""
    out = []
    for attr in ("atom1", "atom2", "atom3", "atom4", "atom5"):
        a = getattr(term, attr, None)
        if a is not None:
            out.append(a)
    return out


def _copy_atom(src) -> "pmd.Atom":
    """A fresh ParmEd Atom copying src's identity, charge, mass, LJ and coordinates."""
    a = pmd.Atom(atomic_number=src.atomic_number, name=src.name, type=src.type,
                 charge=src.charge, mass=src.mass)
    # LJ: atom_type carries rmin/epsilon; also copy sigma/epsilon/rmin defensively
    a.atom_type = src.atom_type
    for attr in ("sigma", "epsilon", "rmin", "rmin_14", "epsilon_14"):
        val = getattr(src, attr, None)
        if val is not None:
            try:
                setattr(a, attr, val)
            except (AttributeError, TypeError):
                pass
    a.xx, a.xy, a.xz = src.xx, src.xy, src.xz
    return a


class _TypeCache:
    """Copies a variant's parameter-type objects into the base's type lists once each."""
    def __init__(self):
        self._seen: dict[int, object] = {}

    def get(self, t, base_list):
        if t is None:
            return None
        key = id(t)
        if key not in self._seen:
            nt = copy.copy(t)          # detach from the source structure
            base_list.append(nt)
            self._seen[key] = nt
        return self._seen[key]


def _touches_block(atoms, block_src: set[int]) -> bool:
    return any(a.idx in block_src for a in atoms)


# merge
def merge_variants(variants: list[VariantInput], *,
                   average_env: bool = True) -> MergeResult:
    """Merge per-variant Structures into one combined Structure + CoreMapping.

    average_env : give each shared env atom the per-atom average charge across the
                  variants (default on). 
                  Emits a message when charges differ. See charges.average_env_charges.
    """
    if len(variants) < 1:
        raise ValueError("need at least one variant")

    base = copy.copy(variants[0].structure)   # ParmEd copy: deep-copies atoms/terms/types
    v0 = variants[0]
    combined_env = list(v0.env_indices)        # env atom indices in the base (unchanged)

    blocks: dict[str, set[int]] = {}
    index_maps: dict[str, dict[int, int]] = {}

    # variant 0: its block atoms already sit in the base; just record them
    blocks[v0.name] = set(v0.block_indices())
    index_maps[v0.name] = {i: i for i in range(len(v0.structure.atoms))}

    for var in variants[1:]:
        cache = _TypeCache()
        env = set(var.env_indices)
        block_src = set(var.block_indices())

        # atom index map: source idx -> combined (base) idx
        amap: dict[int, int] = {}
        for i, e in enumerate(var.env_indices):
            amap[e] = combined_env[i]          # env atoms map onto base env atoms

        # append this variant's block atoms as new atoms
        new_block: set[int] = set()
        for si in var.block_indices():
            src = var.structure.atoms[si]
            new_atom = _copy_atom(src)
            base.add_atom(new_atom, var.name, len(base.residues) + 1)
            amap[si] = new_atom.idx
            new_block.add(new_atom.idx)
        blocks[var.name] = new_block
        index_maps[var.name] = amap

        # copy only the bonded terms that touch a block atom, re-indexed
        _transplant_terms(base, var.structure, amap, block_src, cache)

    # give the shared env atoms the per-atom average charge across variants
    report = None
    if average_env and len(variants) > 1:
        per_variant = [[var.structure.atoms[e].charge for e in var.env_indices]
                       for var in variants]
        labels = [base.atoms[combined_env[i]].name for i in range(len(combined_env))]
        report = average_env_charges(per_variant, labels=labels)
        for i, q in enumerate(report.averaged):
            base.atoms[combined_env[i]].charge = q

    mapping = CoreMapping(env_atoms=set(combined_env), blocks=blocks).validate()
    return MergeResult(structure=base, mapping=mapping, index_maps=index_maps,
                       env_charge_report=report)


def _transplant_terms(base, src, amap, block_src, cache):
    """Copy src's block-touching bonded terms into base, remapping atom indices."""
    def A(term_atom):                          # source atom -> base atom object
        return base.atoms[amap[term_atom.idx]]

    # bonds
    for b in src.bonds:
        if _touches_block([b.atom1, b.atom2], block_src):
            t = cache.get(b.type, base.bond_types)
            base.bonds.append(pmd.Bond(A(b.atom1), A(b.atom2), type=t))

    # angles
    for ang in src.angles:
        ats = [ang.atom1, ang.atom2, ang.atom3]
        if _touches_block(ats, block_src):
            t = cache.get(ang.type, base.angle_types)
            base.angles.append(pmd.Angle(A(ats[0]), A(ats[1]), A(ats[2]), type=t))

    # proper + improper (periodic) dihedrals
    for d in src.dihedrals:
        ats = [d.atom1, d.atom2, d.atom3, d.atom4]
        if _touches_block(ats, block_src):
            t = cache.get(d.type, base.dihedral_types)
            base.dihedrals.append(pmd.Dihedral(
                A(ats[0]), A(ats[1]), A(ats[2]), A(ats[3]),
                improper=d.improper, ignore_end=d.ignore_end, type=t))

    # Urey-Bradley (CHARMM 1-3)
    for ub in getattr(src, "urey_bradleys", []):
        if _touches_block([ub.atom1, ub.atom2], block_src):
            t = cache.get(ub.type, base.urey_bradley_types)
            base.urey_bradleys.append(pmd.UreyBradley(A(ub.atom1), A(ub.atom2), type=t))

    # harmonic impropers (CHARMM)
    for imp in getattr(src, "impropers", []):
        ats = [imp.atom1, imp.atom2, imp.atom3, imp.atom4]
        if _touches_block(ats, block_src):
            t = cache.get(imp.type, base.improper_types)
            base.impropers.append(pmd.Improper(
                A(ats[0]), A(ats[1]), A(ats[2]), A(ats[3]), type=t))

    # CMAP (CHARMM backbone cross-term)
    for cm in getattr(src, "cmaps", []):
        ats = _term_atoms(cm)
        if _touches_block(ats, block_src):
            t = cache.get(cm.type, base.cmap_types)
            base.cmaps.append(pmd.Cmap(*[A(a) for a in ats], type=t))

    # 1-4 exceptions ("adjusts"): the scaled 1-4 pairs. These are not rederived by
    # createSystem when there are no dihedrals, so they must be transplanted, or the
    # env<->block 1-4 pair would wrongly become a full interaction.
    for adj in getattr(src, "adjusts", []):
        if _touches_block([adj.atom1, adj.atom2], block_src):
            t = cache.get(adj.type, base.adjust_types)
            base.adjusts.append(pmd.NonbondedException(A(adj.atom1), A(adj.atom2), type=t))
