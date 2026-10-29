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

# dU/dlambda is a hybrid: analytic where OpenMM can expose it, finite difference where it
# cannot. We split the forces into two groups so the integrator can do exactly that:
#   ANALYTIC_FORCE_GROUP : every force that registered a dU/dlambda_b via
#                          addEnergyParameterDerivative (bonded, LJ, soft-core and within-block
#                          elec corrections, biases). Their derivative comes back for free from
#                          getState.
#   group 0 (the default): everything else that depends on lambda -- the base
#                          NonbondedForce (charge-scaling electrostatics, which OpenMM cannot
#                          expose; exactly quadratic in each lambda), and ANY force a caller
#                          injects after building (e.g. ALF test offsets). The integrator
#                          finite-differences THIS group alone, so nothing lambda-dependent
#                          is ever dropped. lambda-independent env forces also sit here and
#                          simply contribute 0 to the FD.
# Group assignment changes no energy or force -- only which getState query sees a force.
ANALYTIC_FORCE_GROUP = 1
FD_FORCE_GROUP = 0


def _split_force_groups(system: mm.System) -> None:
    """Move every force that exposes an analytic dU/dlambda into ANALYTIC_FORCE_GROUP;
    leave the finite-difference remainder (electrostatics, biases, injected, env) in group 0."""
    for i in range(system.getNumForces()):
        f = system.getForce(i)
        getn = getattr(f, "getNumEnergyParameterDerivatives", None)
        if getn is not None and getn() > 0:
            f.setForceGroup(ANALYTIC_FORCE_GROUP)
        else:
            f.setForceGroup(FD_FORCE_GROUP)


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


def set_biases(context: mm.Context, model) -> None:
    """Push the model's bias coefficients into the Context globals (the ALF update step).

    Mirrors `set_lambdas`: only globals a force actually registered are set. The fixed linear bias
    of block b lives in `biascoef{b}` (from `Block.lambda_bias`); the m-th variable bias' strength in
    `biask{m}` (from `VariableBias.k`). Requires the bias force to exist -- build the System with
    `model.bias_flattening = True` (or with non-zero biases) so those globals are present.
    """
    present = context.getParameters()
    for b in range(1, model.n_blocks):
        name = forces.bias_coef_name(b)
        if name in present:
            context.setParameter(name, float(model.blocks[b].lambda_bias))
    for m, vb in enumerate(model.variable_biases):
        name = forces.variable_bias_k_name(m)
        if name in present:
            context.setParameter(name, float(vb.k))


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


def scale_msld_system(system: mm.System, model, check_unhandled: bool = True) -> dict:
    """Apply MSLD block-scaling to `system` in place.

    Returns an info dict describing what was scaled. Raises (unless
    check_unhandled=False) if unsupported force types carry alchemical atoms.
    """
    if not getattr(model, "_finalized", False):
        raise RuntimeError("call model.finalize() before scale_msld_system()")

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
    # CHARMM harmonic impropers (CustomTorsionForce)
    info["scaled_improper_forces"] = (
        [f.getName() for f in forces.add_scaled_impropers(system, model)]
        if getattr(model, "scale_torsion", True) else [])
    # within-block electrostatics correction (lambda, not lambda^2) — reads RAW charges,
    # so it must run BEFORE add_scaled_electrostatics zeroes them
    info["within_block_elec_corrections"] = [
        f.getName() for f in forces.add_within_block_elec_correction(system, model)]
    # raw charges, read before add_scaled_electrostatics moves them into lambda offsets
    nbfs = [f for f in system.getForces() if isinstance(f, mm.NonbondedForce)]
    raw_q = ([nbfs[0].getParticleParameters(i)[0].value_in_unit(forces._E)
              for i in range(system.getNumParticles())] if nbfs else [])
    nbf = forces.add_scaled_electrostatics(system, model)
    info["scaled_electrostatics"] = (nbf is not None)
    info["scaled_lj_forces"] = [f.getName() for f in forces.add_scaled_lj(system, model)]
    # soft-core direct-space Coulomb for overlap-prone pairs (no-op if model.softcore_alpha == 0)
    info["softcore_elec_forces"] = [
        f.getName() for f in forces.add_softcore_electrostatics(system, model, raw_q)]
    # CHARMM tabulated LJ (NBFIX -> CustomNonbondedForce); no-op on Amber
    info["scaled_charmm_lj_forces"] = [
        f.getName() for f in forces.add_scaled_charmm_lj(system, model)]
    info["scaled_14_exceptions"] = forces.add_scaled_14_exceptions(system, model)
    bias = forces.add_biases(system, model)
    info["bias_force"] = bias.getName() if bias is not None else None
    restr = forces.add_atom_restraints(system, model)
    info["atom_restraint_force"] = restr.getName() if restr is not None else None

    # split analytic vs finite-difference forces for the integrator's dU/dlambda
    _split_force_groups(system)

    if check_unhandled:
        _check_unhandled(system, model)

    return info
