"""use_plugin: MSLDNonbondedForce (t3tianaa/openmm-ld) in place of the stock nonbonded forces.

Against the NumPy oracle (NoCutoff toy, the tolerance allows for the oracle's rounded Coulomb
constant) and against the stock build of the same system: PME, reaction field and CHARMM tabulated
LJ with NBFIX, in a periodic box. Skipped unless msldplugin is importable; see msld/plugin.py.
"""
import json
import math
import os
import sys

import numpy as np
import openmm as mm
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
pytest.importorskip("msldplugin")
from msld.builder import scale_msld_system, set_lambdas
from msld.integrator import LambdaDynamics
from msld.model import MSLDModel
from msld.plugin import PLUGIN_FORCE_NAME, load_msldplugin
from test_oracle_partial_lambda import _build, _close, _random_thetas

load_msldplugin()
_REF = mm.Platform.getPlatform("Reference")
_FIXTURE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "oracle_toy.json")
BOX, CUTOFF, SWITCH = 3.2, 1.0, 0.85
NBFIX_TYPES = 3
NBFIX = {(0, 1): (0.27, 0.9), (1, 2): (0.36, 0.12)}


def test_plugin_matches_oracle_without_finite_difference():
    oracle, model, ctx = _build(seed=1, use_plugin=True)
    names = [f.getName() for f in ctx.getSystem().getForces()]
    assert names.count(PLUGIN_FORCE_NAME) == 1
    assert not any(isinstance(f, (mm.NonbondedForce, mm.CustomNonbondedForce))
                   for f in ctx.getSystem().getForces())
    dyn = LambdaDynamics(ctx, model, temperature=300.0, seed=0)
    assert dyn._uses_plugin and not dyn._has_fd
    rng = np.random.default_rng(7)
    for th in _random_thetas(rng, 8):
        dyn.theta = list(th)
        lam = np.array(dyn.project())
        e_ref = float(np.real(oracle.energy(lam)))
        assert abs(dyn.potential_energy() - e_ref) <= 5e-8 * max(1.0, abs(e_ref))
        d, _ = dyn.dUdlambda(lam=list(lam))
        assert _close(d[1:], oracle.dU_dlambda(lam)[1:], 5e-8), (lam, d)


def test_injected_lambda_force_keeps_the_finite_difference():
    _, model, ctx0 = _build(seed=1, use_plugin=True)
    lam = [1.0] * model.n_blocks
    d0, _ = LambdaDynamics(ctx0, model, temperature=300.0, seed=0).dUdlambda(lam=lam)
    _, model, ctx = _build(seed=1, use_plugin=True)
    system = ctx.getSystem()
    f = mm.CustomExternalForce("lambda1*2.5")
    f.addGlobalParameter("lambda1", 1.0)
    f.addParticle(0, [])
    system.addForce(f)
    ctx.reinitialize(preserveState=True)
    dyn = LambdaDynamics(ctx, model, temperature=300.0, seed=0)
    assert dyn._has_fd
    d1, _ = dyn.dUdlambda(lam=lam)
    assert abs(d1[1] - d0[1] - 2.5) < 1e-6


def _base_system(spec, method, nbfix):
    n = len(spec["positions"])
    system = mm.System()
    system.setDefaultPeriodicBoxVectors(mm.Vec3(BOX, 0, 0), mm.Vec3(0, BOX, 0), mm.Vec3(0, 0, BOX))
    for _ in range(n):
        system.addParticle(12.0)
    nbf = mm.NonbondedForce()
    nbf.setNonbondedMethod(method)
    nbf.setCutoffDistance(CUTOFF)
    nbf.setUseSwitchingFunction(method != mm.NonbondedForce.NoCutoff)
    nbf.setSwitchingDistance(SWITCH)
    nbf.setEwaldErrorTolerance(1e-5)
    nbf.setUseDispersionCorrection(False)
    for i in range(n):
        if nbfix:
            nbf.addParticle(spec["charge"][i], 1.0, 0.0)
        else:
            nbf.addParticle(spec["charge"][i], spec["sigma"][i], spec["epsilon"][i])
    pairs14 = {(min(i, j), max(i, j)): (qq, s, e) for i, j, qq, s, e in spec["pairs14"]}
    excluded = sorted({(min(i, j), max(i, j)) for i, j in spec["excluded"]})
    for i, j in excluded:
        nbf.addException(i, j, *pairs14.get((i, j), (0.0, 0.1, 0.0)))
    system.addForce(nbf)
    if nbfix:     # as ParmEd: U = (a/r^6)^2 - b/r^6
        tp = [(0.30, 0.5), (0.32, 0.3), (0.28, 0.7)]
        acoef, bcoef = [0.0] * NBFIX_TYPES ** 2, [0.0] * NBFIX_TYPES ** 2
        for t1 in range(NBFIX_TYPES):
            for t2 in range(NBFIX_TYPES):
                s, e = NBFIX.get((min(t1, t2), max(t1, t2)),
                                 (0.5 * (tp[t1][0] + tp[t2][0]), math.sqrt(tp[t1][1] * tp[t2][1])))
                acoef[t1 + NBFIX_TYPES * t2] = math.sqrt(4 * e * s ** 12)
                bcoef[t1 + NBFIX_TYPES * t2] = 4 * e * s ** 6
        lj = mm.CustomNonbondedForce("(a/r6)^2-b/r6; r6=r^6; a=acoef(type1, type2); b=bcoef(type1, type2)")
        lj.addTabulatedFunction("acoef", mm.Discrete2DFunction(NBFIX_TYPES, NBFIX_TYPES, acoef))
        lj.addTabulatedFunction("bcoef", mm.Discrete2DFunction(NBFIX_TYPES, NBFIX_TYPES, bcoef))
        lj.addPerParticleParameter("type")
        for i in range(n):
            lj.addParticle([float(i % NBFIX_TYPES)])
        for i, j in excluded:
            lj.addExclusion(i, j)
        cn = mm.CustomNonbondedForce
        lj.setNonbondedMethod(cn.NoCutoff if method == mm.NonbondedForce.NoCutoff else
                              cn.CutoffNonPeriodic if method == mm.NonbondedForce.CutoffNonPeriodic
                              else cn.CutoffPeriodic)
        lj.setCutoffDistance(CUTOFF)
        lj.setUseSwitchingFunction(method != mm.NonbondedForce.NoCutoff)
        lj.setSwitchingDistance(SWITCH)
        system.addForce(lj)
    bonds = mm.HarmonicBondForce()
    for i, j, r0, k in spec["bonds"]:
        bonds.addBond(i, j, r0, k)
    system.addForce(bonds)
    return system


def _evaluate(spec, method, nbfix, use_plugin, lam):
    n = len(spec["positions"])
    model = MSLDModel(n, fnex=spec["fnex"])
    model.softcore_alpha, model.softcore_sigma_q = spec["alpha"], spec["sigma_q"]
    for b in range(1, len(spec["block_site"])):
        model.add_block(site=spec["block_site"][b], atoms=[i for i in range(n) if spec["atom_block"][i] == b])
    model.finalize()
    model.use_plugin = use_plugin
    system = _base_system(spec, method, nbfix)
    model.scale_system(system)
    x = np.asarray(spec["positions"])
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(x - x.mean(axis=0) + 0.5 * BOX)
    dyn = LambdaDynamics(ctx, model, temperature=300.0, seed=0)
    set_lambdas(ctx, lam)
    d, _ = dyn.dUdlambda(lam=list(lam))
    st = ctx.getState(getEnergy=True, getForces=True)
    return (st.getPotentialEnergy()._value, np.array(d),
            np.array(st.getForces(asNumpy=True)._value), dyn)


NB = mm.NonbondedForce


@pytest.mark.parametrize("method,nbfix", [(NB.NoCutoff, False), (NB.CutoffNonPeriodic, False),
                                          (NB.CutoffPeriodic, False), (NB.PME, False),
                                          (NB.NoCutoff, True), (NB.PME, True)],
                         ids=["NoCutoff", "RF-nonperiodic", "RF-periodic", "PME", "NBFIX-NoCutoff", "NBFIX-PME"])
def test_plugin_matches_stock_build(method, nbfix):
    with open(_FIXTURE) as fh:
        system0 = json.load(fh)["systems"][0]
    spec = system0["spec"]
    for case in system0["cases"]:
        lam = case["lam"]
        e0, d0, f0, _ = _evaluate(spec, method, nbfix, False, lam)
        e1, d1, f1, dyn = _evaluate(spec, method, nbfix, True, lam)
        assert dyn._uses_plugin and not dyn._has_fd
        assert abs(e1 - e0) <= 1e-7 * max(1.0, abs(e0)), (e1, e0)
        assert _close(d1[1:], d0[1:], 1e-7), (d1, d0)
        assert np.max(np.abs(f1 - f0)) <= 1e-6 * max(1.0, np.max(np.abs(f0)))


def test_switch_off_is_the_default():
    model = MSLDModel(2)
    assert model.use_plugin is False


def test_plugin_rejects_cross_site_14():
    system = mm.System()
    for _ in range(4):
        system.addParticle(12.0)
    nbf = mm.NonbondedForce()
    for _ in range(4):
        nbf.addParticle(0.1, 0.3, 0.5)
    nbf.addException(0, 2, 0.01, 0.3, 0.2)
    system.addForce(nbf)
    m = MSLDModel(4)
    m.add_block(site=1, atoms=[0]); m.add_block(site=1, atoms=[1])
    m.add_block(site=2, atoms=[2]); m.add_block(site=2, atoms=[3])
    m.finalize()
    with pytest.raises(NotImplementedError):
        scale_msld_system(system, m, use_plugin=True)
