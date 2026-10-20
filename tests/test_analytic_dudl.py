"""Tier-0 hybrid dU/dlambda: analytic + electrostatics-only finite difference.

The integrator gets dU/dlambda_b as
    analytic (bonded + LJ + within-block correction + biases, via
    addEnergyParameterDerivative)  +  finite difference of ONLY the base
    NonbondedForce (electrostatics charge-scaling, which OpenMM cannot expose).

This must equal a finite difference of the FULL energy (what the engine used to
do) to machine-ish precision in double precision. We build one rich system that
exercises every force type -- if any analytic-capable force were NOT registered
(e.g. the bias, historically), the hybrid would drop that term and this test would
fail, exactly as it would have for the +bias gradient.
"""
import os
import sys

import openmm as mm
from openmm import unit, Vec3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.model import MSLDModel
from msld.builder import scale_msld_system, set_lambdas, ANALYTIC_FORCE_GROUP, FD_FORCE_GROUP
from msld.forces import lambda_name
from msld.integrator import LambdaDynamics

_REF = mm.Platform.getPlatform("Reference")     # double precision -> FD is accurate
_KJ = unit.kilojoule_per_mole


# Topology (18 atoms). env is a 10-atom chain 0-1-...-9; the four alchemical blocks
# attach at env atoms 0, 3, 6, 9 -- >=3 env bonds apart, so NO cross-block pair is within
# 1-4 (a same-site or cross-site scaled 1-4 would be illegal/deferred; real prep pre-excludes
# same-site pairs, which a hand-built createExceptionsFromBonds would otherwise make scaled).
#   site1: block1 = {10,11,12,13,14} chain off env0  ;  block2 = {15} off env3
#   site2: block3 = {16} off env6                    ;  block4 = {17} off env9
# block1's chain gives a within-block 1-4 scaled exception (10-13) AND a within-block full
# 1-5 pair (10-14 -> within-block electrostatics correction fires). Every atom has charge + LJ.
_BLOCK1 = [10, 11, 12, 13, 14]


def _rich_system():
    n = 18
    system = mm.System()
    for _ in range(n):
        system.addParticle(12.0)

    bond_pairs = [(i, i + 1) for i in range(9)]                    # env chain 0..9
    bond_pairs += [(0, 10), (10, 11), (11, 12), (12, 13), (13, 14)]  # block1 off env0
    bond_pairs += [(3, 15), (6, 16), (9, 17)]                     # block2/3/4 attachments
    bond = mm.HarmonicBondForce()
    for a, c in bond_pairs:
        bond.addBond(a, c, 0.15, 2000.0)
    system.addForce(bond)

    angle = mm.HarmonicAngleForce()
    angle.addAngle(0, 10, 11, 1.9, 300.0)        # env-block1-block1 -> lambda1
    angle.addAngle(10, 11, 12, 1.9, 300.0)
    angle.addAngle(0, 1, 2, 1.9, 300.0)          # env-only -> unscaled (stays in base)
    system.addForce(angle)

    tors = mm.PeriodicTorsionForce()
    tors.addTorsion(0, 10, 11, 12, 2, 0.0, 8.0)  # -> lambda1
    tors.addTorsion(10, 11, 12, 13, 3, 0.0, 6.0)
    system.addForce(tors)

    nbf = mm.NonbondedForce()
    nbf.setNonbondedMethod(mm.NonbondedForce.NoCutoff)
    rng = [((-1) ** i) * (0.2 + 0.02 * i) for i in range(n)]      # spread of charges
    for q in rng:
        nbf.addParticle(q, 0.28, 0.4)
    # 1-2/1-3 exclusions + scaled 1-4 exceptions from the bond graph
    nbf.createExceptionsFromBonds(bond_pairs, 0.8333, 0.5)
    system.addForce(nbf)

    pos = [Vec3(0.15 * i, 0.0, 0.0) for i in range(10)]           # env chain along x
    pos += [Vec3(0.0, 0.15 * k, 0.0) for k in range(1, 6)]        # block1 chain up y off env0
    pos += [Vec3(0.45, 0.15, 0.0), Vec3(0.90, 0.15, 0.0), Vec3(1.35, 0.15, 0.0)]  # 15,16,17
    return system, pos * unit.nanometer


def _rich_model(block1_bias=2.0):
    m = MSLDModel(18)
    m.add_block(site=1, atoms=_BLOCK1, theta0=0.25, lambda_bias=block1_bias)   # fixed bias
    m.add_block(site=1, atoms=[15], theta0=-0.15)
    m.add_block(site=2, atoms=[16], theta0=0.10)
    m.add_block(site=2, atoms=[17], theta0=0.40)
    m.add_variable_bias(1, 3, 6, 0.0, 3.0, 0)     # type-6 coupling k*lambda1*lambda3
    return m.finalize()


def _full_fd(dyn, lam):
    """Central FD of the FULL energy at fixed lambda `lam` (the old engine's dU/dlambda)."""
    set_lambdas(dyn.context, lam)
    h = dyn.h
    d = {}
    present = dyn.context.getParameters()
    for b in dyn.dof:
        name = lambda_name(b)
        if name not in present:
            continue
        base = dyn.context.getParameter(name)
        dyn.context.setParameter(name, base + h); ep = dyn.potential_energy()
        dyn.context.setParameter(name, base - h); em = dyn.potential_energy()
        dyn.context.setParameter(name, base)
        d[b] = (ep - em) / (2 * h)
    return d


def _build(block1_bias=2.0):
    system, pos = _rich_system()
    model = _rich_model(block1_bias)
    scale_msld_system(system, model)
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(pos)
    dyn = LambdaDynamics(ctx, model, temperature=300.0, fd_step=1e-5)
    return system, model, ctx, dyn


def test_force_group_split():
    """Analytic-capable forces go to ANALYTIC_FORCE_GROUP; electrostatics + bias stay in group 0.

    The split is by whether a force registered an energy-parameter derivative -- so the base
    NonbondedForce and the CustomExternalForce bias (neither can) land in the FD group, while
    the scaled bonded/LJ/within-block CustomForces land in the analytic group.
    """
    system, model, ctx, dyn = _build()
    fd, an = [], []
    for i in range(system.getNumForces()):
        f = system.getForce(i)
        (an if f.getForceGroup() == ANALYTIC_FORCE_GROUP else fd).append(f)
    # every analytic-group force actually registered a derivative; no FD-group force did
    assert an and all(f.getNumEnergyParameterDerivatives() > 0 for f in an)
    assert any(isinstance(f, mm.NonbondedForce) for f in fd)          # electrostatics -> FD
    assert any(f.getName() == "MSLDBias" for f in fd)                 # bias -> FD
    assert dyn._has_fd is True


def test_hybrid_dudl_matches_full_fd():
    """Hybrid (analytic + electrostatics-only FD) == full-energy FD, over several lambda points."""
    system, model, ctx, dyn = _build()

    # a spread of theta -> lambda points, including the master-invariant point (all lambda = 1)
    theta_points = [
        [0.0, 0.25, -0.15, 0.10, 0.40],      # the model's own thetas
        [0.0, 0.9, -0.9, 0.5, -0.5],
        [0.0, -0.7, 0.7, -0.3, 0.6],
        [0.0, 5.0, -5.0, 5.0, -5.0],         # near lambda = 1/0 endpoints per site
    ]
    for theta in theta_points:
        dyn.theta = list(theta)
        d_hybrid, lam = dyn.dUdlambda()          # NEW path (also restores lambda)
        d_full = _full_fd(dyn, lam)              # independent gold standard at the same lambda
        for b in dyn.dof:
            hv, fv = d_hybrid[b], d_full[b]
            assert abs(hv - fv) < 1e-4 * max(1.0, abs(fv)), (theta, b, hv, fv)


def test_bias_gradient_captured():
    """Regression: the fixed-bias contribution to dU/dlambda1 is NOT dropped.

    The bias is a CustomExternalForce (cannot expose an analytic derivative) and lives in the
    FD group. Compare two builds differing ONLY in block1's fixed bias (2.0 vs 0.0) at the same
    lambda: dU/dlambda1 must differ by exactly the bias coefficient (d(bias*lambda1)/dlambda1 = 2.0).
    Everything else (electrostatics, bonded, LJ, variable bias) is identical and cancels.
    """
    theta = [0.0, 0.3, -0.2, 0.15, 0.45]
    _, _, _, dyn_on = _build(block1_bias=2.0)
    _, _, _, dyn_off = _build(block1_bias=0.0)
    dyn_on.theta = list(theta);  d_on, _ = dyn_on.dUdlambda()
    dyn_off.theta = list(theta); d_off, _ = dyn_off.dUdlambda()
    assert abs((d_on[1] - d_off[1]) - 2.0) < 1e-4, (d_on[1], d_off[1])


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); print("ok", name)
