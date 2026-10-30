"""P3.7: CHARMM tabulated LJ (NBFIX) block-scaling.

When a CHARMM system has NBFIX, ParmEd/OpenMM put ALL Lennard-Jones into a single
CustomNonbondedForce (acoef/bcoef lookup tables) and ZERO the NonbondedForce LJ. The
Amber-path add_scaled_lj then finds nothing. add_scaled_charmm_lj scales that tabulated
force instead, preserving NBFIX. Here we confirm:
  * the force field really is tabulated (a CustomNonbondedForce appears),
  * lambda=1 reproduces the base energy,
  * a single block's lambda scales its env<->block LJ (incl. an NBFIX pair) linearly,
  * dU/dlambda is analytic.

Layout: env atom 0 (type TE), block A = atom 1 (type TA), block B = atom 2 (type TZ, zero
LJ). NBFIX overrides the TE-TA pair (so the scaled interaction is an NBFIX one). No bonds
-> no exclusions; charges 0 -> energy is pure LJ.
"""
import os
import sys

import numpy as np
import openmm as mm
import parmed as pmd
from openmm import app, unit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.model import MSLDModel
from msld.builder import scale_msld_system, set_lambdas

_REF = mm.Platform.getPlatform("Reference")
_KJ = unit.kilojoule_per_mole


def _nbfix_structure():
    s = pmd.Structure()
    tE = pmd.AtomType("TE", 1, 12.0, 6); tE.set_lj_params(0.10, 1.70)
    tA = pmd.AtomType("TA", 2, 12.0, 6); tA.set_lj_params(0.10, 1.70)
    tZ = pmd.AtomType("TZ", 3, 12.0, 6); tZ.set_lj_params(0.00, 1.00)   # zero LJ
    tE.add_nbfix("TA", 3.6, 0.25); tA.add_nbfix("TE", 3.6, 0.25)         # NBFIX TE-TA
    for nm, at in [("TE", tE), ("TA", tA), ("TZ", tZ)]:
        a = pmd.Atom(name=nm, atomic_number=6, charge=0.0, mass=12.0, type=nm)
        a.atom_type = at
        s.add_atom(a, "RES", 1)
    s.coordinates = np.array([[0, 0, 0], [3.4, 0, 0], [0, 3.4, 0]], dtype=float)
    return s


def _energy_and_derivs(system, pos, lambdas):
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(pos)
    set_lambdas(ctx, lambdas)
    st = ctx.getState(getEnergy=True, getParameterDerivatives=True)
    e = st.getPotentialEnergy().value_in_unit(_KJ)
    d = {k: v for k, v in st.getEnergyParameterDerivatives().items()}
    return e, d


def _model(softcore_alpha=0.0):
    m = MSLDModel(3)
    m.softcore_alpha = softcore_alpha    # 0: the plain linear-lambda formulas below
    m.add_block(site=1, atoms=[1])       # block A (real LJ)
    m.add_block(site=1, atoms=[2])       # block B (zero LJ)
    return m.finalize()


def test_lj_is_tabulated():
    # sanity: NBFIX forces the LJ into a CustomNonbondedForce, NonbondedForce LJ zeroed
    s = _nbfix_structure()
    sysm = s.createSystem(nonbondedMethod=app.NoCutoff)
    assert any(isinstance(f, mm.CustomNonbondedForce) for f in sysm.getForces())
    nb = [f for f in sysm.getForces() if isinstance(f, mm.NonbondedForce)][0]
    assert all(nb.getParticleParameters(i)[2].value_in_unit(_KJ) == 0.0 for i in range(3))


def test_charmm_lj_recovers_base_and_scales():
    s = _nbfix_structure()
    pos = [mm.Vec3(*xyz) for xyz in (np.array(s.coordinates) / 10.0)] * unit.nanometer

    base = s.createSystem(nonbondedMethod=app.NoCutoff)
    e_base, _ = _energy_and_derivs(base, pos, [])
    assert abs(e_base) > 1e-6, e_base            # nonzero LJ (the TE-TA NBFIX pair)

    scaled = s.createSystem(nonbondedMethod=app.NoCutoff)
    model = _model()
    info = scale_msld_system(scaled, model)
    assert info["scaled_charmm_lj_forces"], "CHARMM LJ should have been scaled"

    # lambda = 1 reproduces base exactly
    e_one, _ = _energy_and_derivs(scaled, pos, [1.0, 1.0, 1.0])
    assert abs(e_one - e_base) < 1e-6 * max(1.0, abs(e_base)), (e_one, e_base)

    # lambda_A = 0.4 -> 0.4 * base (only the env<->A NBFIX pair is nonzero)
    e_part, d = _energy_and_derivs(scaled, pos, [1.0, 0.4, 1.0])
    assert abs(e_part - 0.4 * e_base) < 1e-6 * max(1.0, abs(e_base)), (e_part, 0.4 * e_base)
    # analytic dU/dlambda1 == base energy
    assert abs(d["lambda1"] - e_base) < 1e-6 * max(1.0, abs(e_base)), (d["lambda1"], e_base)


def test_amber_path_is_noop_on_plain_lj():
    # a plain (no-NBFIX) LJ system has no CustomNonbondedForce -> add_scaled_charmm_lj no-op
    from msld.forces import add_scaled_charmm_lj
    system = mm.System()
    for _ in range(3):
        system.addParticle(12.0)
    nbf = mm.NonbondedForce(); nbf.setNonbondedMethod(mm.NonbondedForce.NoCutoff)
    for _ in range(3):
        nbf.addParticle(0.0, 0.3, 0.5)
    system.addForce(nbf)
    m = _model()
    assert add_scaled_charmm_lj(system, m) == []


def test_charmm_lj_softcore_matches_beutler_form():
    # soft-core on the tabulated LJ: the env<->A NBFIX pair at lambda_A = L must follow
    # U = L * 4 eps (1/s^2 - 1/s), s = (r/sigma)^6 + alpha (1 - L), with sigma and eps the PAIR's
    # (NBFIX) values from its acoef/bcoef. lambda = 1 is still the base energy.
    s = _nbfix_structure()
    pos = [mm.Vec3(*xyz) for xyz in (np.array(s.coordinates) / 10.0)] * unit.nanometer
    base = s.createSystem(nonbondedMethod=app.NoCutoff)
    e_base, _ = _energy_and_derivs(base, pos, [])
    scaled = s.createSystem(nonbondedMethod=app.NoCutoff)
    alpha = 0.5
    scale_msld_system(scaled, _model(softcore_alpha=alpha))
    e_one, _ = _energy_and_derivs(scaled, pos, [1.0, 1.0, 1.0])
    assert abs(e_one - e_base) < 1e-6 * max(1.0, abs(e_base)), (e_one, e_base)

    sigma = 3.6 * 2 ** (-1 / 6) / 10.0                    # NBFIX Rmin 3.6 A -> sigma (nm)
    eps = 0.25 * 4.184                                     # kcal/mol -> kJ/mol
    r = 0.34
    for L in (0.4, 0.05):
        e, d = _energy_and_derivs(scaled, pos, [1.0, L, 1.0])
        sc = (r / sigma) ** 6 + alpha * (1 - L)
        ref = L * 4 * eps * (1 / sc ** 2 - 1 / sc)
        assert abs(e - ref) < 1e-6 * max(1.0, abs(ref)), (L, e, ref)
        h = 1e-6
        dref = ((L + h) * 4 * eps * (1 / ((r / sigma) ** 6 + alpha * (1 - L - h)) ** 2
                                     - 1 / ((r / sigma) ** 6 + alpha * (1 - L - h)))
                - (L - h) * 4 * eps * (1 / ((r / sigma) ** 6 + alpha * (1 - L + h)) ** 2
                                       - 1 / ((r / sigma) ** 6 + alpha * (1 - L + h)))) / (2 * h)
        assert abs(d["lambda1"] - dref) < 1e-5 * max(1.0, abs(dref)), (L, d["lambda1"], dref)


def test_charmm_lj_shares_exclusions_with_nonbonded_force():
    # the CPU/OpenCL/CUDA platforms need one exclusion set on every nonbonded force; the
    # tabulated LJ copies used to miss the same-site exclusions added to the NonbondedForce,
    # so a CHARMM/NBFIX MSLD System could only run on Reference.
    s = _nbfix_structure()
    pos = [mm.Vec3(*xyz) for xyz in (np.array(s.coordinates) / 10.0)] * unit.nanometer
    scaled = s.createSystem(nonbondedMethod=app.NoCutoff)
    scale_msld_system(scaled, _model(softcore_alpha=0.5))
    sets = []
    for f in scaled.getForces():
        if isinstance(f, mm.NonbondedForce):
            sets.append({tuple(sorted(f.getExceptionParameters(k)[:2]))
                         for k in range(f.getNumExceptions())})
        elif isinstance(f, mm.CustomNonbondedForce):
            sets.append({tuple(sorted(f.getExclusionParticles(k)))
                         for k in range(f.getNumExclusions())})
    assert (1, 2) in sets[0] and all(x == sets[0] for x in sets), sets
    ctx = mm.Context(scaled, mm.VerletIntegrator(0.001), mm.Platform.getPlatform("CPU"))
    ctx.setPositions(pos)
    ctx.getState(getEnergy=True)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nCHARMM NBFIX LJ tests passed")
