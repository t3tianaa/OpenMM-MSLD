"""Tests: angle & torsion block-scaling.

Trick to avoid hand-computing angle/dihedral geometry: let OpenMM compute the
base term energy E1 (at lambda=1), then assert the scaled energy == factor*E1,
where factor is the product of the block lambdas on that term. This validates
the classifier + lambda-prefix independent of the actual geometry.

Also checks dU/dlambda via OpenMM's energy-parameter-derivative.
"""
import os
import sys

import openmm as mm
from openmm import unit, Vec3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.model import MSLDModel
from msld.builder import build_msld_system, set_lambdas

_REF = mm.Platform.getPlatform("Reference")


def _energy_and_derivs(system, positions, lambdas):
    integ = mm.VerletIntegrator(0.001)
    ctx = mm.Context(system, integ, _REF)
    ctx.setPositions(positions)
    set_lambdas(ctx, lambdas)
    st = ctx.getState(getEnergy=True, getParameterDerivatives=True)
    e = st.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
    d = {k: v for k, v in st.getEnergyParameterDerivatives().items()}
    return e, d


def _check(system, positions, model, lam_partial, factor, deriv_checks):
    """Build, verify lambda=1 gives nonzero base E1, and factor*E1 at lam_partial."""
    build_msld_system(system, model)
    ones = [1.0] * model.n_blocks
    e1, _ = _energy_and_derivs(system, positions, ones)
    assert e1 > 1e-6, f"base term energy ~0 ({e1}); pick geometry with nonzero E"
    ep, d = _energy_and_derivs(system, positions, lam_partial)
    assert abs(ep - factor * e1) < 1e-6 * max(1.0, abs(e1)), (ep, factor * e1)
    for name, expected_cofactor in deriv_checks.items():
        assert abs(d[name] - expected_cofactor * e1) < 1e-6 * max(1.0, abs(e1)), \
            (name, d[name], expected_cofactor * e1)


# ------------------------------------------------------------------- angles
def test_angle_single_lambda():
    # atoms 0,1 env; site1: b1={2}, b2={3}; angle (0,1,2) -> single lambda1
    system = mm.System()
    for _ in range(4):
        system.addParticle(12.0)
    haf = mm.HarmonicAngleForce()
    haf.addAngle(0, 1, 2, 2.0, 400.0)          # theta0=2.0 rad, k=400
    system.addForce(haf)
    pos = [Vec3(0.1, 0, 0), Vec3(0, 0, 0), Vec3(0, 0.1, 0), Vec3(0.2, 0.2, 0)] * unit.nanometer

    m = MSLDModel(4)
    m.add_block(site=1, atoms=[2])
    m.add_block(site=1, atoms=[3])
    m.finalize()
    # lambda1=0.4 -> energy 0.4*E1; dU/dlambda1 = E1
    _check(system, pos, m, [1.0, 0.4, 1.0], 0.4, {"lambda1": 1.0})


def test_angle_product_lambda():
    # site1: b1={1}, b2={2}; site2: b3={3}, b4={4}; angle (1,0,3) -> lambda1*lambda3
    system = mm.System()
    for _ in range(5):
        system.addParticle(12.0)
    haf = mm.HarmonicAngleForce()
    haf.addAngle(1, 0, 3, 2.0, 400.0)
    system.addForce(haf)
    pos = [Vec3(0, 0, 0), Vec3(0.1, 0, 0), Vec3(0.2, 0.1, 0),
           Vec3(0, 0.1, 0), Vec3(0.1, 0.2, 0)] * unit.nanometer

    m = MSLDModel(5)
    m.add_block(site=1, atoms=[1])
    m.add_block(site=1, atoms=[2])
    m.add_block(site=2, atoms=[3])
    m.add_block(site=2, atoms=[4])
    m.finalize()
    # lambda1=0.4, lambda3=0.6 -> factor 0.24; dU/dlambda1=lambda3*E1, dU/dlambda3=lambda1*E1
    _check(system, pos, m, [1.0, 0.4, 1.0, 0.6, 1.0], 0.4 * 0.6,
           {"lambda1": 0.6, "lambda3": 0.4})


# ------------------------------------------------------------------ torsions
def test_torsion_single_lambda():
    # atoms 0,1,2 env; site1: b1={3}, b2={4}; torsion (0,1,2,3) -> single lambda1
    system = mm.System()
    for _ in range(5):
        system.addParticle(12.0)
    ptf = mm.PeriodicTorsionForce()
    ptf.addTorsion(0, 1, 2, 3, 1, 0.3, 10.0)   # per=1, phase=0.3, k=10
    system.addForce(ptf)
    pos = [Vec3(0, 0, 0), Vec3(0.1, 0, 0), Vec3(0.1, 0.1, 0),
           Vec3(0.2, 0.1, 0.1), Vec3(0.3, 0, 0)] * unit.nanometer

    m = MSLDModel(5)
    m.add_block(site=1, atoms=[3])
    m.add_block(site=1, atoms=[4])
    m.finalize()
    _check(system, pos, m, [1.0, 0.4, 1.0], 0.4, {"lambda1": 1.0})


def test_torsion_product_lambda():
    # site1: b1={2}, b2={3}; site2: b3={4}, b4={5}; torsion (2,0,1,4) -> lambda1*lambda3
    system = mm.System()
    for _ in range(6):
        system.addParticle(12.0)
    ptf = mm.PeriodicTorsionForce()
    ptf.addTorsion(2, 0, 1, 4, 1, 0.3, 10.0)
    system.addForce(ptf)
    pos = [Vec3(0, 0, 0), Vec3(0.1, 0, 0), Vec3(0.1, 0.1, 0.05),
           Vec3(0.2, 0.1, 0), Vec3(0.0, 0.1, 0.1), Vec3(0.2, 0.2, 0)] * unit.nanometer

    m = MSLDModel(6)
    m.add_block(site=1, atoms=[2])
    m.add_block(site=1, atoms=[3])
    m.add_block(site=2, atoms=[4])
    m.add_block(site=2, atoms=[5])
    m.finalize()
    _check(system, pos, m, [1.0, 0.4, 1.0, 0.6, 1.0], 0.4 * 0.6,
           {"lambda1": 0.6, "lambda3": 0.4})


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nall angle/torsion tests passed")
