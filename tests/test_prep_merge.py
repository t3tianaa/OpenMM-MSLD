"""P2: the merge engine + the end-state gate.

The key correctness test of the whole builder:

    take two per-variant systems that SHARE an environment, merge them into one
    combined system, apply MSLD scaling, and check that with ONE variant fully on
    (its lambda = 1, the other 0) the combined energy reproduces the independently
    built single-variant system.

If that holds for BOTH variants, the merge transplanted each block's atoms and bonded
terms correctly, and the "off" block does not perturb the physics.

Toy (per variant, 4 atoms): shared env chain 0-1-2, one block atom 3 bonded to atom 2.
  env atoms 0,1,2 are IDENTICAL across variants (same charges, LJ, geometry).
  block atom differs (charge / LJ / position).
"""
import os
import sys

import numpy as np
import openmm as mm
from openmm import app, unit, Vec3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import parmed as pmd
from msld.prep import VariantInput, merge_variants, model_from_mappings
from msld.builder import build_msld_system, set_lambdas

_REF = mm.Platform.getPlatform("Reference")
_NM = unit.nanometer
_KJ = unit.kilojoule_per_mole

# shared environment: atoms 0,1,2 identical in every variant
_ENV_CHARGE = [0.30, -0.20, 0.10]
_ENV_EPS = [0.40, 0.40, 0.40]
_ENV_POS = [Vec3(0.0, 0.0, 0.0), Vec3(0.15, 0.0, 0.0), Vec3(0.28, 0.10, 0.0)]
_SIG = 0.30
_BONDS = [(0, 1), (1, 2), (2, 3)]          # env chain + block atom 3


def _variant_structure(block_charge, block_eps, block_pos):
    """A 4-atom OpenMM system (env 0-1-2 + block atom 3) -> ParmEd Structure."""
    charges = _ENV_CHARGE + [block_charge]
    epsv = _ENV_EPS + [block_eps]
    pos = _ENV_POS + [block_pos]

    system = mm.System()
    for _ in range(4):
        system.addParticle(12.0)
    hbf = mm.HarmonicBondForce()
    for i, j in _BONDS:
        hbf.addBond(i, j, 0.15, 200000.0)
    system.addForce(hbf)
    haf = mm.HarmonicAngleForce()
    for a in [(0, 1, 2), (1, 2, 3)]:
        haf.addAngle(*a, 1.9, 300.0)
    system.addForce(haf)
    nbf = mm.NonbondedForce()
    nbf.setNonbondedMethod(mm.NonbondedForce.NoCutoff)
    for q, e in zip(charges, epsv):
        nbf.addParticle(q, _SIG, e)
    nbf.createExceptionsFromBonds(_BONDS, 0.8333, 0.5)
    system.addForce(nbf)

    top = app.Topology()
    ch = top.addChain()
    res = top.addResidue("RES", ch)
    ats = [top.addAtom(f"A{i}", app.Element.getByAtomicNumber(6), res) for i in range(4)]
    for i, j in _BONDS:
        top.addBond(ats[i], ats[j])

    xyz_ang = np.array([[p.x, p.y, p.z] for p in pos]) * 10.0     # nm -> angstrom
    st = pmd.openmm.load_topology(top, system=system, xyz=xyz_ang)
    return st, system, pos


def _energy(system, pos, lambdas=None):
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(pos)
    if lambdas is not None:
        set_lambdas(ctx, lambdas)
    return ctx.getState(getEnergy=True).getPotentialEnergy().value_in_unit(_KJ)


def test_merge_end_state_reproduces_single_variant():
    # two variants sharing env; block atom differs
    stA, sysA, posA = _variant_structure(block_charge=-0.20, block_eps=0.50,
                                         block_pos=Vec3(0.40, 0.05, 0.10))
    stB, sysB, posB = _variant_structure(block_charge=0.05, block_eps=0.30,
                                         block_pos=Vec3(0.39, -0.06, 0.08))

    A = VariantInput("A", stA, env_indices=[0, 1, 2])
    B = VariantInput("B", stB, env_indices=[0, 1, 2])
    merged = merge_variants([A, B])

    # combined: env 0,1,2 + blockA=3 + blockB=4
    assert len(merged.structure.atoms) == 5
    assert merged.mapping.env_atoms == {0, 1, 2}
    assert merged.mapping.blocks == {"A": {3}, "B": {4}}

    combined = merged.structure.createSystem(nonbondedMethod=app.NoCutoff)
    # positions of the combined system, in nm
    comb_pos = (np.array(merged.structure.coordinates) / 10.0).tolist()
    comb_pos = [Vec3(*xyz) for xyz in comb_pos] * _NM

    model = model_from_mappings(5, [merged.mapping], add_restraints=False)
    build_msld_system(combined, model)

    # independent single-variant reference energies
    eA_ref = _energy(sysA, posA * _NM)
    eB_ref = _energy(sysB, posB * _NM)

    # combined with A fully on (lambda: env=1 unused, A=1, B=0)
    eA_on = _energy(combined, comb_pos, [1.0, 1.0, 0.0])
    eB_on = _energy(combined, comb_pos, [1.0, 0.0, 1.0])

    assert abs(eA_on - eA_ref) < 1e-4 * max(1.0, abs(eA_ref)), (eA_on, eA_ref)
    assert abs(eB_on - eB_ref) < 1e-4 * max(1.0, abs(eB_ref)), (eB_on, eB_ref)

    # sanity: the two end states differ (the block really changed the physics)
    assert abs(eA_ref - eB_ref) > 1e-3
    print(f"  A on={eA_on:.5f} ref={eA_ref:.5f}   B on={eB_on:.5f} ref={eB_ref:.5f}")


def test_off_block_does_not_perturb():
    # with A on, adding block B (off) must not change the energy vs a merge of A alone-ish:
    # check that A-on energy equals the standalone A energy exactly (already above), and
    # that switching B fully off is what makes it match (B on would differ).
    stA, sysA, posA = _variant_structure(-0.20, 0.50, Vec3(0.40, 0.05, 0.10))
    stB, sysB, posB = _variant_structure(0.05, 0.30, Vec3(0.39, -0.06, 0.08))
    merged = merge_variants([VariantInput("A", stA, [0, 1, 2]),
                             VariantInput("B", stB, [0, 1, 2])])
    combined = merged.structure.createSystem(nonbondedMethod=app.NoCutoff)
    comb_pos = [Vec3(*xyz) for xyz in (np.array(merged.structure.coordinates) / 10.0)] * _NM
    model = model_from_mappings(5, [merged.mapping], add_restraints=False)
    build_msld_system(combined, model)

    eA_ref = _energy(sysA, posA * _NM)
    e_Aon_Boff = _energy(combined, comb_pos, [1.0, 1.0, 0.0])
    e_Aon_Bon = _energy(combined, comb_pos, [1.0, 1.0, 1.0])
    assert abs(e_Aon_Boff - eA_ref) < 1e-4 * max(1.0, abs(eA_ref))
    assert abs(e_Aon_Bon - eA_ref) > 1e-3        # B on DOES change things


def test_merge_averages_differing_env_charge():
    # Amber-like: the two variants disagree on a backbone (env) charge -> merge should
    # give that shared atom the average, and warn.
    import warnings

    # variant A: env atom 1 charge -0.20 ; variant B: env atom 1 charge 0.00
    stA, _, _ = _variant_structure(block_charge=-0.20, block_eps=0.50,
                                   block_pos=Vec3(0.40, 0.05, 0.10))
    stB, _, _ = _variant_structure(block_charge=0.05, block_eps=0.30,
                                   block_pos=Vec3(0.39, -0.06, 0.08))
    stB.atoms[1].charge = 0.00                     # perturb a shared env atom in B only
    # A's env atom 1 keeps the base value from _ENV_CHARGE[1] = -0.20

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        merged = merge_variants([VariantInput("A", stA, [0, 1, 2]),
                                 VariantInput("B", stB, [0, 1, 2])])

    # shared env atom 1 now carries the average of -0.20 and 0.00 = -0.10
    assert abs(merged.structure.atoms[1].charge - (-0.10)) < 1e-9
    assert merged.env_charge_report is not None
    assert len(merged.env_charge_report.differing) == 1
    assert any("average" in str(w.message) for w in caught)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nP2 prep-merge tests passed")
