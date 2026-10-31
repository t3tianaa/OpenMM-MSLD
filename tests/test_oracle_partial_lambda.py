"""Partial-lambda energies and dU/dlambda of the scaled OpenMM System vs the independent NumPy
oracle (tests/msld_oracle.py). FEAT-045 / TASK-067, closes the "only lambda = 1 is tested" gap
(ISS-012) and is the correctness target for the C++ plugin (ADR-0035).

Toy: a 6-atom environment chain with two sites, 3 blocks at site 1 (5-, 5- and 3-atom chains, so
within-block 1-5+ pairs exist) and 2 at site 2 (2- and 3-atom chains). Bonds, angles, torsions,
1-4s, every nonbonded pair kind (env-env, env-block, within-block, cross-site, same-site excluded),
fixed and variable biases (types 6, 8, 10) and a restraint group. NoCutoff, Reference platform.
"""
import math
import os
import sys

import numpy as np
import openmm as mm
import pytest
from openmm import unit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from msld.model import MSLDModel
from msld.builder import scale_msld_system, set_lambdas
from msld.integrator import LambdaDynamics
from msld_oracle import Oracle

_REF = mm.Platform.getPlatform("Reference")
_KJ = unit.kilojoule_per_mole

# topology ---------------------------------------------------------------------------------------
ENV = list(range(6))                                     # chain 0-1-2-3-4-5
BLOCKS = {1: (1, [6, 7, 8, 9, 10], 2),                   # block: (site, atoms (chain), anchor)
          2: (1, [11, 12, 13, 14, 15], 2),
          3: (1, [16, 17, 18], 2),
          4: (2, [19, 20], 4),
          5: (2, [21, 22, 23], 4)}
N = 24
SCALE14_Q, SCALE14_LJ = 1.0 / 1.2, 0.5


def _topology():
    bonds = [(i, i + 1) for i in range(5)]
    for _, (_, atoms, anchor) in BLOCKS.items():
        bonds.append((anchor, atoms[0]))
        bonds += [(atoms[k], atoms[k + 1]) for k in range(len(atoms) - 1)]
    atom_block = [0] * N
    for b, (_, atoms, _) in BLOCKS.items():
        for a in atoms:
            atom_block[a] = b
    site = {0: 0, **{b: v[0] for b, v in BLOCKS.items()}}

    def same_site_cross(atoms):
        bs = {atom_block[a] for a in atoms if atom_block[a]}
        return len({site[b] for b in bs}) < len(bs)

    adj = {i: set() for i in range(N)}
    for i, j in bonds:
        adj[i].add(j); adj[j].add(i)
    # simple paths of 2 and 3 bonds; a path through two blocks of one site is not a real term
    angles, torsions = set(), set()
    for j in range(N):
        for i in adj[j]:
            for l in adj[j]:
                if i < l and not same_site_cross((i, j, l)):
                    angles.add((i, j, l))
    for j, l in bonds:
        for i in adj[j] - {l}:
            for m in adj[l] - {j}:
                if i != m and not same_site_cross((i, j, l, m)):
                    torsions.add((i, j, l, m))
    p12 = {(min(a), max(a)) for a in bonds}
    p13 = {(min(i, l), max(i, l)) for i, _, l in angles}
    p14 = {(min(i, m), max(i, m)) for i, _, _, m in torsions} - p12 - p13
    return bonds, sorted(angles), sorted(torsions), atom_block, site, p12 | p13, sorted(p14)


def _positions(rng, overlap=False):
    """Random chain geometry (bond 0.15 nm, ~110 degree angles); blocks of one site overlap."""
    x = np.zeros((N, 3))

    def grow(prev2, prev, new):
        while True:
            d = rng.normal(size=3)
            d /= np.linalg.norm(d)
            if prev2 is not None:
                u = x[prev2] - x[prev]
                u /= np.linalg.norm(u)
                if np.dot(u, d) > -0.1:                 # keep the angle obtuse (> ~95 degrees)
                    continue
            x[new] = x[prev] + 0.15 * d
            return

    x[0] = [1.0, 1.0, 1.0]
    grow(None, 0, 1)
    for i in range(2, 6):
        grow(i - 2, i - 1, i)
    for _, (_, atoms, anchor) in BLOCKS.items():
        grow(anchor - 1, anchor, atoms[0])
        for k in range(1, len(atoms)):
            grow(atoms[k - 2] if k >= 2 else anchor, atoms[k - 1], atoms[k])
    if overlap:                                         # env atom 0 sits on block 4's last atom
        x[0] = x[20] + np.array([0.0, 0.0, 0.01])
    return x


def _build(seed=0, alpha=0.5, overlap=False):
    rng = np.random.default_rng(seed)
    bonds, angles, torsions, atom_block, site, excl, p14 = _topology()
    q = rng.uniform(-0.5, 0.5, N)
    sig = rng.uniform(0.25, 0.35, N)
    eps = rng.uniform(0.2, 0.8, N)
    x = _positions(rng, overlap)

    bpar = [(i, j, 0.15 + 0.01 * rng.normal(), rng.uniform(2e4, 4e4)) for i, j in bonds]
    apar = [(i, j, l, rng.uniform(1.8, 2.0), rng.uniform(300, 500)) for i, j, l in angles]
    tpar = [(i, j, l, m, int(rng.integers(1, 4)), rng.uniform(0, math.pi), rng.uniform(0.5, 5))
            for i, j, l, m in torsions]
    pairs14 = [(i, j, SCALE14_Q * q[i] * q[j], 0.5 * (sig[i] + sig[j]),
                SCALE14_LJ * math.sqrt(eps[i] * eps[j])) for i, j in p14]
    fixed_bias = [0.0] + list(rng.uniform(-20, 20, 5))
    vbias = [(1, 2, 6, 0.0, 7.5), (2, 3, 6, 0.0, -4.0), (1, 3, 8, 0.017, 2.5),
             (3, 1, 10, -5.56, -1.5), (4, 5, 6, 0.0, 3.0), (5, 4, 8, 0.017, -2.0)]
    restraints = [([6, 7, 8], 500.0)]

    spec = dict(positions=x, charge=q, sigma=sig, epsilon=eps, atom_block=atom_block,
                block_site=[site[b] for b in range(6)], bonds=bpar, angles=apar, torsions=tpar,
                pairs14=pairs14, excluded=excl | set(p14), alpha=alpha, sigma_q=0.3,
                fixed_bias=fixed_bias, variable_biases=vbias, restraints=restraints, fnex=5.5)

    # the same physics as a plain OpenMM System, then MSLD-scaled by the engine
    system = mm.System()
    for _ in range(N):
        system.addParticle(12.0)
    nbf = mm.NonbondedForce()
    nbf.setNonbondedMethod(mm.NonbondedForce.NoCutoff)
    for i in range(N):
        nbf.addParticle(q[i], sig[i], eps[i])
    for i, j in sorted(excl):
        nbf.addException(i, j, 0.0, 0.1, 0.0)
    for i, j, qq, s14, e14 in pairs14:
        nbf.addException(i, j, qq, s14, e14)
    system.addForce(nbf)
    hb = mm.HarmonicBondForce()
    for i, j, r0, k in bpar:
        hb.addBond(i, j, r0, k)
    system.addForce(hb)
    ha = mm.HarmonicAngleForce()
    for i, j, l, t0, k in apar:
        ha.addAngle(i, j, l, t0, k)
    system.addForce(ha)
    pt = mm.PeriodicTorsionForce()
    for i, j, l, m, n, ph, k in tpar:
        pt.addTorsion(i, j, l, m, n, ph, k)
    system.addForce(pt)

    model = MSLDModel(N, fnex=5.5)
    model.softcore_alpha = alpha
    model.softcore_sigma_q = 0.3
    for b in range(1, 6):
        model.add_block(site=site[b], atoms=BLOCKS[b][1], lambda_bias=fixed_bias[b])
    for i, j, typ, l0, k in vbias:
        model.add_variable_bias(i, j, type=typ, l0=l0, k=k, n=0)
    for atoms, k in restraints:
        model.add_atom_restraint(atoms)
    model.k_restraint = restraints[0][1]
    model.finalize()
    scale_msld_system(system, model)
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(x * unit.nanometer)
    return Oracle(spec), model, ctx


def _random_thetas(rng, n):
    return [np.concatenate([[0.0], rng.uniform(-math.pi, math.pi, 5)]) for _ in range(n)]


def _close(a, b, rel):
    a, b = np.asarray(a, float), np.asarray(b, float)
    scale = max(1.0, float(np.max(np.abs(b))))
    return float(np.max(np.abs(a - b))) <= rel * scale


@pytest.mark.parametrize("alpha", [0.5, 0.0])
def test_energy_and_dudl_match_oracle(alpha):
    """>= 20 random interior lambda vectors: total energy and every dU/dlambda_b to 1e-8."""
    oracle, model, ctx = _build(seed=1, alpha=alpha)
    dyn = LambdaDynamics(ctx, model, temperature=300.0, seed=0)
    rng = np.random.default_rng(7)
    for th in _random_thetas(rng, 24):
        dyn.theta = list(th)
        lam = np.array(dyn.project())
        assert np.allclose(lam, oracle.lambdas_from_theta(th), atol=1e-14)
        e = dyn.potential_energy()
        e_ref = float(np.real(oracle.energy(lam)))
        assert abs(e - e_ref) <= 1e-8 * max(1.0, abs(e_ref)), (lam, e, e_ref)
        d, _ = dyn.dUdlambda(lam=list(lam))
        d_ref = oracle.dU_dlambda(lam)
        assert _close(d[1:], d_ref[1:], 1e-8), (lam, d, d_ref)


def test_dudtheta_matches_oracle():
    """The softmax chain rule (dU/dtheta) against complex-step through the oracle's softmax."""
    oracle, model, ctx = _build(seed=2)
    dyn = LambdaDynamics(ctx, model, temperature=300.0, seed=0)
    rng = np.random.default_rng(11)
    for th in _random_thetas(rng, 8):
        dyn.theta = list(th)
        g = dyn.dUdtheta()
        g_ref = oracle.dU_dtheta(th)
        assert _close(g[1:], g_ref[1:], 1e-8), (th, g, g_ref)


def test_softcore_overlap_matches_oracle():
    """An env atom 0.01 nm from a block atom: the soft-core regime at small lambda."""
    oracle, model, ctx = _build(seed=3, overlap=True)
    dyn = LambdaDynamics(ctx, model, temperature=300.0, seed=0)
    for lam4 in (1e-3, 0.05, 0.3):
        lam = np.array([1.0, 0.2, 0.5, 0.3, lam4, 1.0 - lam4])
        set_lambdas(ctx, lam)
        e = dyn.potential_energy()
        e_ref = float(np.real(oracle.energy(lam)))
        assert abs(e - e_ref) <= 1e-8 * max(1.0, abs(e_ref)), (lam4, e, e_ref)
        d, _ = dyn.dUdlambda(lam=list(lam))
        assert _close(d[1:], oracle.dU_dlambda(lam)[1:], 1e-8), (lam4, d)


# golden fixture for the C++ plugin ---------------------------------------------------------------
# tests/data/oracle_toy.json holds the toy's full parameter set, 8 lambda vectors and the oracle's
# energies and dU/dlambda (double precision), so the plugin's own tests can check against fixed
# numbers without Python. Regenerate with:  python tests/test_oracle_partial_lambda.py
_FIXTURE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "oracle_toy.json")


def _fixture_cases():
    out = []
    for alpha, overlap, seed in ((0.5, False, 1), (0.5, True, 3)):
        oracle, _, _ = _build(seed=seed, alpha=alpha, overlap=overlap)
        rng = np.random.default_rng(100 + seed)
        lams = [oracle.lambdas_from_theta(th) for th in _random_thetas(rng, 4)]
        s = oracle.s
        spec = {k: (np.asarray(v).tolist() if isinstance(v, np.ndarray) else v)
                for k, v in s.items() if k != "excluded"}
        spec["excluded"] = sorted([list(p) for p in s["excluded"]])
        spec["bonds"] = [list(t) for t in s["bonds"]]
        out.append(dict(seed=seed, overlap=overlap, spec=spec, cases=[
            dict(lam=list(map(float, lam)), energy=float(np.real(oracle.energy(lam))),
                 dU_dlambda=oracle.dU_dlambda(lam).tolist()) for lam in lams]))
    return out


def test_golden_fixture_is_current():
    """The stored fixture still equals the oracle (and so the engine) to 1e-10."""
    import json
    with open(_FIXTURE) as fh:
        stored = json.load(fh)
    for st, now in zip(stored["systems"], _fixture_cases()):
        for a, b in zip(st["cases"], now["cases"]):
            assert np.allclose(a["lam"], b["lam"], rtol=0, atol=1e-14)
            assert abs(a["energy"] - b["energy"]) <= 1e-10 * max(1.0, abs(b["energy"]))
            assert _close(a["dU_dlambda"], b["dU_dlambda"], 1e-10)


if __name__ == "__main__":
    import json
    os.makedirs(os.path.dirname(_FIXTURE), exist_ok=True)
    doc = {"description": "MSLD partial-lambda oracle fixture (tests/msld_oracle.py). Units nm, "
                          "kJ/mol, e, rad. lam[0] is the environment. NoCutoff. Bias sign: "
                          "+fixed_bias[b]*lam[b]; variable biases (i, j, type, l0, k) as in "
                          "msld_oracle.py. excluded = 1-2, 1-3 and 1-4 pairs (1-4s are in pairs14).",
           "systems": _fixture_cases()}
    with open(_FIXTURE, "w") as fh:
        json.dump(doc, fh, indent=1)
    print("wrote", _FIXTURE)
