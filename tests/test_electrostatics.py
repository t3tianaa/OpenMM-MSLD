"""Eelectrostatics + PME block-scaling via charge offsets.

OpenMM computes the base pair energy E1 (at lambda=1), and 
we assert the scaled energy == factor*E1, with factor the
product of the block lambdas. Plus: same-site exclusion, 
and PME recovers-base.
"""
import os
import sys

import openmm as mm
from openmm import unit, Vec3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.model import MSLDModel
from msld.builder import build_msld_system, set_lambdas

_REF = mm.Platform.getPlatform("Reference")


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


def _nb_nocutoff(charges):
    """NonbondedForce, NoCutoff, pure charges (epsilon=0)."""
    system = mm.System()
    nbf = mm.NonbondedForce()
    nbf.setNonbondedMethod(mm.NonbondedForce.NoCutoff)
    for q in charges:
        system.addParticle(12.0)
        nbf.addParticle(q, 0.3, 0.0)      # charge, sigma, epsilon=0
    system.addForce(nbf)
    return system


def _fd_dUdlambda(system, pos, base_lams, block, h=1e-4):
    """Finite-difference dU/dlambda_block (electrostatics offsets give no analytic
    derivative, so we validate the scaling this way)."""
    lp = list(base_lams); lp[block] += h
    lm = list(base_lams); lm[block] -= h
    ep, _ = _energy_and_derivs(system, pos, lp)
    em, _ = _energy_and_derivs(system, pos, lm)
    return (ep - em) / (2 * h)


def _check(system, pos, model, lam_partial, factor, deriv_checks):
    build_msld_system(system, model)
    e1, _ = _energy_and_derivs(system, pos, [1.0] * model.n_blocks)
    assert abs(e1) > 1e-6, f"base pair energy ~0 ({e1})"
    ep, _ = _energy_and_derivs(system, pos, lam_partial)
    assert abs(ep - factor * e1) < 1e-6 * max(1.0, abs(e1)), (ep, factor * e1)
    # dU/dlambda_b via finite difference == cofactor * E1
    for name, cofactor in deriv_checks.items():
        b = int(name.replace("lambda", ""))
        fd = _fd_dUdlambda(system, pos, lam_partial, b)
        assert abs(fd - cofactor * e1) < 1e-3 * max(1.0, abs(e1)), (name, fd, cofactor * e1)


def test_elec_single_lambda():
    # 0=env(+1), site1: b1={1}(+1), b2={2}(0). Only pair (0,1) charged -> single lambda1
    system = _nb_nocutoff([1.0, 1.0, 0.0])
    pos = [Vec3(0, 0, 0), Vec3(0.3, 0, 0), Vec3(1.0, 0, 0)] * unit.nanometer
    m = MSLDModel(3)
    m.add_block(site=1, atoms=[1])
    m.add_block(site=1, atoms=[2])
    m.finalize()
    _check(system, pos, m, [1.0, 0.4, 1.0], 0.4, {"lambda1": 1.0})


def test_elec_product_lambda():
    # site1: b1={1}(+1),b2={2}(0); site2: b3={3}(+1),b4={4}(0). pair (1,3) -> lambda1*lambda3
    system = _nb_nocutoff([0.0, 1.0, 0.0, 1.0, 0.0])
    pos = [Vec3(2, 0, 0), Vec3(0, 0, 0), Vec3(2, 2, 0),
           Vec3(0.4, 0, 0), Vec3(2, 2, 2)] * unit.nanometer
    m = MSLDModel(5)
    m.add_block(site=1, atoms=[1])
    m.add_block(site=1, atoms=[2])
    m.add_block(site=2, atoms=[3])
    m.add_block(site=2, atoms=[4])
    m.finalize()
    _check(system, pos, m, [1.0, 0.4, 1.0, 0.6, 1.0], 0.4 * 0.6,
           {"lambda1": 0.6, "lambda3": 0.4})


def test_elec_same_site_excluded():
    # site1: b1={0}(+1), b2={1}(+1) placed close; must be excluded after build.
    system = _nb_nocutoff([1.0, 1.0, 0.0])
    pos = [Vec3(0, 0, 0), Vec3(0.2, 0, 0), Vec3(1.5, 0, 0)] * unit.nanometer
    m = MSLDModel(3)
    m.add_block(site=1, atoms=[0])
    m.add_block(site=1, atoms=[1])
    m.finalize()

    e_pre, _ = _energy_and_derivs(system, pos)           # before build: big clash
    assert e_pre > 100.0, e_pre
    build_msld_system(system, m)
    e_post, _ = _energy_and_derivs(system, pos, [1.0, 1.0, 1.0])
    assert abs(e_post) < 1e-6, e_post                    # same-site pair removed


def test_elec_pme_recovers_base():
    # periodic PME, neutral; alchemical charged blocks in different sites, their
    # same-site partners have q=0 so same-site exclusions don't change the energy.
    charges = [0.5, 0.0, -0.5, 0.0, 0.3, -0.3]           # net 0
    system = mm.System()
    L = 2.0
    system.setDefaultPeriodicBoxVectors(Vec3(L, 0, 0) * unit.nanometer,
                                        Vec3(0, L, 0) * unit.nanometer,
                                        Vec3(0, 0, L) * unit.nanometer)
    nbf = mm.NonbondedForce()
    nbf.setNonbondedMethod(mm.NonbondedForce.PME)
    nbf.setCutoffDistance(0.8 * unit.nanometer)
    for q in charges:
        system.addParticle(12.0)
        nbf.addParticle(q, 0.3, 0.0)
    system.addForce(nbf)
    pos = [Vec3(0.2, 0.2, 0.2), Vec3(0.5, 0.2, 0.2), Vec3(1.2, 1.0, 0.5),
           Vec3(1.5, 1.0, 0.5), Vec3(0.8, 1.5, 1.2), Vec3(1.7, 0.4, 1.6)] * unit.nanometer

    e_base, _ = _energy_and_derivs(system, pos)          # pristine PME energy

    m = MSLDModel(6)
    m.add_block(site=1, atoms=[0])
    m.add_block(site=1, atoms=[1])
    m.add_block(site=2, atoms=[2])
    m.add_block(site=2, atoms=[3])
    m.finalize()
    build_msld_system(system, m)
    e_one, _ = _energy_and_derivs(system, pos, [1.0] * m.n_blocks)
    assert abs(e_one - e_base) < 1e-4 * max(1.0, abs(e_base)), (e_one, e_base)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nall electrostatics tests passed")
