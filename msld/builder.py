"""System builder.

Takes an already constructed OpenMM `System` + `MSLDModel` and return a System
whose energy terms are block-scaled by per-block `lambda{b}`.

Mirrors BLaDE Process 1 (construction): walk each base force, classify every term
by which block-lambda(s) scale it, and route scaled terms to `forces.py`.

Currently handled:  HarmonicBondForce, HarmonicAngleForce, PeriodicTorsionForce.
Not yet handled  :  nonbonded / PME. The builder RAISES if it finds alchemical
                    atoms in a NonbondedForce, so it never silently produces a
                    wrong (partially-scaled) System.
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

    for f in system.getForces():
        if isinstance(f, mm.NonbondedForce):
            for i in alch:
                q, sig, eps = f.getParticleParameters(i)
                if q._value != 0.0 or eps._value != 0.0:
                    raise NotImplementedError(
                        "nonbonded/PME scaling is not implemented yet; base System "
                        "has alchemical nonbonded particles")


def build_msld_system(system: mm.System, model, check_unhandled: bool = True) -> dict:
    """Apply MSLD block-scaling to `system` in place.

    Returns an info dict describing what was scaled. Raises (unless
    check_unhandled=False) if unsupported force types carry alchemical atoms.
    """
    if not getattr(model, "_finalized", False):
        raise RuntimeError("call model.finalize() before build_msld_system()")

    info: dict = {"lambda_parameters": lambda_parameter_names(model)}
    info["scaled_bond_forces"] = [f.getName() for f in forces.add_scaled_bonds(system, model)]
    info["scaled_angle_forces"] = [f.getName() for f in forces.add_scaled_angles(system, model)]
    info["scaled_torsion_forces"] = [f.getName() for f in forces.add_scaled_torsions(system, model)]

    if check_unhandled:
        _check_unhandled(system, model)

    return info
