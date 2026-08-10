"""Holonomic constraints (SHAKE/RATTLE) in the lambda-dynamics driver.

A System constraint must stay satisfied throughout a trajectory, while lambda
still moves. Exercises the constrained BAOAB path in LambdaDynamics.
"""
import os
import sys

import numpy as np
import openmm as mm
from openmm import unit, Vec3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.model import MSLDModel
from msld.builder import build_msld_system
from msld.integrator import LambdaDynamics

_REF = mm.Platform.getPlatform("Reference")
_D0 = 0.15


def test_constraint_kept_rigid():
    system = mm.System()
    for _ in range(4):
        system.addParticle(12.0)
    system.addConstraint(0, 1, _D0 * unit.nanometer)     # rigid bond 0-1
    hbf = mm.HarmonicBondForce()
    hbf.addBond(0, 2, 0.12, 3000.0)                      # env-block1 -> scaled by lambda1
    system.addForce(hbf)

    m = MSLDModel(4)
    m.add_block(site=1, atoms=[2], theta0=0.2)
    m.add_block(site=1, atoms=[3], theta0=-0.1)
    m.finalize()
    build_msld_system(system, m)

    pos = [Vec3(0, 0, 0), Vec3(_D0, 0, 0), Vec3(0.10, 0.10, 0), Vec3(0.20, 0.20, 0)] * unit.nanometer
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(pos)
    dyn = LambdaDynamics(ctx, m, temperature=300.0, timestep=0.001, seed=2)
    assert dyn.has_constraints

    lam0 = dyn.get_lambdas()
    for _ in range(50):
        dyn.step(5)
        d = np.linalg.norm(dyn.x[0] - dyn.x[1])          # constrained distance
        assert abs(d - _D0) < 1e-4, d                    # stays rigid
        lam = dyn.get_lambdas()
        assert abs(lam[1] + lam[2] - 1.0) < 1e-9
        assert all(np.isfinite(dyn.x).flatten())

    lam1 = dyn.get_lambdas()
    assert any(abs(lam1[b] - lam0[b]) > 1e-3 for b in dyn.dof), (lam0, lam1)  # lambda moved
    print(f"  final |x0-x1| = {np.linalg.norm(dyn.x[0]-dyn.x[1]):.6f} nm (target {_D0})")
    print(f"  lambda {[round(x,3) for x in lam0]} -> {[round(x,3) for x in lam1]}")


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nconstraint tests passed")
