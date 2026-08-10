"""System builder.

Takes an already constructed OpenMM `System` + `MSLDModel` and return a System
whose energy terms are block-scaled by per-block `lambda{b}`.

Mirrors BLaDE Process 1 (construction): walk each base force, classify every term
by which block-lambda(s) scale it, and route scaled terms to `forces.py`.
"""
from __future__ import annotations

import openmm as mm

from . import forces
from .forces import lambda_name


def lambda_parameter_names(model) -> list[str]:
    """Return names of all non-environment blocks."""
    return [lambda_name(b) for b in range(1, model.n_blocks)]


def set_lambdas(context: mm.Context, lambdas) -> None:
    """Set lambda{b} context globals from a per-block sequence (index 0 = env).

    Only parameters actually registered by some force are set. In a full system
    every block has nonbonded terms (so every lambda{b} exists). In reduced test
    systems a block may have no scaled force, and its lambda is simply absent.
    """
    present = context.getParameters()
    for b in range(1, len(lambdas)):
        name = lambda_name(b)
        if name in present:
            context.setParameter(name, float(lambdas[b]))


def _alchemical_atoms(model) -> set[int]:
    return {a for a, b in enumerate(model.atom_block) if b != 0}


def _check_unhandled(system: mm.System, model) -> None:
    """Raise if a not yet supported force type contains alchemical atoms."""
    alch = _alchemical_atoms(model)
    if not alch:
        return

    def touches(idxs):
        return any(i in alch for i in idxs)

    # Bonded, electrostatics, LJ, and 1-4 exceptions are handled. CMAP is not.
    for f in system.getForces():
        if isinstance(f, mm.CMAPTorsionForce):
            for i in range(f.getNumTorsions()):
                atoms = f.getTorsionParameters(i)[1:]      # (map, a1..a4, b1..b4)
                if any(a in alch for a in atoms):
                    raise NotImplementedError(
                        "CMAP scaling is not implemented; base System has an "
                        "alchemical CMAP torsion")


def build_msld_system(system: mm.System, model, check_unhandled: bool = True) -> dict:
    """Apply MSLD block-scaling to `system` in place.

    Returns an info dict describing what was scaled. Raises (unless
    check_unhandled=False) if unsupported force types carry alchemical atoms.
    """
    if not getattr(model, "_finalized", False):
        raise RuntimeError("call model.finalize() before build_msld_system()")

    info: dict = {"lambda_parameters": lambda_parameter_names(model)}
    # bonded scaling can be turned off per term type (BLaDE "removescaling")
    info["scaled_bond_forces"] = (
        [f.getName() for f in forces.add_scaled_bonds(system, model)]
        if getattr(model, "scale_bond", True) else [])
    info["scaled_angle_forces"] = (
        [f.getName() for f in forces.add_scaled_angles(system, model)]
        if getattr(model, "scale_angle", True) else [])
    info["scaled_torsion_forces"] = (
        [f.getName() for f in forces.add_scaled_torsions(system, model)]
        if getattr(model, "scale_torsion", True) else [])
    nbf = forces.add_scaled_electrostatics(system, model)
    info["scaled_electrostatics"] = (nbf is not None)
    info["scaled_lj_forces"] = [f.getName() for f in forces.add_scaled_lj(system, model)]
    info["scaled_14_exceptions"] = forces.add_scaled_14_exceptions(system, model)
    bias = forces.add_biases(system, model)
    info["bias_force"] = bias.getName() if bias is not None else None
    restr = forces.add_atom_restraints(system, model)
    info["atom_restraint_force"] = restr.getName() if restr is not None else None

    if check_unhandled:
        _check_unhandled(system, model)

    return info
