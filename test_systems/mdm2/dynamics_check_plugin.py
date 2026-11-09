"""MDM2 on the CPU platform: short dynamics with use_plugin against the stock build.

Both builds start from one minimized geometry with one seed.
  nve : atom and theta friction 0 (the VRORV step reduces to velocity Verlet); total energy drift.
  nvt : atom and theta friction 1 ps^-1; theta and atom temperatures, lambda trajectories.

Usage:
  python dynamics_check_plugin.py prep   OUTDIR
  python dynamics_check_plugin.py run    OUTDIR {stock,plugin} {nve,nvt} NSTEPS
  python dynamics_check_plugin.py report OUTDIR
Env: THREADS (default 4), MIN_ITERS (default 2000). Needs msldplugin for the plugin build (msld/plugin.py).
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

NM = unit.nanometer
THREADS = os.environ.get("THREADS", "4")
MIN_ITERS = int(os.environ.get("MIN_ITERS", 2000))
MDM2 = Path(REPO) / "test_systems" / "mdm2"
DT = 0.001
SEED = 0
ENERGY_EVERY = {"nve": 5, "nvt": 50}
LOG_EVERY = {"nve": 5, "nvt": 10}


def prepare_model():
    from msld.prep import ingest, build_msld_system, Site
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
    return bundle, model


def prep(out):
    from msld.integrator import LambdaDynamics
    bundle, model = prepare_model()
    (out / "base_system.xml").write_text(mm.XmlSerializer.serialize(bundle.system))
    system = mm.XmlSerializer.deserialize(mm.XmlSerializer.serialize(bundle.system))
    model.scale_system(system, use_plugin=False)
    names = [mm.Platform.getPlatform(i).getName() for i in range(mm.Platform.getNumPlatforms())]
    ctx = mm.Context(system, mm.VerletIntegrator(DT), mm.Platform.getPlatformByName("OpenCL" if "OpenCL" in names else "CPU"))
    ctx.setPositions(bundle.structure.positions)
    dyn = LambdaDynamics(ctx, model, temperature=300.0, timestep=DT, seed=SEED)
    dyn.minimize(max_iterations=MIN_ITERS)
    box = np.array(ctx.getState().getPeriodicBoxVectors(asNumpy=True).value_in_unit(NM))
    np.savez(out / "start.npz", x=dyn.x, box=box)
    print(f"prepared: {len(dyn.x)} atoms, {system.getNumConstraints()} constraints, "
          f"blocks {bundle.mapping.sites[0].block_names}", flush=True)


def run(out, build, mode, nsteps):
    from msld.integrator import LambdaDynamics
    _, model = prepare_model()
    start = np.load(out / "start.npz")
    system = mm.XmlSerializer.deserialize((out / "base_system.xml").read_text())
    model.scale_system(system, use_plugin=(build == "plugin"))
    friction = 0.0 if mode == "nve" else 1.0
    for bl in model.blocks[1:]:
        bl.theta_mass, bl.theta_friction = 0.05, friction
    ctx = mm.Context(system, mm.VerletIntegrator(DT), mm.Platform.getPlatformByName("CPU"), {"Threads": THREADS})
    ctx.setPeriodicBoxVectors(*[mm.Vec3(*v) * NM for v in start["box"]])
    ctx.setPositions(start["x"] * NM)
    dyn = LambdaDynamics(ctx, model, temperature=300.0, timestep=DT, atom_friction=friction, seed=SEED)
    path = out / f"{build}_{mode}.jsonl"
    t0 = time.time()
    with open(path, "w") as fh:
        for step in range(nsteps + 1):
            if step:
                dyn.step(1)
            if step % LOG_EVERY[mode] == 0:
                row = {"step": step, "wall": time.time() - t0, "T_theta": dyn.theta_temperature(),
                       "T_atoms": dyn.atom_temperature(), "lam": [float(v) for v in dyn.get_lambdas()[1:]]}
                row["KE_atoms"] = 0.5 * float(np.sum(dyn.mass_x[:, None] * dyn.vx ** 2))
                row["KE_theta"] = 0.5 * sum(dyn.mass[b] * dyn.vtheta[b] ** 2 for b in dyn.dof)
                if step % ENERGY_EVERY[mode] == 0:
                    row["PE"] = dyn.potential_energy()
                fh.write(json.dumps(row) + "\n")
                fh.flush()
    print(f"{build} {mode}: {nsteps} steps in {time.time() - t0:.0f}s", flush=True)


def _load(path):
    return [json.loads(line) for line in open(path)]


def report(out):
    results = {}
    for build in ("stock", "plugin"):
        path = out / f"{build}_nve.jsonl"
        if not path.exists():
            continue
        rows = [r for r in _load(path) if "PE" in r]
        t = np.array([r["step"] * DT for r in rows])
        total = np.array([r["PE"] + r["KE_atoms"] + r["KE_theta"] for r in rows])
        slope = float(np.polyfit(t, total, 1)[0])
        results[f"{build} NVE"] = {
            "steps": rows[-1]["step"], "E0": float(total[0]), "drift kJ/mol/ps": slope,
            "residual rms kJ/mol": float(np.std(total - np.polyval(np.polyfit(t, total, 1), t))),
            "max |E-E0| kJ/mol": float(np.max(np.abs(total - total[0]))),
            "PE range kJ/mol": float(max(r["PE"] for r in rows) - min(r["PE"] for r in rows)),
            "T_atoms end": rows[-1]["T_atoms"], "s/step": rows[-1]["wall"] / max(1, rows[-1]["step"])}
    series = {}
    for build in ("stock", "plugin"):
        path = out / f"{build}_nvt.jsonl"
        if not path.exists():
            continue
        rows = _load(path)
        series[build] = rows
        tail = rows[len(rows) // 5:]         # first 20 % discarded
        results[f"{build} NVT"] = {
            "steps": rows[-1]["step"], "s/step": rows[-1]["wall"] / max(1, rows[-1]["step"]),
            "<T_theta> K": float(np.mean([r["T_theta"] for r in tail])),
            "<T_atoms> K": float(np.mean([r["T_atoms"] for r in tail])),
            "<lambda>": np.mean([r["lam"] for r in tail], axis=0).tolist(),
            "lambda end": rows[-1]["lam"]}
    if len(series) == 2:
        n = min(len(series["stock"]), len(series["plugin"]))
        d = np.array([np.max(np.abs(np.array(series["stock"][i]["lam"]) - np.array(series["plugin"][i]["lam"])))
                      for i in range(n)])
        marks = sorted({0, n // 4, n // 2, 3 * n // 4, n - 1})
        results["NVT |lambda stock - lambda plugin| (max over blocks)"] = {
            f"step {series['stock'][i]['step']}": float(d[i]) for i in marks}
    print(json.dumps(results, indent=1))
    (out / "report.json").write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    command, out = sys.argv[1], Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    if command == "prep":
        prep(out)
    elif command == "run":
        run(out, sys.argv[3], sys.argv[4], int(sys.argv[5]))
    elif command == "report":
        report(out)
    else:
        raise SystemExit(__doc__)
