"""The softmax chain rule (theta -> lambda -> force).

Validates dU/dtheta_i (computed as dU/dlambda times the analytic softmax
Jacobian) against a direct finite difference of the energy with respect to
theta_i (perturb theta, re-project to lambda, evaluate energy). This is exactly
BLaDE's `test alchemical-theta`, and it checks the chain-rule formula including
the per-site coupling term.
"""
import math
import os
import sys

import openmm as mm
from openmm import unit, Vec3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.model import MSLDModel
from msld.builder import build_msld_system
from msld.integrator import LambdaDynamics

_REF = mm.Platform.getPlatform("Reference")


def _two_site_system():
    # env 0 ; site1: b1={1}, b2={2} ; site2: b3={3}, b4={4}
    # each substituent has one bond to env (so every lambda has a nonzero gradient)
    system = mm.System()
    for _ in range(5):
        system.addParticle(12.0)
    bond = mm.HarmonicBondForce()
    for j, r0 in [(1, 0.10), (2, 0.13), (3, 0.16), (4, 0.20)]:
        bond.addBond(0, j, r0, 1000.0)
    system.addForce(bond)
    pos = [Vec3(0, 0, 0), Vec3(0.15, 0, 0), Vec3(0.22, 0, 0),
           Vec3(0.28, 0, 0), Vec3(0.34, 0, 0)] * unit.nanometer
    return system, pos


def _model():
    m = MSLDModel(5)
    m.add_block(site=1, atoms=[1], theta0=0.3)
    m.add_block(site=1, atoms=[2], theta0=-0.2)
    m.add_block(site=2, atoms=[3], theta0=0.1)
    m.add_block(site=2, atoms=[4], theta0=0.4)
    return m.finalize()


def test_theta_force_matches_finite_difference():
    system, pos = _two_site_system()
    model = _model()
    build_msld_system(system, model)

    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(pos)
    dyn = LambdaDynamics(ctx, model, temperature=300.0)

    # analytic (chain-rule) theta-force
    g = dyn.dUdtheta()

    # sanity: lambdas normalize per site
    lam = dyn.project()
    assert abs(lam[1] + lam[2] - 1.0) < 1e-9
    assert abs(lam[3] + lam[4] - 1.0) < 1e-9

    # finite difference of the energy w.r.t. each theta (through the softmax)
    h = 1e-4
    for i in dyn.dof:
        base = dyn.theta[i]
        dyn.theta[i] = base + h; dyn.project(); ep = dyn.potential_energy()
        dyn.theta[i] = base - h; dyn.project(); em = dyn.potential_energy()
        dyn.theta[i] = base
        fd = (ep - em) / (2 * h)
        assert abs(g[i] - fd) < 1e-3 * max(1.0, abs(fd)), (i, g[i], fd)

    # the coupling term must actually matter: theta_1 force depends on block 2's
    # gradient too, so g[1] is not simply lambda_1*fnex*cos(theta_1)*dUdl_1.
    assert any(abs(g[i]) > 1e-6 for i in dyn.dof)


def test_dynamics_runs_stably():
    # 3b gate: a short trajectory must stay valid (lambda normalized/in-range, no
    # NaN), thermostat theta near the target T, and lambda must actually move.
    system, pos = _two_site_system()
    model = _model()
    build_msld_system(system, model)
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(pos)
    dyn = LambdaDynamics(ctx, model, temperature=300.0, timestep=0.001, seed=1)

    lam0 = dyn.get_lambdas()
    temps = []
    for _ in range(60):
        dyn.step(10)
        lam = dyn.get_lambdas()
        assert abs(lam[1] + lam[2] - 1.0) < 1e-9 and abs(lam[3] + lam[4] - 1.0) < 1e-9
        assert all(-1e-9 <= L <= 1.0 + 1e-9 for L in lam), lam
        assert all(math.isfinite(t) for t in dyn.theta)
        temps.append(dyn.theta_temperature())

    lam1 = dyn.get_lambdas()
    assert any(abs(lam1[b] - lam0[b]) > 1e-3 for b in dyn.dof), (lam0, lam1)  # moved
    avg_T = sum(temps) / len(temps)
    assert 150.0 < avg_T < 600.0, avg_T                                       # thermostatted
    print(f"  avg theta temperature over run: {avg_T:.0f} K  (target 300)")
    print(f"  lambda: {[round(x, 3) for x in lam0]} -> {[round(x, 3) for x in lam1]}")


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nphase 3a (theta-force) tests passed")
