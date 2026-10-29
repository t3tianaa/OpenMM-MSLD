"""Soft-core for overlap-prone nonbonded pairs (block<->env, block<->block across sites).

Without soft-core a switched-off block (lambda ~ 0) fills with solvent and its dU/dlambda is the
unscaled overlap energy (1e5-1e6 kJ/mol), so it can never switch back on. With soft-core:
  - lambda = 1 is unchanged (the soft-core terms vanish at L = 1),
  - dU/dlambda stays bounded when an environment atom sits on top of a block atom,
  - the hybrid dU/dlambda (analytic + FD) still equals a finite difference of the total energy.
"""
import os
import sys

import openmm as mm
from openmm import unit, Vec3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.model import MSLDModel
from msld.builder import scale_msld_system, set_lambdas
from msld.integrator import LambdaDynamics

_REF = mm.Platform.getPlatform("Reference")
_KJ = unit.kilojoule_per_mole
_L = 3.0
# env = 0,1 (bonded pair) ; site 1: block1 = {2}, block2 = {3} ; site 2: block3 = {4}, block4 = {5}
_Q = [0.4, -0.4, -0.5, 0.3, 0.45, -0.2]


def _system(overlap=False):
    system = mm.System()
    system.setDefaultPeriodicBoxVectors(Vec3(_L, 0, 0), Vec3(0, _L, 0), Vec3(0, 0, _L))
    for _ in range(6):
        system.addParticle(12.0)
    nbf = mm.NonbondedForce()
    nbf.setNonbondedMethod(mm.NonbondedForce.PME)
    nbf.setCutoffDistance(1.0)
    nbf.setUseDispersionCorrection(False)
    for q in _Q:
        nbf.addParticle(q, 0.32, 0.5)
    nbf.addException(0, 1, 0.0, 0.1, 0.0)
    system.addForce(nbf)
    hb = mm.HarmonicBondForce()
    hb.addBond(0, 1, 0.15, 1000.0)
    system.addForce(hb)
    x2 = Vec3(1.15, 1.0, 1.0) if not overlap else Vec3(1.0, 1.0, 1.0005)   # block1 on env atom 0
    pos = [Vec3(1.0, 1.0, 1.0), Vec3(1.15, 1.02, 1.0), x2,
           Vec3(0.75, 1.1, 1.05), Vec3(1.3, 1.35, 0.9), Vec3(0.8, 0.7, 1.2)]
    return system, pos * unit.nanometer


def _model(alpha):
    m = MSLDModel(6)
    m.softcore_alpha = alpha
    m.add_block(site=1, atoms=[2], theta0=0.3)
    m.add_block(site=1, atoms=[3], theta0=-0.2)
    m.add_block(site=2, atoms=[4], theta0=0.1)
    m.add_block(site=2, atoms=[5], theta0=0.4)
    return m.finalize()


def _energy(system, pos, lambdas):
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(pos)
    set_lambdas(ctx, lambdas)
    return ctx.getState(getEnergy=True).getPotentialEnergy().value_in_unit(_KJ)


def test_endpoint_unchanged():
    """Soft-core on vs off gives identical energies whenever every lambda is 0 or 1."""
    for lam in ([1, 1, 0, 1, 0], [1, 0, 1, 0, 1], [1, 1, 0, 0, 1]):
        e = []
        for alpha in (0.0, 0.5):
            system, pos = _system()
            scale_msld_system(system, _model(alpha))
            e.append(_energy(system, pos, lam))
        assert abs(e[0] - e[1]) < 1e-6 * max(1.0, abs(e[0])), (lam, e)


def test_softcore_changes_intermediate_lambda():
    e = []
    for alpha in (0.0, 0.5):
        system, pos = _system()
        scale_msld_system(system, _model(alpha))
        e.append(_energy(system, pos, [1, 0.3, 0.7, 0.6, 0.4]))
    assert abs(e[0] - e[1]) > 1e-3, e


def _dyn(alpha, overlap, theta):
    system, pos = _system(overlap)
    model = _model(alpha)
    scale_msld_system(system, model)
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(pos)
    dyn = LambdaDynamics(ctx, model, temperature=300.0, fd_step=1e-2)
    dyn.theta = list(theta)
    return dyn


def test_overlap_derivative_bounded():
    """Block 1 sits 0.0005 nm from an environment atom and is switched off."""
    theta = [0.0, -1.5, 1.5, 0.3, 0.4]          # lambda1 ~ 1.7e-5
    d_plain, lam = _dyn(0.0, True, theta).dUdlambda()
    d_soft, _ = _dyn(0.5, True, theta).dUdlambda()
    assert lam[1] < 1e-4, lam
    assert abs(d_plain[1]) > 1e8, d_plain[1]     # r^-12 wall: enormous
    assert abs(d_soft[1]) < 2e3, d_soft[1]       # soft-core: bounded
    print(f"  overlapped off block: dU/dlambda plain {d_plain[1]:.3g}, soft-core {d_soft[1]:.3g}")


def _full_fd(dyn, h=1e-5):
    d = {}
    for b in dyn.dof:
        name = f"lambda{b}"
        base = dyn.context.getParameter(name)
        dyn.context.setParameter(name, base + h); ep = dyn.potential_energy()
        dyn.context.setParameter(name, base - h); em = dyn.potential_energy()
        dyn.context.setParameter(name, base)
        d[b] = (ep - em) / (2 * h)
    return d


def test_hybrid_matches_full_fd_with_softcore():
    for theta in ([0.0, 0.3, -0.2, 0.1, 0.4], [0.0, -0.9, 0.9, 0.6, -0.4]):
        dyn = _dyn(0.5, False, theta)
        d, lam = dyn.dUdlambda()
        full = _full_fd(dyn)
        for b in dyn.dof:
            assert abs(d[b] - full[b]) < 1e-4 * max(1.0, abs(full[b])), (theta, b, d[b], full[b])


def test_theta_force_matches_fd_with_softcore():
    dyn = _dyn(0.5, False, [0.0, 0.3, -0.2, 0.1, 0.4])
    g = dyn.dUdtheta()
    h = 1e-5
    for i in dyn.dof:
        t0 = dyn.theta[i]
        dyn.theta[i] = t0 + h; dyn.project(); ep = dyn.potential_energy()
        dyn.theta[i] = t0 - h; dyn.project(); em = dyn.potential_energy()
        dyn.theta[i] = t0; dyn.project()
        fd = (ep - em) / (2 * h)
        assert abs(g[i] - fd) < 1e-4 * max(1.0, abs(fd)), (i, g[i], fd)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nsoft-core tests passed")
