"""Within-block electrostatics must scale LINEARLY (lambda), not lambda^2.

BLaDE (nbdirect.cu) scales a nonbonded pair whose atoms share a block by lambda_b ONCE
(linear), because the two atoms of one substituent are perfectly correlated. The
charge-offset method (each atom's charge * lambda_b) instead gives lambda_b^2 for such a
pair. add_within_block_elec_correction fixes the direct/real space back to linear
(reciprocal stays lambda^2, as in BLaDE's PME). This only affects blocks with a 1-5+
internal pair; small substituents are untouched.
"""
import os
import sys

import openmm as mm
from openmm import unit, Vec3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.model import MSLDModel
from msld.builder import scale_msld_system, set_lambdas

_REF = mm.Platform.getPlatform("Reference")
_KJ = unit.kilojoule_per_mole


def _energy(system, pos, lam):
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(pos)
    set_lambdas(ctx, lam)
    return ctx.getState(getEnergy=True).getPotentialEnergy().value_in_unit(_KJ)


def _chain_block_system(method, box=None):
    """env 0 ; block A = 1..5 (chain, atoms 1 and 5 charged -> a within-block 1-5 pair) ;
    block B = 6 (inert). Only the within-block 1-5 electrostatic pair is nonzero."""
    system = mm.System()
    if box is not None:
        system.setDefaultPeriodicBoxVectors(Vec3(box, 0, 0) * unit.nanometer,
                                            Vec3(0, box, 0) * unit.nanometer,
                                            Vec3(0, 0, box) * unit.nanometer)
    for _ in range(7):
        system.addParticle(12.0)
    bonds = [(1, 2), (2, 3), (3, 4), (4, 5)]
    q = [0, 1.0, 0, 0, 0, -1.0, 0]
    nbf = mm.NonbondedForce(); nbf.setNonbondedMethod(method)
    if method != mm.NonbondedForce.NoCutoff:
        nbf.setCutoffDistance(0.9 * unit.nanometer)
    for i in range(7):
        nbf.addParticle(q[i], 0.30, 0.0)
    nbf.createExceptionsFromBonds(bonds, 1.0, 1.0)     # 1-4 scale 1.0
    system.addForce(nbf)
    pos = [Vec3(0.30, 0.55, 0.30), Vec3(0.30, 0.30, 0.30), Vec3(0.45, 0.30, 0.30),
           Vec3(0.60, 0.30, 0.30), Vec3(0.75, 0.30, 0.30), Vec3(0.90, 0.30, 0.30),
           Vec3(0.30, 0.90, 0.30)] * unit.nanometer
    m = MSLDModel(7)
    m.add_block(site=1, atoms=[1, 2, 3, 4, 5])
    m.add_block(site=1, atoms=[6])
    m.finalize()
    return system, pos, m


def test_within_block_nocutoff_is_linear():
    system, pos, m = _chain_block_system(mm.NonbondedForce.NoCutoff)
    info = scale_msld_system(system, m)
    assert info["within_block_elec_corrections"] == ["MSLDWBElec_1"]   # block A corrected
    e1 = _energy(system, pos, [1, 1, 1])
    ehalf = _energy(system, pos, [1, 0.5, 1])
    assert abs(ehalf / e1 - 0.5) < 1e-6, ehalf / e1        # LINEAR, not 0.25


def test_within_block_pme_correction_is_exact_erfc():
    # under PME the reciprocal part is lambda^2 (BLaDE too); the correction fixes only the
    # real-space (erfc) part to linear. Verify the correction force contributes EXACTLY
    # (lambda - lambda^2) * [erfc(alpha r)/r Coulomb] for the within-block 1-5 pair.
    import math
    system, pos, m = _chain_block_system(mm.NonbondedForce.PME, box=2.5)
    scale_msld_system(system, m)
    corr = next(i for i, f in enumerate(system.getForces()) if f.getName() == "MSLDWBElec_1")
    system.getForce(corr).setForceGroup(11)

    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(pos); set_lambdas(ctx, [1, 0.5, 1])
    e_corr = ctx.getState(getEnergy=True, groups={11}).getPotentialEnergy().value_in_unit(_KJ)

    # expected: (0.5 - 0.25) * 138.935456 * q1*q5 * erfc(alpha*d)/d
    d = 0.60                                        # |atom1 - atom5| in nm
    rc = 0.9; alpha = math.sqrt(-math.log(2.0 * 5e-4)) / rc      # OpenMM default tol
    expected = 0.25 * 138.935456 * (1.0) * (-1.0) * math.erfc(alpha * d) / d
    assert abs(e_corr - expected) < 1e-4 * max(1.0, abs(expected)), (e_corr, expected)
    # and it strictly shifts the ratio above pure lambda^2 (0.25) toward linear
    ratio = _energy(system, pos, [1, 0.5, 1]) / _energy(system, pos, [1, 1, 1])
    assert ratio > 0.25 + 1e-4, ratio


def test_lambda_one_preserved():
    # the correction is zero at lambda=1, so lambda=1 must equal the base energy
    for method, box in [(mm.NonbondedForce.NoCutoff, None), (mm.NonbondedForce.PME, 2.5)]:
        system, pos, m = _chain_block_system(method, box=box)
        # base energy (no MSLD)
        base = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
        base.setPositions(pos)
        e_base = base.getState(getEnergy=True).getPotentialEnergy().value_in_unit(_KJ)
        scale_msld_system(system, m)
        e_one = _energy(system, pos, [1, 1, 1])
        assert abs(e_one - e_base) < 1e-4 * max(1.0, abs(e_base)), (method, e_one, e_base)


def test_small_block_gets_no_correction():
    # a 1-atom (or all-1-4) block has no within-block full pair -> no correction force
    system = mm.System()
    for _ in range(3):
        system.addParticle(12.0)
    nbf = mm.NonbondedForce(); nbf.setNonbondedMethod(mm.NonbondedForce.NoCutoff)
    for q in (1.0, 1.0, 0.0):
        nbf.addParticle(q, 0.3, 0.0)
    system.addForce(nbf)
    m = MSLDModel(3); m.add_block(site=1, atoms=[1]); m.add_block(site=1, atoms=[2]); m.finalize()
    info = scale_msld_system(system, m)
    assert info["within_block_elec_corrections"] == []


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nwithin-block electrostatics tests passed")
