"""1-4 exception block-scaling.

A 1-4 exception's chargeProd and epsilon are scaled by a single block lambda via
NonbondedForce exception parameter offsets (linear -> exact). Derivative is
finite-difference (NonbondedForce), like the rest of electrostatics.
"""
import os
import sys

import openmm as mm
from openmm import unit, Vec3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.model import MSLDModel
from msld.builder import build_msld_system, set_lambdas

_REF = mm.Platform.getPlatform("Reference")


def _energy(system, positions, lambdas=None):
    integ = mm.VerletIntegrator(0.001)
    ctx = mm.Context(system, integ, _REF)
    ctx.setPositions(positions)
    if lambdas is not None:
        set_lambdas(ctx, lambdas)
    return ctx.getState(getEnergy=True).getPotentialEnergy().value_in_unit(
        unit.kilojoule_per_mole)


def _fd_dUdlambda(system, pos, base_lams, block, h=1e-4):
    lp = list(base_lams); lp[block] += h
    lm = list(base_lams); lm[block] -= h
    return (_energy(system, pos, lp) - _energy(system, pos, lm)) / (2 * h)


def test_14_single_lambda():
    # atoms 0(env), 1(block1), 2(block2); ONE 1-4 exception on pair (0,1).
    # particle charges/eps are 0, so the only energy is that exception.
    system = mm.System()
    nbf = mm.NonbondedForce()
    nbf.setNonbondedMethod(mm.NonbondedForce.NoCutoff)
    for _ in range(3):
        system.addParticle(12.0)
        nbf.addParticle(0.0, 0.3, 0.0)
    nbf.addException(0, 1, 0.7, 0.3, 0.5)          # chargeProd, sigma, epsilon14
    system.addForce(nbf)
    pos = [Vec3(0, 0, 0), Vec3(0.35, 0, 0), Vec3(1.5, 0, 0)] * unit.nanometer

    m = MSLDModel(3)
    m.add_block(site=1, atoms=[1])                 # (0,1) -> env<->block1 -> single lambda1
    m.add_block(site=1, atoms=[2])
    m.finalize()
    build_msld_system(system, m)

    e1 = _energy(system, pos, [1.0, 1.0, 1.0])
    assert abs(e1) > 1e-6, e1
    ep = _energy(system, pos, [1.0, 0.4, 1.0])
    assert abs(ep - 0.4 * e1) < 1e-6 * abs(e1), (ep, 0.4 * e1)
    fd = _fd_dUdlambda(system, pos, [1.0, 0.4, 1.0], 1)
    assert abs(fd - e1) < 1e-3 * abs(e1), (fd, e1)     # dU/dlambda1 = E1


def test_14_recovers_base():
    # chain 0-1-2-3-4-5 (bonds) -> exclusions + 1-4 exceptions via createExceptionsFromBonds.
    # block1={4,5} (site1), block2={6} (LJ/charge inert); atoms 0-3 env.
    charges = [1.0, -1.0, 1.0, -1.0, 0.5, -0.5, 0.0]   # net 0
    eps = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0]
    system = mm.System()
    nbf = mm.NonbondedForce()
    nbf.setNonbondedMethod(mm.NonbondedForce.NoCutoff)
    nbf.setUseDispersionCorrection(False)
    for q, e in zip(charges, eps):
        system.addParticle(12.0)
        nbf.addParticle(q, 0.3, e)
    nbf.createExceptionsFromBonds([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)], 0.8333, 0.5)
    system.addForce(nbf)
    pos = [Vec3(0.0, 0, 0), Vec3(0.15, 0, 0), Vec3(0.30, 0, 0), Vec3(0.45, 0.1, 0),
           Vec3(0.60, 0, 0), Vec3(0.75, 0.1, 0), Vec3(2.0, 2.0, 2.0)] * unit.nanometer

    e_base = _energy(system, pos)

    m = MSLDModel(7)
    m.add_block(site=1, atoms=[4, 5])
    m.add_block(site=1, atoms=[6])
    m.finalize()
    build_msld_system(system, m)

    e_one = _energy(system, pos, [1.0] * m.n_blocks)
    assert abs(e_one - e_base) < 1e-5 * max(1.0, abs(e_base)), (e_one, e_base)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nall exception (1-4) tests passed")
