"""The full assembled system at lambda=1 must reproduce
the pristine base System's ENERGY and FORCES.

Realistic single-site system exercising every scaled force type at once:
bonds, angles, torsions, PME electrostatics, LJ, 1-2/1-3 exclusions, and 1-4
exceptions. If the electrostatics/LJ/exception split introduced any error, the
lambda=1 energy or per-atom forces would disagree with the untouched base.

Topology (periodic box):
  env scaffold 0-1-2 ; block1={3,4} (bonded 2-3-4) ; block2={5} inert (bonded 0-5)
  block1 and block2 are both site 1 (block2 has zero charge/epsilon so same-site
  exclusion of (3,5)/(4,5) does not change the energy).
"""
import os
import sys

import numpy as np
import openmm as mm
from openmm import unit, Vec3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.model import MSLDModel
from msld.builder import build_msld_system, set_lambdas

_REF = mm.Platform.getPlatform("Reference")
_L = 3.0
_BONDS = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5)]


def make_system():
    charges = [0.3, -0.3, 0.4, -0.2, -0.2, 0.0]      # net 0; atom5 inert
    epsv = [0.4, 0.4, 0.4, 0.4, 0.4, 0.0]
    system = mm.System()
    system.setDefaultPeriodicBoxVectors(Vec3(_L, 0, 0) * unit.nanometer,
                                        Vec3(0, _L, 0) * unit.nanometer,
                                        Vec3(0, 0, _L) * unit.nanometer)
    for _ in range(6):
        system.addParticle(12.0)

    bond = mm.HarmonicBondForce()
    for i, j in _BONDS:
        bond.addBond(i, j, 0.15, 200000.0)
    system.addForce(bond)

    angle = mm.HarmonicAngleForce()
    for a in [(0, 1, 2), (1, 2, 3), (2, 3, 4), (1, 0, 5)]:   # no cross-block angles
        angle.addAngle(*a, 1.9, 400.0)
    system.addForce(angle)

    tor = mm.PeriodicTorsionForce()
    for t in [(0, 1, 2, 3), (1, 2, 3, 4), (2, 1, 0, 5)]:
        tor.addTorsion(*t, 2, 0.0, 8.0)
    system.addForce(tor)

    nbf = mm.NonbondedForce()
    nbf.setNonbondedMethod(mm.NonbondedForce.PME)
    nbf.setCutoffDistance(1.0 * unit.nanometer)
    nbf.setUseDispersionCorrection(False)
    for q, e in zip(charges, epsv):
        nbf.addParticle(q, 0.3, e)
    nbf.createExceptionsFromBonds(_BONDS, 0.8333, 0.5)
    system.addForce(nbf)

    # deliberately non-collinear (collinear torsion atoms give undefined forces)
    pos = [Vec3(0.50, 0.50, 0.50), Vec3(0.65, 0.53, 0.50), Vec3(0.80, 0.50, 0.51),
           Vec3(0.93, 0.60, 0.48), Vec3(1.06, 0.58, 0.55), Vec3(0.50, 0.65, 0.52)]
    return system, pos * unit.nanometer


def make_model():
    m = MSLDModel(6)
    m.add_block(site=1, atoms=[3, 4])
    m.add_block(site=1, atoms=[5])
    return m.finalize()


def _energy_forces(system, pos, lambdas=None):
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(pos)
    if lambdas is not None:
        set_lambdas(ctx, lambdas)
    st = ctx.getState(getEnergy=True, getForces=True)
    e = st.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
    f = st.getForces(asNumpy=True).value_in_unit(unit.kilojoule_per_mole / unit.nanometer)
    return e, np.array(f)


def test_master_recovers_base_energy_and_forces():
    base, pos = make_system()
    e_base, f_base = _energy_forces(base, pos)

    scaled, _ = make_system()
    info = build_msld_system(scaled, make_model())
    e_one, f_one = _energy_forces(scaled, pos, [1.0] * make_model().n_blocks)

    # energy
    assert abs(e_one - e_base) < 1e-4 * max(1.0, abs(e_base)), (e_one, e_base)
    # per-atom forces
    max_abs = np.abs(f_one - f_base).max()
    scale = max(1.0, np.abs(f_base).max())
    assert max_abs < 1e-3 * scale, (max_abs, scale)

    # sanity: partial lambda actually changes the energy (scaling is live)
    e_half, _ = _energy_forces(scaled, pos, [1.0, 0.5, 1.0])
    assert abs(e_half - e_base) > 1e-3 * max(1.0, abs(e_base)), (e_half, e_base)

    print("  base energy:", round(e_base, 4), "kJ/mol; max force diff:", max_abs)
    print("  info:", {k: v for k, v in info.items()})


def test_cmap_guard():
    # a CMAPTorsionForce touching an alchemical atom must be refused.
    system, _ = make_system()
    cmap = mm.CMAPTorsionForce()
    idx = cmap.addMap(2, [0.0, 0.0, 0.0, 0.0])          # 2x2 energy grid
    cmap.addTorsion(idx, 3, 4, 2, 1, 1, 2, 3, 4)        # involves alchemical atom 3/4
    system.addForce(cmap)
    try:
        build_msld_system(system, make_model())
        assert False, "expected CMAP NotImplementedError"
    except NotImplementedError as ex:
        assert "CMAP" in str(ex)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nmaster (N4) checks passed")
