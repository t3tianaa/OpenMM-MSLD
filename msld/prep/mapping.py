"""Site-level alchemical mapping (`CoreMapping`) and its producers (`CoreMapper`).

An MSLD specification is, per site, a partition of particle indices into a shared
environment and a set of mutually-exclusive variant blocks. `CoreMapping` is the
canonical, force-field-agnostic representation of that partition for a single site:

    env_atoms    : indices shared by all variants (unscaled, instantiated once)
    blocks       : ordered {variant_name: indices}; one block == one lambda DOF
    attachments  : env->block boundary bonds. A list, since ring-closing residues
                   (e.g. proline) cross the boundary more than once
    align_xform  : per-variant rigid transform into the shared frame (optional)
    core_charges : fixed reference charge per env atom 
    buffer_atoms : env atoms permitted a per-variant charge (subset of env_atoms)

Producers implement the `CoreMapper` protocol (`build_mapping() -> CoreMapping`). This
decouples correspondence discovery - name/topology-based for peptides, maximum common
substructure for small molecules, explicit for `ManualMapper` - from the downstream
pipeline (charge renormalization, topology merge, `MSLDModel` assembly), which depends
only on `CoreMapping`.

A multi-site system is an ordered sequence of `CoreMapping`s indexed by site (1..N).
`model_from_mappings` assembles them into a finalized `MSLDModel`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

from ..model import MSLDModel


# ---------------------------------------------------------------------
# The shared data structure
# ---------------------------------------------------------------------
@dataclass
class CoreMapping:
    """Description of one site's alchemical partition.

    Particle indices are 0-based and refer to the target OpenMM System.

    env_atoms    : indices shared by all variants; instantiated once, never
                   lambda-scaled.
    blocks       : ordered {variant_name: indices}; each entry is one block == one
                   lambda DOF. Dict insertion order fixes block ordering within the site.
    attachments  : env->block boundary bonds as (env_atom, block_atom) pairs. A list,
                   since a variant may cross the boundary more than once (e.g. proline).
    align_xform  : {variant_name: rigid transform} placing each variant's coordinates
                   into the shared frame; empty when coordinates are already co-framed.
    core_charges : {env_atom: reference charge}.
    buffer_atoms : env atoms permitted a per-variant charge (subset of env_atoms).
    """
    env_atoms: set[int]
    blocks: dict[str, set[int]]
    attachments: list[tuple[int, int]] = field(default_factory=list)
    align_xform: dict[str, "object"] = field(default_factory=dict)
    core_charges: dict[int, float] = field(default_factory=dict)
    buffer_atoms: set[int] = field(default_factory=set)

    # helpers
    @property
    def block_names(self) -> list[str]:
        """Variant names in order within the site."""
        return list(self.blocks.keys())

    def all_block_atoms(self) -> set[int]:
        """Every atom that belongs to some block at this site."""
        out: set[int] = set()
        for atoms in self.blocks.values():
            out |= atoms
        return out

    # validation 
    def validate(self) -> "CoreMapping":
        """Check the mapping is internally consistent. Raises ValueError if not.

        Rejects malformed partitions before they reach the MSLDModel: empty
        blocks, a negative index, an index assigned to two blocks, env/block overlap,
        attachments referencing an unknown env or block atom, and a buffer_atoms set
        not contained in env_atoms. Returns self, to allow fluent use.
        """
        if not self.blocks:
            raise ValueError("CoreMapping has no blocks (a site needs >= 1 variant)")

        # blocks non-empty, and no atom shared between two blocks
        owner: dict[int, str] = {}
        for name, atoms in self.blocks.items():
            if not atoms:
                raise ValueError(f"block '{name}' has no atoms")
            for a in atoms:
                if a < 0:
                    raise ValueError(f"block '{name}' has negative atom index {a}")
                if a in owner:
                    raise ValueError(
                        f"atom {a} is in two blocks: '{owner[a]}' and '{name}'")
                owner[a] = name

        # env and blocks must not overlap
        overlap = self.env_atoms & set(owner)
        if overlap:
            raise ValueError(
                f"atoms {sorted(overlap)} are in BOTH the environment and a block")

        # attachments must connect a real env atom to a real block atom
        block_atoms = set(owner)
        for e, b in self.attachments:
            if e not in self.env_atoms:
                raise ValueError(f"attachment env atom {e} is not in env_atoms")
            if b not in block_atoms:
                raise ValueError(f"attachment block atom {b} is not in any block")

        # buffer atoms must be part of the environment
        if not self.buffer_atoms <= self.env_atoms:
            bad = sorted(self.buffer_atoms - self.env_atoms)
            raise ValueError(f"buffer_atoms {bad} are not in env_atoms")
        return self


# ---------------------------------------------------------------------
# CoreMapper protocol
# ---------------------------------------------------------------------
@runtime_checkable
class CoreMapper(Protocol):
    """Interface for the mappers that build a CoreMapping.

    A mapper decides, for one site, which particles are the shared environment and
    which form each variant block, and returns that as a validated CoreMapping via
    `build_mapping()`. Implementations differ only in how they find the split:
        ManualMapper           - indices supplied explicitly
        PeptideBackboneMapper  - matched by atom name / topology   
        MCSMapper              - maximum common substructure        
    The rest of the pipeline consumes CoreMapping only, so it never depends on which
    mapper produced it.
    """
    def build_mapping(self) -> CoreMapping: ...


# ---------------------------------------------------------------------
# The simplest mapper: atoms given explicitly
# ---------------------------------------------------------------------
@dataclass
class ManualMapper:
    """Mapper for a predefined split.

    The environment/block assignment is supplied directly rather than inferred.
    Primary uses: deterministic test fixtures, and an override path when the automatic
    mappers are unsuitable. build_mapping() copies the inputs and validates them.
    """
    env_atoms: set[int]
    blocks: dict[str, set[int]]
    attachments: list[tuple[int, int]] = field(default_factory=list)
    core_charges: dict[int, float] = field(default_factory=dict)
    buffer_atoms: set[int] = field(default_factory=set)

    def build_mapping(self) -> CoreMapping:
        mapping = CoreMapping(
            env_atoms=set(self.env_atoms),
            blocks={name: set(atoms) for name, atoms in self.blocks.items()},
            attachments=list(self.attachments),
            core_charges=dict(self.core_charges),
            buffer_atoms=set(self.buffer_atoms),
        )
        return mapping.validate()


# ---------------------------------------------------------------------
# CoreMapping(s) -> MSLDModel
# ---------------------------------------------------------------------
def model_from_mappings(n_atoms: int, mappings, *, fnex: float = 5.5,
                        add_restraints: bool = True,
                        block_options: dict | None = None) -> MSLDModel:
    """Assemble an ordered sequence of per-site CoreMappings into a finalized MSLDModel.

    Site indexing: mappings[k] becomes site k+1. Site 0 / block 0 is the non-alchemical
    environment, it is never declared. Blocks are registered in site order, then variant
    order, since MSLDModel requires blocks added under consecutive, non-decreasing site
    indices.

    Only block atoms are assigned. Every particle not placed in a block stays in block 0
    (full strength, never lambda-scaled) - this includes the rest of the protein and all
    explicit solvent and ions.

    CATS centroid restraints are added per block when `add_restraints` is set. A
    single-atom block is skipped: the restraint is realized as pairwise harmonic terms
    and is undefined for fewer than two atoms.

    `block_options` maps a variant name to extra Block keyword arguments (theta0,
    theta_mass, theta_friction, lambda_bias, fixed), unspecified blocks use defaults.

    Returns the model after finalize(), which additionally enforces MSLDModel's own
    invariants (consecutive site indices, >= 2 blocks per site unless a single fixed
    block, contiguous per-site block ranges).
    """
    # accept a single mapping or a list
    if isinstance(mappings, CoreMapping):
        mappings = [mappings]
    mappings = list(mappings)
    if not mappings:
        raise ValueError("need at least one CoreMapping (one site)")
    block_options = block_options or {}

    model = MSLDModel(n_atoms, fnex=fnex)

    # add all blocks of site 1, then site 2, ... (consecutive-site order required)
    for site_index, mapping in enumerate(mappings, start=1):
        mapping.validate()
        for name in mapping.block_names:
            atoms = sorted(mapping.blocks[name])
            model.add_block(site=site_index, atoms=atoms,
                            **block_options.get(name, {}))

    # CATS restraints: keep each block near its own centroid (skip single-atom blocks)
    if add_restraints:
        for mapping in mappings:
            for name in mapping.block_names:
                atoms = sorted(mapping.blocks[name])
                if len(atoms) >= 2:
                    model.add_atom_restraint(atoms)

    return model.finalize()
