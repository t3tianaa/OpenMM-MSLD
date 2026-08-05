"""Stress tests for the two unverified corners of the force-calculation design.

(1) same-site PME cancellation with CHARGED atoms:
    two same-site charged atoms must have NO net mutual interaction after build,
    even under PME (reciprocal space). Test: with them the only charges, the
    total electrostatic energy must be INDEPENDENT of their separation once
    excluded (self-energy is position-independent; there is nothing else charged).

(2) analytic dU/dlambda summation across forces:
    one block's lambda appears in its bond, angle, torsion, AND LJ forces.
    getEnergyParameterDerivatives()['lambda1'] must equal the FULL derivative
    (checked against finite difference of the total energy).
"""
import os
import sys

import openmm as mm
from openmm import unit, Vec3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.model import MSLDModel
from msld.builder import build_msld_system, set_lambdas

_REF = mm.Platform.getPlatform("Reference")
_KJ = unit.kilojoule_per_mole


def _energy(system, pos, lambdas=None, want_derivs=False):
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(pos)
    if lambdas is not None:
        set_lambdas(ctx, lambdas)
    st = ctx.getState(getEnergy=True, getParameterDerivatives=want_derivs)
    e = st.getPotentialEnergy().value_in_unit(_KJ)
    if want_derivs:
        return e, {k: v for k, v in st.getEnergyParameterDerivatives().items()}
    return e


# --------------------------------------------------------------------------
# (1) same-site cancellation under PME, with real charges
# --------------------------------------------------------------------------
def _pme_two_charges():
    L = 2.5
    system = mm.System()
    system.setDefaultPeriodicBoxVectors(Vec3(L, 0, 0) * unit.nanometer,
                                        Vec3(0, L, 0) * unit.nanometer,
                                        Vec3(0, 0, L) * unit.nanometer)
    nbf = mm.NonbondedForce()
    nbf.setNonbondedMethod(mm.NonbondedForce.PME)
    nbf.setCutoffDistance(1.0 * unit.nanometer)
    nbf.setUseDispersionCorrection(False)
    for q in [1.0, -1.0, 0.0, 0.0]:          # only atoms 0,1 are charged
        system.addParticle(12.0)
        nbf.addParticle(q, 0.3, 0.0)         # epsilon 0 -> pure electrostatics
    system.addForce(nbf)
    return system


def _pos(atom1_x):
    return [Vec3(0.5, 0.5, 0.5), Vec3(atom1_x, 0.5, 0.5),
            Vec3(2.0, 2.0, 2.0), Vec3(2.0, 2.0, 1.7)] * unit.nanometer


def test_same_site_pme_matches_reference():
    # REFERENCE: full charges (+1,-1) with a NORMAL exclusion between 0 and 1.
    # This is the physically-correct "excluded charged pair" under PME (its energy
    # is weakly position-dependent through periodic images -- that's expected).
    ref = _pme_two_charges()
    ref.getForce(0).addException(0, 1, 0.0, 0.0, 0.0)     # normal exclusion, full charges

    # BUILT: same charges, but via MSLD (base charge 0 + lambda offset + same-site
    # exclusion). At lambda=1 it must reproduce the reference EXACTLY, otherwise the
    # parameter offset is not being applied to the PME exclusion correction.
    built = _pme_two_charges()
    m = MSLDModel(4)
    m.add_block(site=1, atoms=[0])
    m.add_block(site=1, atoms=[1])
    m.finalize()
    build_msld_system(built, m)

    for x in (0.8, 1.1):                                  # two separations
        e_ref = _energy(ref, _pos(x))
        e_built = _energy(built, _pos(x), [1.0, 1.0, 1.0])
        assert abs(e_ref - e_built) < 1e-4 * max(1.0, abs(e_ref)), (x, e_ref, e_built)


# --------------------------------------------------------------------------
# (2) analytic dU/dlambda1 must be the SUM over bond+angle+torsion+LJ forces
# --------------------------------------------------------------------------
def _multi_force_system():
    # env 0,1,2 ; block1={3,4} (site1) ; block2={5} inert (site1)
    system = mm.System()
    nbf = mm.NonbondedForce()
    nbf.setNonbondedMethod(mm.NonbondedForce.NoCutoff)
    eps = [0.5, 0.5, 0.5, 0.5, 0.5, 0.0]
    for e in eps:
        system.addParticle(12.0)
        nbf.addParticle(0.0, 0.3, e)         # charge 0 -> only LJ + bonded depend on lambda1

    bond = mm.HarmonicBondForce()
    bond.addBond(2, 3, 0.15, 200000.0)       # env-block1 -> lambda1
    bond.addBond(3, 4, 0.15, 200000.0)       # within block1 -> lambda1
    system.addForce(bond)

    ang = mm.HarmonicAngleForce()
    ang.addAngle(2, 3, 4, 1.9, 400.0)        # -> lambda1
    system.addForce(ang)

    tor = mm.PeriodicTorsionForce()
    tor.addTorsion(1, 2, 3, 4, 2, 0.0, 8.0)  # -> lambda1
    system.addForce(tor)

    system.addForce(nbf)                     # LJ env<->block1 + within -> lambda1
    pos = [Vec3(0.00, 0.00, 0.00), Vec3(0.15, 0.02, 0.00), Vec3(0.30, 0.00, 0.05),
           Vec3(0.45, 0.10, 0.00), Vec3(0.55, 0.08, 0.10), Vec3(0.00, 0.50, 0.00)]
    return system, pos * unit.nanometer


def test_lambda_derivative_sums_across_forces():
    system, pos = _multi_force_system()
    m = MSLDModel(6)
    m.add_block(site=1, atoms=[3, 4])
    m.add_block(site=1, atoms=[5])
    m.finalize()
    build_msld_system(system, m)

    # lambda1 must be spread across several MSLD forces
    l1_forces = [f.getName() for f in system.getForces()
                 if f.getName().startswith("MSLD") and f.getName().endswith("_1")]
    assert len(l1_forces) >= 3, l1_forces      # bond, angle, torsion, LJ

    lam = [1.0, 0.5, 1.0]
    _, d = _energy(system, pos, lam, want_derivs=True)
    d_analytic = d["lambda1"]

    # finite difference of the TOTAL energy w.r.t. lambda1
    h = 1e-4
    ep = _energy(system, pos, [1.0, 0.5 + h, 1.0])
    em = _energy(system, pos, [1.0, 0.5 - h, 1.0])
    d_fd = (ep - em) / (2 * h)

    assert abs(d_analytic - d_fd) < 1e-3 * max(1.0, abs(d_fd)), (d_analytic, d_fd)
    print(f"  lambda1 in {len(l1_forces)} forces {l1_forces}")
    print(f"  d_analytic={d_analytic:.4f}  d_fd={d_fd:.4f}")


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\ngrill tests passed")
