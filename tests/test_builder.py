"""Tests for builder.py + forces.add_scaled_bonds.

Synthetic 6-atom, 2-site system with a HarmonicBondForce carrying one bond of
each scaling kind:
    (0,1) env-env          -> unscaled
    (0,2) env-block1       -> single   lambda1
    (2,4) block1<->block3  -> product  lambda1*lambda3   (different sites)

Blocks: 0=env; site1: b1={2}, b2={3}; site2: b3={4}, b4={5}.

Checks:
  1. lambda=1 everywhere  -> total energy == unscaled base energy
  2. partial lambda       -> energy == hand-computed scaled sum
  3. dU/dlambda1          -> matches analytic, via finite difference AND OpenMM's
                             own energy-parameter-derivative
"""
import os
import sys

import openmm as mm
from openmm import unit, Vec3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.model import MSLDModel
from msld.builder import build_msld_system, set_lambdas

K = 1000.0          # kJ/mol/nm^2
R0 = 0.1            # nm
_REF = mm.Platform.getPlatform("Reference")

POSITIONS = [Vec3(0.00, 0.0, 0.0),   # 0 env
             Vec3(0.12, 0.0, 0.0),   # 1 env
             Vec3(0.25, 0.0, 0.0),   # 2 block1
             Vec3(0.00, 0.2, 0.0),   # 3 block2
             Vec3(0.40, 0.0, 0.0),   # 4 block3
             Vec3(0.00, 0.3, 0.0)] * unit.nanometer

# per-bond deviations -> hand-computed base energies 0.5*k*(r-r0)^2
E01 = 0.5 * K * (0.12 - R0) ** 2     # = 0.20
E02 = 0.5 * K * (0.25 - R0) ** 2     # = 11.25
E24 = 0.5 * K * (0.15 - R0) ** 2     # = 1.25  (|0.40-0.25|=0.15)


def build_base():
    system = mm.System()
    for _ in range(6):
        system.addParticle(12.0)
    hbf = mm.HarmonicBondForce()
    hbf.addBond(0, 1, R0, K)
    hbf.addBond(0, 2, R0, K)
    hbf.addBond(2, 4, R0, K)
    system.addForce(hbf)
    return system


def build_model():
    m = MSLDModel(6)
    m.add_block(site=1, atoms=[2])
    m.add_block(site=1, atoms=[3])
    m.add_block(site=2, atoms=[4])
    m.add_block(site=2, atoms=[5])
    return m.finalize()


def energy_and_derivs(system, lambdas):
    integ = mm.VerletIntegrator(0.001)
    ctx = mm.Context(system, integ, _REF)
    ctx.setPositions(POSITIONS)
    set_lambdas(ctx, lambdas)
    st = ctx.getState(getEnergy=True, getParameterDerivatives=True)
    e = st.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
    d = {k: v for k, v in st.getEnergyParameterDerivatives().items()}
    return e, d


def test_lambda_one_recovers_base():
    base = build_base()
    e_base, _ = energy_and_derivs(base, [1, 1, 1, 1, 1])   # no scaling yet -> full base
    assert abs(e_base - (E01 + E02 + E24)) < 1e-6, e_base

    system = build_base()
    build_msld_system(system, build_model())
    e_scaled, _ = energy_and_derivs(system, [1, 1, 1, 1, 1])
    assert abs(e_scaled - e_base) < 1e-6, (e_scaled, e_base)


def test_partial_lambda_value():
    system = build_base()
    build_msld_system(system, build_model())
    # blocks: [env, b1, b2, b3, b4] -> lambda1=0.4, lambda3=0.6
    lam = [1.0, 0.4, 1.0, 0.6, 1.0]
    e, _ = energy_and_derivs(system, lam)
    expected = E01 + 0.4 * E02 + 0.4 * 0.6 * E24
    assert abs(e - expected) < 1e-6, (e, expected)


def test_dUdlambda1():
    system = build_base()
    build_msld_system(system, build_model())
    lam = [1.0, 0.4, 1.0, 0.6, 1.0]

    # analytic: dU/dlambda1 = E02 + lambda3*E24
    analytic = E02 + 0.6 * E24

    # OpenMM's own energy-parameter-derivative
    _, d = energy_and_derivs(system, lam)
    assert abs(d["lambda1"] - analytic) < 1e-6, (d["lambda1"], analytic)

    # finite difference of the energy w.r.t. lambda1
    h = 1e-4
    ep, _ = energy_and_derivs(system, [1.0, 0.4 + h, 1.0, 0.6, 1.0])
    em, _ = energy_and_derivs(system, [1.0, 0.4 - h, 1.0, 0.6, 1.0])
    fd = (ep - em) / (2 * h)
    assert abs(fd - analytic) < 1e-3, (fd, analytic)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nall builder tests passed")
