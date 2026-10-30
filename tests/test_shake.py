"""SHAKE in the lambda-dynamics drift, and the atom temperature it produces.

The drift used to call Context.applyConstraints, which takes the predicted positions as their own
reference. That projection is not time-reversible and steadily drained kinetic energy: rigid water
at gamma = 1/ps settled ~30 K below the bath. SHAKE with the pre-drift positions as the reference
is time-reversible (a drift with v, then with -v, returns the start) and keeps the bath temperature.
"""
import os
import sys

import numpy as np
import openmm as mm
from openmm import app, unit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.model import MSLDModel
from msld.builder import scale_msld_system
from msld.integrator import LambdaDynamics


def _water_box(box=1.8, gamma=5.0, dt=0.002, seed=4):
    ff = app.ForceField("amber14-all.xml", "amber14/tip3p.xml")
    mod = app.Modeller(app.Topology(), [])
    mod.addSolvent(ff, boxSize=mm.Vec3(box, box, box) * unit.nanometer)
    system = ff.createSystem(mod.topology, nonbondedMethod=app.PME,
                             nonbondedCutoff=0.7 * unit.nanometer, constraints=app.HBonds,
                             rigidWater=True, removeCMMotion=False)
    res = list(mod.topology.residues())
    model = MSLDModel(system.getNumParticles())
    model.scale_bond = model.scale_angle = False
    model.add_block(site=1, atoms=[a.index for a in res[0].atoms()], theta0=0.5)
    model.add_block(site=1, atoms=[a.index for a in res[3].atoms()], theta0=-0.5)
    model.finalize()
    scale_msld_system(system, model)
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), mm.Platform.getPlatform("CPU"))
    ctx.setPositions(mod.positions)
    dyn = LambdaDynamics(ctx, model, temperature=300.0, timestep=dt, atom_friction=gamma, seed=seed)
    return dyn, system


def _max_constraint_error(dyn, system):
    err = 0.0
    for k in range(system.getNumConstraints()):
        i, j, d = system.getConstraintParameters(k)
        d = d.value_in_unit(unit.nanometer)
        err = max(err, abs(np.linalg.norm(dyn.x[i] - dyn.x[j]) - d) / d)
    return err


def test_shake_time_reversible():
    dyn, system = _water_box()
    dyn.step(1)                                      # start exactly on the constraint manifold
    x0 = dyn.x.copy()
    dyn._drift_x(0.001)
    assert _max_constraint_error(dyn, system) < 1e-5
    dyn.vx = -dyn.vx
    dyn._drift_x(0.001)
    assert np.max(np.abs(dyn.x - x0)) < 1e-6, np.max(np.abs(dyn.x - x0))


def test_initial_velocities_on_manifold():
    dyn, system = _water_box()
    for k in range(system.getNumConstraints()):
        i, j, _ = system.getConstraintParameters(k)
        r = dyn.x[i] - dyn.x[j]
        assert abs(np.dot(r, dyn.vx[i] - dyn.vx[j])) < 1e-4 * np.linalg.norm(r)


def test_constrained_atom_temperature():
    dyn, system = _water_box()
    dyn.minimize(max_iterations=200)
    dyn.step(500)                                    # 1 ps warm-up at gamma = 5/ps
    temps = []
    for _ in range(150):
        dyn.step(10)
        temps.append(dyn.atom_temperature())
    t = float(np.mean(temps))
    assert _max_constraint_error(dyn, system) < 1e-5
    assert 285.0 < t < 315.0, t                      # old projection gave ~290 at gamma 5, ~267 at 1
    print(f"  rigid-water atom temperature {t:.1f} K (target 300)")


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nSHAKE tests passed")
