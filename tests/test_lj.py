"""Lennard-Jones block-scaling via grouped CustomNonbondedForce.

Pure-LJ systems (charges 0), so nonbonded energy is the LJ. CustomNonbondedForce
supports analytic dU/dlambda, so we check the derivative directly.
"""
import os
import sys

import openmm as mm
from openmm import unit, Vec3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.model import MSLDModel
from msld.builder import build_msld_system, set_lambdas

_REF = mm.Platform.getPlatform("Reference")
_SIG = 0.3


def _energy_and_derivs(system, positions, lambdas=None):
    integ = mm.VerletIntegrator(0.001)
    ctx = mm.Context(system, integ, _REF)
    ctx.setPositions(positions)
    if lambdas is not None:
        set_lambdas(ctx, lambdas)
    st = ctx.getState(getEnergy=True, getParameterDerivatives=True)
    e = st.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
    d = {k: v for k, v in st.getEnergyParameterDerivatives().items()}
    return e, d


def _nb_lj(epsilons, method=mm.NonbondedForce.NoCutoff, box=None, cutoff=0.8):
    """System with a NonbondedForce, pure LJ (charge 0), given per-atom epsilons."""
    system = mm.System()
    nbf = mm.NonbondedForce()
    nbf.setNonbondedMethod(method)
    if method != mm.NonbondedForce.NoCutoff:
        nbf.setCutoffDistance(cutoff * unit.nanometer)
    nbf.setUseDispersionCorrection(False)
    if box is not None:
        system.setDefaultPeriodicBoxVectors(Vec3(box, 0, 0) * unit.nanometer,
                                            Vec3(0, box, 0) * unit.nanometer,
                                            Vec3(0, 0, box) * unit.nanometer)
    for eps in epsilons:
        system.addParticle(12.0)
        nbf.addParticle(0.0, _SIG, eps)      # charge 0, sigma, epsilon
    system.addForce(nbf)
    return system


def _check(system, pos, model, lam_partial, factor, deriv_checks):
    build_msld_system(system, model)
    e1, _ = _energy_and_derivs(system, pos, [1.0] * model.n_blocks)
    assert abs(e1) > 1e-6, f"base LJ ~0 ({e1})"
    ep, d = _energy_and_derivs(system, pos, lam_partial)
    assert abs(ep - factor * e1) < 1e-6 * max(1.0, abs(e1)), (ep, factor * e1)
    for name, cofactor in deriv_checks.items():           # analytic dU/dlambda
        assert abs(d[name] - cofactor * e1) < 1e-6 * max(1.0, abs(e1)), \
            (name, d[name], cofactor * e1)


def test_lj_single_lambda():
    # env0(eps1), site1: b1={1}(eps1), b2={2}(eps0). pair (0,1) -> single lambda1
    system = _nb_lj([1.0, 1.0, 0.0])
    pos = [Vec3(0, 0, 0), Vec3(0.35, 0, 0), Vec3(1.5, 0, 0)] * unit.nanometer
    m = MSLDModel(3)
    m.add_block(site=1, atoms=[1])
    m.add_block(site=1, atoms=[2])
    m.finalize()
    _check(system, pos, m, [1.0, 0.4, 1.0], 0.4, {"lambda1": 1.0})


def test_lj_product_lambda():
    # site1: b1={1}(eps1),b2={2}(0); site2: b3={3}(eps1),b4={4}(0). pair (1,3) -> lambda1*lambda3
    system = _nb_lj([0.0, 1.0, 0.0, 1.0, 0.0])
    pos = [Vec3(2, 0, 0), Vec3(0, 0, 0), Vec3(2, 2, 0),
           Vec3(0.35, 0, 0), Vec3(2, 2, 2)] * unit.nanometer
    m = MSLDModel(5)
    m.add_block(site=1, atoms=[1])
    m.add_block(site=1, atoms=[2])
    m.add_block(site=2, atoms=[3])
    m.add_block(site=2, atoms=[4])
    m.finalize()
    _check(system, pos, m, [1.0, 0.4, 1.0, 0.6, 1.0], 0.4 * 0.6,
           {"lambda1": 0.6, "lambda3": 0.4})


def test_lj_same_site_excluded():
    # site1: b1={0}(eps1), b2={1}(eps1) close; their LJ must not be computed.
    system = _nb_lj([1.0, 1.0, 0.0])
    pos = [Vec3(0, 0, 0), Vec3(0.35, 0, 0), Vec3(1.5, 0, 0)] * unit.nanometer
    m = MSLDModel(3)
    m.add_block(site=1, atoms=[0])
    m.add_block(site=1, atoms=[1])
    m.finalize()
    build_msld_system(system, m)
    e, _ = _energy_and_derivs(system, pos, [1.0, 1.0, 1.0])
    assert abs(e) < 1e-6, e          # only LJ pair was same-site -> removed


def _recovers_base(method, box):
    # env 0,1 (eps1); site1 b1={2}(eps1),b2={3}(0); site2 b3={4}(eps1),b4={5}(0)
    system = _nb_lj([1.0, 1.0, 1.0, 0.0, 1.0, 0.0], method=method, box=box)
    pos = [Vec3(0.2, 0.2, 0.2), Vec3(0.6, 0.2, 0.2), Vec3(0.4, 0.6, 0.3),
           Vec3(1.0, 1.0, 1.0), Vec3(0.7, 0.4, 0.7), Vec3(1.3, 1.3, 0.5)] * unit.nanometer
    e_base, _ = _energy_and_derivs(system, pos)
    m = MSLDModel(6)
    m.add_block(site=1, atoms=[2])
    m.add_block(site=1, atoms=[3])
    m.add_block(site=2, atoms=[4])
    m.add_block(site=2, atoms=[5])
    m.finalize()
    build_msld_system(system, m)
    e_one, _ = _energy_and_derivs(system, pos, [1.0] * m.n_blocks)
    assert abs(e_one - e_base) < 1e-5 * max(1.0, abs(e_base)), (method, e_one, e_base)


def test_lj_recovers_base_nocutoff():
    _recovers_base(mm.NonbondedForce.NoCutoff, box=None)


def test_lj_recovers_base_periodic():
    _recovers_base(mm.NonbondedForce.CutoffPeriodic, box=2.0)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nall LJ tests passed")
