"""MDM2 (PME, ~26k atoms): the use_plugin build against the stock build, at partial lambda.

Both builds start from one hybrid System and one minimized geometry. Reports total energy, dU/dlambda
per block and forces (plugin vs stock, both on the Reference platform, in double precision), and the
time of one energy + forces + dU/dlambda evaluation on each platform. Needs msldplugin (msld/plugin.py).

Usage: python compare_plugin.py OUTDIR       (env: THREADS=4, MIN_ITERS=2000)
"""
import json
import os
import sys
import time
from pathlib import Path

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO)
import numpy as np
import openmm as mm
from openmm import unit

from msld.builder import set_lambdas
from msld.integrator import LambdaDynamics
from msld.prep import ingest, build_msld_system, Site

NM, KJ, F_UNIT = unit.nanometer, unit.kilojoule_per_mole, unit.kilojoule_per_mole / unit.nanometer
THREADS = os.environ.get("THREADS", "4")
MIN_ITERS = int(os.environ.get("MIN_ITERS", 2000))
MDM2 = Path(REPO) / "test_systems" / "mdm2"
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)


def log(*a):
    print(*a, flush=True)


t0 = time.time()
protein = ingest(MDM2 / "mdm2_protein.pdb", forcefield=["amber14-all.xml"], add_hydrogens=True)
peptide = ingest(MDM2 / "mdm2_peptide.pdb", forcefield=["amber14-all.xml"], add_hydrogens=True)
for r in peptide.residues:
    r.chain = "B"
bundle = build_msld_system(
    environment=protein + peptide,
    sites=[Site(residue=len(protein.residues) + 3,
                variants={v: MDM2 / f"{v}_var.pdb" for v in ("ILE", "LEU", "SER", "VAL")},
                mapper="backbone")],
    forcefield=["amber14-all.xml"], renormalize=True, solvate=True)
model = bundle.to_model()
model.scale_bond = False
model.scale_angle = False
base_xml = mm.XmlSerializer.serialize(bundle.system)
names = bundle.mapping.sites[0].block_names
blocks = model.blocks_in_site(1)
log(f"built in {time.time() - t0:.0f}s: {bundle.system.getNumParticles()} atoms, blocks {dict(zip(names, blocks))}")


def build(use_plugin):
    system = mm.XmlSerializer.deserialize(base_xml)
    model.scale_system(system, use_plugin=use_plugin)
    return system


def context(system, platform):
    props = {"Threads": THREADS} if platform == "CPU" else {}
    return mm.Context(system, mm.VerletIntegrator(0.001), mm.Platform.getPlatformByName(platform), props)


# one geometry for everything: minimized on the stock build (OpenCL if there is one)
stock_xml = mm.XmlSerializer.serialize(build(False))
platforms = [mm.Platform.getPlatform(i).getName() for i in range(mm.Platform.getNumPlatforms())]
t0 = time.time()
ctx = context(mm.XmlSerializer.deserialize(stock_xml), "OpenCL" if "OpenCL" in platforms else "CPU")
ctx.setPositions(bundle.structure.positions)
dyn = LambdaDynamics(ctx, model, temperature=300.0, timestep=0.001, seed=0)
dyn.minimize(max_iterations=MIN_ITERS)
x = np.array(dyn.x)
box = ctx.getState().getPeriodicBoxVectors()
log(f"minimized in {time.time() - t0:.0f}s on {ctx.getPlatform().getName()}, box {box[0][0]}")
del ctx, dyn
np.save(OUT / "positions.npy", x)


def lam_vector(on):
    lam = [0.0] * model.n_blocks
    lam[0] = 1.0
    for name, value in on.items():
        lam[blocks[names.index(name)]] = value
    return lam


n = len(names)
POINTS = {
    "uniform": lam_vector({v: 1.0 / n for v in names}),
    "LEU 0.70": lam_vector({v: (0.70 if v == "LEU" else 0.30 / (n - 1)) for v in names}),
    "LEU 0.40 / VAL 0.40": lam_vector({v: (0.40 if v in ("LEU", "VAL") else 0.20 / (n - 2)) for v in names}),
    "LEU 0.99": lam_vector({v: (0.99 if v == "LEU" else 0.01 / (n - 1)) for v in names}),
}


def evaluate(system, platform, lam):
    ctx = context(system, platform)
    ctx.setPeriodicBoxVectors(*box)
    ctx.setPositions(x * NM)
    dyn = LambdaDynamics(ctx, model, temperature=300.0, timestep=0.001, seed=0)
    set_lambdas(ctx, lam)
    st = ctx.getState(getEnergy=True, getForces=True, getParameterDerivatives=True)
    d, _ = dyn.dUdlambda(analytic_deriv=st.getEnergyParameterDerivatives(), lam=list(lam))
    e, f = st.getPotentialEnergy().value_in_unit(KJ), st.getForces(asNumpy=True).value_in_unit(F_UNIT)
    del dyn, ctx
    return e, np.array(d), np.array(f)


def timing(system, platform, lam, repeats):
    """Seconds for what one dynamics step needs: energy, forces and every dU/dlambda. The atoms
    random-walk 0.0005 nm per coordinate between evaluations, about what a 1 fs step does, so a
    platform that reuses its neighbour list rebuilds it as often as it would in dynamics."""
    ctx = context(system, platform)
    ctx.setPeriodicBoxVectors(*box)
    dyn = LambdaDynamics(ctx, model, temperature=300.0, timestep=0.001, seed=0)
    set_lambdas(ctx, lam)
    rng = np.random.default_rng(0)
    walk = x.copy()
    out = []
    for r in range(repeats):
        walk = walk + rng.normal(0.0, 0.0005, walk.shape)
        ctx.setPositions(walk * NM)
        t = time.perf_counter()
        st = ctx.getState(getEnergy=True, getForces=True, getParameterDerivatives=True)
        forces_time = time.perf_counter() - t
        dyn.dUdlambda(analytic_deriv=st.getEnergyParameterDerivatives(), lam=list(lam))
        out.append((forces_time, time.perf_counter() - t))
    return {"energy+forces s": float(np.mean([o[0] for o in out])),
            "energy+forces+dU/dlambda s": float(np.mean([o[1] for o in out])),
            "evaluations": repeats, "fd": dyn._has_fd}


plugin_xml = mm.XmlSerializer.serialize(build(True))
results = {"atoms": len(x), "blocks": names, "points": {}, "timing": {}}
for label, lam in POINTS.items():
    t0 = time.time()
    e0, d0, f0 = evaluate(mm.XmlSerializer.deserialize(stock_xml), "Reference", lam)
    e1, d1, f1 = evaluate(mm.XmlSerializer.deserialize(plugin_xml), "Reference", lam)
    df = np.linalg.norm(f1 - f0, axis=1)
    fn = np.linalg.norm(f0, axis=1)
    row = {"lambda": lam, "E stock": e0, "E plugin": e1, "E rel err": abs(e1 - e0) / abs(e0),
           "dU/dlambda stock": dict(zip(names, d0[blocks].tolist())),
           "dU/dlambda plugin": dict(zip(names, d1[blocks].tolist())),
           "dU/dlambda max rel err": float(np.max(np.abs(d1[blocks] - d0[blocks]) / np.abs(d0[blocks]))),
           "dU/dlambda max abs err": float(np.max(np.abs(d1[blocks] - d0[blocks]))),
           "F max abs err": float(df.max()), "F max": float(fn.max()),
           "F max err / F max": float(df.max() / fn.max()),
           "F max per-atom rel err": float(np.max(df / np.maximum(fn, 1.0)))}
    results["points"][label] = row
    log(label, json.dumps({k: v for k, v in row.items() if "stock" not in k and "plugin" not in k and k != "lambda"}),
        f"({time.time() - t0:.0f}s)")
    (OUT / "results.json").write_text(json.dumps(results, indent=1))

lam = POINTS["uniform"]
for label, xml, platform, repeats in (("stock CPU", stock_xml, "CPU", 50), ("plugin CPU", plugin_xml, "CPU", 20),
                                      ("stock Reference", stock_xml, "Reference", 5),
                                      ("plugin Reference", plugin_xml, "Reference", 20)):
    results["timing"][label] = timing(mm.XmlSerializer.deserialize(xml), platform, lam, repeats)
    log(label, results["timing"][label])
    (OUT / "results.json").write_text(json.dumps(results, indent=1))

# stock on CPU against stock on Reference: the single-precision noise the numbers above do not have
e_c, d_c, f_c = evaluate(mm.XmlSerializer.deserialize(stock_xml), "CPU", lam)
e_r, d_r, f_r = evaluate(mm.XmlSerializer.deserialize(stock_xml), "Reference", lam)
e_p, d_p, f_p = evaluate(mm.XmlSerializer.deserialize(plugin_xml), "CPU", lam)
results["CPU baseline"] = {
    "stock CPU vs stock Reference": {"E rel err": abs(e_c - e_r) / abs(e_r),
                                     "dU/dlambda max abs err": float(np.max(np.abs(d_c[blocks] - d_r[blocks]))),
                                     "F max abs err": float(np.linalg.norm(f_c - f_r, axis=1).max())},
    "plugin CPU vs stock Reference": {"E rel err": abs(e_p - e_r) / abs(e_r),
                                      "dU/dlambda max abs err": float(np.max(np.abs(d_p[blocks] - d_r[blocks]))),
                                      "F max abs err": float(np.linalg.norm(f_p - f_r, axis=1).max())}}
log(json.dumps(results["CPU baseline"]))
(OUT / "results.json").write_text(json.dumps(results, indent=1))
log("done")
