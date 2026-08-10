"""Biasing potentials + term-scaling flags.

Biases are pure functions of lambda; we check the added energy equals the
hand-computed bias. Term-scaling flags let a bonded term type be left unscaled
(BLaDE 'removescaling'); we check a bond stops responding to lambda.
"""
import os
import sys

import openmm as mm
from openmm import unit, Vec3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.model import MSLDModel
from msld.builder import build_msld_system, set_lambdas

_REF = mm.Platform.getPlatform("Reference")


def _energy(system, pos, lambdas):
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(pos)
    set_lambdas(ctx, lambdas)
    return ctx.getState(getEnergy=True).getPotentialEnergy().value_in_unit(
        unit.kilojoule_per_mole)


def _bare(n):
    system = mm.System()
    for _ in range(n):
        system.addParticle(12.0)
    return system, [Vec3(0.1 * i, 0, 0) for i in range(n)] * unit.nanometer


def test_fixed_bias():
    # bias = 2.0 * lambda1
    system, pos = _bare(3)
    m = MSLDModel(3)
    m.add_block(site=1, atoms=[1], lambda_bias=2.0)
    m.add_block(site=1, atoms=[2])
    m.finalize()
    build_msld_system(system, m)
    assert abs(_energy(system, pos, [1.0, 0.4, 0.6]) - 2.0 * 0.4) < 1e-9
    assert abs(_energy(system, pos, [1.0, 1.0, 0.0]) - 2.0 * 1.0) < 1e-9


def _two_site_bias(bias_type, l0, k):
    system, pos = _bare(5)
    m = MSLDModel(5)
    m.add_block(site=1, atoms=[1])
    m.add_block(site=1, atoms=[2])
    m.add_block(site=2, atoms=[3])
    m.add_block(site=2, atoms=[4])
    m.add_variable_bias(1, 3, bias_type, l0, k, 0)   # bias between block1 and block3
    m.finalize()
    build_msld_system(system, m)
    return _energy(system, pos, [1.0, 0.4, 1.0, 0.6, 1.0])   # lambda1=0.4, lambda3=0.6


def test_variable_bias_quadratic():          # type 6:  k*li*lj
    assert abs(_two_site_bias(6, 0.0, 3.0) - 3.0 * 0.4 * 0.6) < 1e-9


def test_variable_bias_endpoint():           # type 8:  k*li*lj/(li+l0)
    expect = 2.0 * 0.4 * 0.6 / (0.4 + 0.5)
    assert abs(_two_site_bias(8, 0.5, 2.0) - expect) < 1e-9


def test_variable_bias_skew():               # type 10: k*lj*(1-exp(l0*li))
    import math
    expect = 1.0 * 0.6 * (1.0 - math.exp(-1.0 * 0.4))
    assert abs(_two_site_bias(10, -1.0, 1.0) - expect) < 1e-9


def test_removescaling_bond():
    # a bond between env and block1; with scaling OFF it must not respond to lambda
    def build(scale):
        system = mm.System()
        for _ in range(3):
            system.addParticle(12.0)
        hbf = mm.HarmonicBondForce()
        hbf.addBond(0, 1, 0.10, 1000.0)          # env-block1, deviation -> nonzero E
        system.addForce(hbf)
        m = MSLDModel(3)
        m.add_block(site=1, atoms=[1])
        m.add_block(site=1, atoms=[2])
        m.scale_bond = scale
        m.finalize()
        info = build_msld_system(system, m)
        pos = [Vec3(0, 0, 0), Vec3(0.2, 0, 0), Vec3(1.0, 0, 0)] * unit.nanometer
        return info, _energy(system, pos, [1.0, 0.3, 0.7]), _energy(system, pos, [1.0, 1.0, 0.0])

    info_off, e_off_partial, e_off_full = build(False)
    assert info_off["scaled_bond_forces"] == []          # nothing moved out
    assert abs(e_off_partial - e_off_full) < 1e-9         # bond ignores lambda

    info_on, e_on_partial, e_on_full = build(True)
    assert info_on["scaled_bond_forces"]                  # a scaled force exists
    assert abs(e_on_partial - 0.3 * e_on_full) < 1e-9     # bond scales by lambda1


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nbias + term-scaling tests passed")
