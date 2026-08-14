"""CHARMM-specific term types (harmonic impropers + Urey-Bradley).

CHARMM force fields add two term types Amber lacks:
  * harmonic impropers  -> OpenMM CustomTorsionForce  (needs add_scaled_impropers)
  * Urey-Bradley (1-3)  -> a second HarmonicBondForce (already scaled by add_scaled_bonds)
"""
import os
import sys

import numpy as np
import openmm as mm
from openmm import app, unit, Vec3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import parmed as pmd
from msld.model import MSLDModel
from msld.builder import build_msld_system, set_lambdas

_REF = mm.Platform.getPlatform("Reference")
_KJ = unit.kilojoule_per_mole


def _energy_and_derivs(system, positions, lambdas):
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(positions)
    set_lambdas(ctx, lambdas)
    st = ctx.getState(getEnergy=True, getParameterDerivatives=True)
    e = st.getPotentialEnergy().value_in_unit(_KJ)
    d = {k: v for k, v in st.getEnergyParameterDerivatives().items()}
    return e, d


def _check(system, pos, model, lam_partial, factor, deriv_checks):
    build_msld_system(system, model)
    e1, _ = _energy_and_derivs(system, pos, [1.0] * model.n_blocks)
    assert e1 > 1e-6, f"base term energy ~0 ({e1})"
    ep, d = _energy_and_derivs(system, pos, lam_partial)
    assert abs(ep - factor * e1) < 1e-6 * max(1.0, abs(e1)), (ep, factor * e1)
    for name, cof in deriv_checks.items():
        assert abs(d[name] - cof * e1) < 1e-6 * max(1.0, abs(e1)), (name, d[name], cof * e1)


# ------------------------------------------------------------- impropers
def test_improper_single_lambda():
    # env 0,1,2 ; site1: A={3}, B={4}. improper (0,1,2,3) -> single lambda1
    system = mm.System()
    for _ in range(5):
        system.addParticle(12.0)
    ctf = mm.CustomTorsionForce("k*(theta-theta0)^2")   # harmonic improper shape
    ctf.addPerTorsionParameter("k")
    ctf.addPerTorsionParameter("theta0")
    ctf.addTorsion(0, 1, 2, 3, [200.0, 0.0])
    system.addForce(ctf)
    pos = [Vec3(0, 0, 0), Vec3(0.1, 0, 0), Vec3(0.1, 0.1, 0),
           Vec3(0.2, 0.1, 0.1), Vec3(0.3, 0, 0)] * unit.nanometer
    m = MSLDModel(5)
    m.add_block(site=1, atoms=[3])
    m.add_block(site=1, atoms=[4])
    m.finalize()
    _check(system, pos, m, [1.0, 0.4, 1.0], 0.4, {"lambda1": 1.0})


def test_improper_product_lambda():
    # site1: A={2},B={3}; site2: C={4},D={5}. improper (2,0,1,4) -> lambda1*lambda3
    system = mm.System()
    for _ in range(6):
        system.addParticle(12.0)
    ctf = mm.CustomTorsionForce("k*(theta-theta0)^2")
    ctf.addPerTorsionParameter("k")
    ctf.addPerTorsionParameter("theta0")
    ctf.addTorsion(2, 0, 1, 4, [200.0, 0.0])
    system.addForce(ctf)
    pos = [Vec3(0, 0, 0), Vec3(0.1, 0, 0), Vec3(0.1, 0.1, 0.05),
           Vec3(0.2, 0.1, 0), Vec3(0.0, 0.1, 0.1), Vec3(0.2, 0.2, 0)] * unit.nanometer
    m = MSLDModel(6)
    m.add_block(site=1, atoms=[2])
    m.add_block(site=1, atoms=[3])
    m.add_block(site=2, atoms=[4])
    m.add_block(site=2, atoms=[5])
    m.finalize()
    _check(system, pos, m, [1.0, 0.4, 1.0, 0.6, 1.0], 0.4 * 0.6,
           {"lambda1": 0.6, "lambda3": 0.4})


def test_env_improper_left_unscaled():
    # an improper on env-only atoms must stay (unscaled), not become an MSLD force
    system = mm.System()
    for _ in range(5):
        system.addParticle(12.0)
    ctf = mm.CustomTorsionForce("k*(theta-theta0)^2")
    ctf.addPerTorsionParameter("k")
    ctf.addPerTorsionParameter("theta0")
    ctf.addTorsion(0, 1, 2, 0, [200.0, 0.0])       # all env atoms
    system.addForce(ctf)
    m = MSLDModel(5)
    m.add_block(site=1, atoms=[3])
    m.add_block(site=1, atoms=[4])
    m.finalize()
    info = build_msld_system(system, m)
    assert info["scaled_improper_forces"] == []     # nothing alchemical -> untouched
    assert any(isinstance(f, mm.CustomTorsionForce) for f in system.getForces())


# ------------------------------------------------------------- Urey-Bradley
def test_urey_bradley_second_bondforce_scales():
    # two HarmonicBondForce: [0] a real bond (env-env, at r0 -> 0 energy),
    #                        [1] a "Urey-Bradley" 1-3 (env-block1, deviated -> nonzero)
    system = mm.System()
    for _ in range(4):
        system.addParticle(12.0)
    real = mm.HarmonicBondForce(); real.setName("bonds")
    real.addBond(0, 1, 0.15, 1000.0)                # placed exactly at r0 -> 0
    system.addForce(real)
    ub = mm.HarmonicBondForce(); ub.setName("ureybradley")
    ub.addBond(0, 2, 0.20, 800.0)                   # env(0)-block1(2), deviated
    system.addForce(ub)
    pos = [Vec3(0, 0, 0), Vec3(0.15, 0, 0), Vec3(0.30, 0, 0), Vec3(0.0, 0.5, 0)] * unit.nanometer
    m = MSLDModel(4)
    m.add_block(site=1, atoms=[2])
    m.add_block(site=1, atoms=[3])
    m.finalize()
    # only the UB term is nonzero, and it is env<->block1 -> scales by lambda1
    _check(system, pos, m, [1.0, 0.4, 1.0], 0.4, {"lambda1": 1.0})


# ------------------------------------------------------- ParmEd round-trip
def _charmm_like_structure():
    """5-atom ParmEd Structure with a real UB and a real harmonic improper touching a
    block atom, built the way ParmEd represents CHARMM."""
    s = pmd.Structure()
    for i in range(5):
        a = pmd.Atom(name=f"A{i}", atomic_number=6, charge=0.05 * (1 if i % 2 else -1),
                     mass=12.0, type=f"CT{i}")
        at = pmd.AtomType(f"CT{i}", i + 1, 12.0, 6)
        at.set_lj_params(0.10, 1.6)
        a.atom_type = at; a.epsilon = 0.10; a.rmin = 1.6
        s.add_atom(a, "RES", 1)
    bt = pmd.BondType(300.0, 1.5); s.bond_types.append(bt)
    for i, j in [(0, 1), (1, 2), (2, 3), (2, 4)]:
        s.bonds.append(pmd.Bond(s.atoms[i], s.atoms[j], type=bt))
    angt = pmd.AngleType(50.0, 110.0); s.angle_types.append(angt)
    # no (3,2,4) angle: that would span both same-site blocks (cross-variant, illegal)
    for a in [(0, 1, 2), (1, 2, 3), (1, 2, 4)]:
        s.angles.append(pmd.Angle(s.atoms[a[0]], s.atoms[a[1]], s.atoms[a[2]], type=angt))
    ubt = pmd.BondType(40.0, 2.5); s.urey_bradley_types.append(ubt)
    s.urey_bradleys.append(pmd.UreyBradley(s.atoms[1], s.atoms[3], type=ubt))   # env-block
    it = pmd.ImproperType(20.0, 0.0); s.improper_types.append(it)
    s.impropers.append(pmd.Improper(s.atoms[0], s.atoms[1], s.atoms[2], s.atoms[3], type=it))
    s.coordinates = np.array([[0, 0, 0], [1.5, 0, 0], [2.8, 1.0, 0],
                              [4.0, 0.6, 0.8], [2.9, 1.2, -1.3]], dtype=float)
    return s


def test_charmm_recovers_base():
    st = _charmm_like_structure()
    pos = (np.array(st.coordinates) / 10.0)
    pos = [Vec3(*xyz) for xyz in pos] * unit.nanometer

    base = st.createSystem(nonbondedMethod=app.NoCutoff)
    e_base = _energy_and_derivs(base, pos, [])[0]

    scaled = st.createSystem(nonbondedMethod=app.NoCutoff)
    m = MSLDModel(5)
    m.add_block(site=1, atoms=[3])
    m.add_block(site=1, atoms=[4])
    m.finalize()
    info = build_msld_system(scaled, m)
    assert info["scaled_improper_forces"], "improper should have been scaled"
    e_one = _energy_and_derivs(scaled, pos, [1.0, 1.0, 1.0])[0]
    assert abs(e_one - e_base) < 1e-4 * max(1.0, abs(e_base)), (e_one, e_base)

    # partial lambda must actually change the energy (scaling is live)
    e_half = _energy_and_derivs(scaled, pos, [1.0, 0.5, 1.0])[0]
    assert abs(e_half - e_base) > 1e-3 * max(1.0, abs(e_base))
    print("  base:", round(e_base, 4), " lambda=1:", round(e_one, 4),
          " impropers:", info["scaled_improper_forces"])


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nCHARMM-term (improper + Urey-Bradley) tests passed")
