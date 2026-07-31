"""Block-scaled force construction.

The problem: OpenMM's built-in bond/angle/torsion forces use a fixed energy
formula, so you cannot multiply them by a lambda.

The fix: for every term that a substituent's lambda should scale, take it out of
the built-in force and re-add it to a CustomForce whose energy formula carries
that lambda as a factor, e.g.  lambda1 * 0.5*k*(r-r0)^2. Block b's coupling is a
global parameter named lambda{b}, shared by all of that block's terms. We also
ask OpenMM to track dU/dlambda{b} (addEnergyParameterDerivative).

Convention: block b's coupling is the Context global parameter  lambda{b}
(e.g. "lambda1"). The environment (block 0) is never scaled and never gets one.

Implemented (bonded family, bilinear scaling = product of the <=2 block lambdas
whose atoms appear in the term):
  add_scaled_bonds     : HarmonicBondForce    -> CustomBondForce(s)
  add_scaled_angles    : HarmonicAngleForce   -> CustomAngleForce(s)
  add_scaled_torsions  : PeriodicTorsionForce -> CustomTorsionForce(s)

Planned (nonbonded):
  electrostatics + PME via NonbondedForce parameter offsets
  LJ scaling + same-site rule via CustomNonbondedForce
  fixed + variable (ALF) biases
"""
from __future__ import annotations

from collections import defaultdict

import openmm as mm
from openmm import unit

_NM = unit.nanometer
_RAD = unit.radian
_KJ = unit.kilojoule_per_mole
_KJ_PER_NM2 = _KJ / _NM**2
_KJ_PER_RAD2 = _KJ / _RAD**2


# --------------------------------------------------------------------- 
# Helpers 
# --------------------------------------------------------------------- 
def lambda_name(b: int) -> str:
    """Context global-parameter name for block b's coupling."""
    # block 1 -> "lambda1"
    return f"lambda{b}"


def _forces_of_type(system: mm.System, cls):
    """Return all forces of a given type in a System."""
    return [system.getForce(i) for i in range(system.getNumForces())
            if isinstance(system.getForce(i), cls)]


def _lambda_prefix(signature: tuple[int, ...]) -> str:
    """'lambda1' or 'lambda1*lambda3' etc. for the energy expression."""
    return "*".join(lambda_name(b) for b in signature)


def _register_lambdas(force, signature: tuple[int, ...]) -> None:
    """Declare block's global parameter and request its energy derivative."""
    for b in signature:
        force.addGlobalParameter(lambda_name(b), 1.0)       # declare the global (default 1.0)
        force.addEnergyParameterDerivative(lambda_name(b))  # dU/dlambda_b


# --------------------------------------------------------------------- 
# Bonds 
# --------------------------------------------------------------------- 
def add_scaled_bonds(system: mm.System, model) -> list[mm.CustomBondForce]:
    """HarmonicBondForce -> block-scaled CustomBondForce(s)."""
    created = []
    for hbf in _forces_of_type(system, mm.HarmonicBondForce):
        groups = defaultdict(list)
        # Classify each bond, and remove the scaled ones from the base force
        for i in range(hbf.getNumBonds()):
            p1, p2, length, k = hbf.getBondParameters(i)    # read bond i
            sig = tuple(model.classify_bonded([p1, p2]))    # which λ's scale it?
            if not sig:
                continue    # env-only -> keep in base force
            groups[sig].append((p1, p2, length.value_in_unit(_NM),
                                k.value_in_unit(_KJ_PER_NM2)))
            hbf.setBondParameters(i, p1, p2, length, 0.0 * k)   # zero it in the base force

        # build one CustomBondForce per signature
        for sig, bonds in groups.items():
            f = mm.CustomBondForce(f"{_lambda_prefix(sig)}*0.5*k*(r-length)^2")
            f.setName("MSLDBond_" + "_".join(map(str, sig)))
            _register_lambdas(f, sig)
            f.addPerBondParameter("length")
            f.addPerBondParameter("k")
            for p1, p2, length, k in bonds:
                f.addBond(p1, p2, [length, k])
            system.addForce(f)
            created.append(f)
    return created


# --------------------------------------------------------------------- 
# Angles 
# --------------------------------------------------------------------- 
def add_scaled_angles(system: mm.System, model) -> list[mm.CustomAngleForce]:
    """HarmonicAngleForce -> block-scaled CustomAngleForce(s)."""
    created = []
    for haf in _forces_of_type(system, mm.HarmonicAngleForce):
        groups = defaultdict(list)
        for i in range(haf.getNumAngles()):
            a1, a2, a3, angle, k = haf.getAngleParameters(i)
            sig = tuple(model.classify_bonded([a1, a2, a3]))
            if not sig:
                continue
            groups[sig].append((a1, a2, a3, angle.value_in_unit(_RAD),
                                k.value_in_unit(_KJ_PER_RAD2)))
            haf.setAngleParameters(i, a1, a2, a3, angle, 0.0 * k)
        for sig, angles in groups.items():
            f = mm.CustomAngleForce(f"{_lambda_prefix(sig)}*0.5*k*(theta-theta0)^2")
            f.setName("MSLDAngle_" + "_".join(map(str, sig)))
            _register_lambdas(f, sig)
            f.addPerAngleParameter("theta0")
            f.addPerAngleParameter("k")
            for a1, a2, a3, theta0, k in angles:
                f.addAngle(a1, a2, a3, [theta0, k])
            system.addForce(f)
            created.append(f)
    return created


# --------------------------------------------------------------------- 
# Torsions 
# --------------------------------------------------------------------- 
def add_scaled_torsions(system: mm.System, model) -> list[mm.CustomTorsionForce]:
    """PeriodicTorsionForce -> block-scaled CustomTorsionForce(s)."""
    created = []
    for ptf in _forces_of_type(system, mm.PeriodicTorsionForce):
        groups = defaultdict(list)
        for i in range(ptf.getNumTorsions()):
            a1, a2, a3, a4, per, phase, k = ptf.getTorsionParameters(i)
            sig = tuple(model.classify_bonded([a1, a2, a3, a4]))
            if not sig:
                continue
            groups[sig].append((a1, a2, a3, a4, int(per),
                                phase.value_in_unit(_RAD), k.value_in_unit(_KJ)))
            ptf.setTorsionParameters(i, a1, a2, a3, a4, per, phase, 0.0 * k)
        for sig, tors in groups.items():
            f = mm.CustomTorsionForce(
                f"{_lambda_prefix(sig)}*k*(1+cos(per*theta-phase))")
            f.setName("MSLDTorsion_" + "_".join(map(str, sig)))
            _register_lambdas(f, sig)
            f.addPerTorsionParameter("per")
            f.addPerTorsionParameter("phase")
            f.addPerTorsionParameter("k")
            for a1, a2, a3, a4, per, phase, k in tors:
                f.addTorsion(a1, a2, a3, a4, [per, phase, k])
            system.addForce(f)
            created.append(f)
    return created
