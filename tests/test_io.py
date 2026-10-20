"""io.py — LambdaTrajectoryWriter + block_labels + populations, on a small 2-site run.

Checks the reporter writes the right columns, lambdas normalize per site every row, the
read-back helpers work, and LambdaDynamics.run drives reporters at the requested interval.
The engine + io are parmed/rdkit-free, so this test uses a duck-typed mapping stub (block_labels
only reads `mapping.sites[k].block_names`).
"""
import os
import sys
import tempfile

import numpy as np
import openmm as mm
from openmm import app, unit, Vec3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.model import MSLDModel
from msld.builder import scale_msld_system
from msld.integrator import LambdaDynamics
from msld.io import LambdaTrajectoryWriter, block_labels, populations, read_trajectory

_REF = mm.Platform.getPlatform("Reference")


def _two_site_system():
    # env 0 ; site1: b1={1}, b2={2} ; site2: b3={3}, b4={4}; each bonded to env
    system = mm.System()
    for _ in range(5):
        system.addParticle(12.0)
    bond = mm.HarmonicBondForce()
    for j, r0 in [(1, 0.10), (2, 0.13), (3, 0.16), (4, 0.20)]:
        bond.addBond(0, j, r0, 1000.0)
    system.addForce(bond)
    pos = [Vec3(0, 0, 0), Vec3(0.15, 0, 0), Vec3(0.22, 0, 0),
           Vec3(0.28, 0, 0), Vec3(0.34, 0, 0)] * unit.nanometer
    return system, pos


def _model():
    m = MSLDModel(5)
    m.add_block(site=1, atoms=[1], theta0=0.3)
    m.add_block(site=1, atoms=[2], theta0=-0.2)
    m.add_block(site=2, atoms=[3], theta0=0.1)
    m.add_block(site=2, atoms=[4], theta0=0.4)
    return m.finalize()


class _StubSite:
    def __init__(self, names):
        self.block_names = names


class _StubBlockSite:
    """A blueprint site that only answers all_block_atoms() (what TrajectoryWriter needs)."""
    def __init__(self, block_atoms):
        self._b = set(block_atoms)

    def all_block_atoms(self):
        return self._b


class _StubBlueprint:
    def __init__(self, sites):
        self.sites = sites


class _StubStructure:
    """TrajectoryWriter reads only .topology and .positions — a real Structure isn't needed here."""
    def __init__(self, topology, positions):
        self.topology = topology
        self.positions = positions


_MAP = _StubBlueprint([_StubSite(["WT", "MUT"]), _StubSite(["A", "B"])])


def _dyn():
    system, pos = _two_site_system()
    model = _model()
    scale_msld_system(system, model)
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(pos)
    return LambdaDynamics(ctx, model, temperature=300.0, timestep=0.001, seed=1), model


def _tmp():
    return os.path.join(tempfile.mkdtemp(), "traj.csv")


def test_block_labels_fallback_and_mapping():
    model = _model()
    assert block_labels(model) == ["lambda1", "lambda2", "lambda3", "lambda4"]     # no mapping
    assert block_labels(model, _MAP) == ["s1:WT", "s1:MUT", "s2:A", "s2:B"]        # 2 sites -> prefixed
    one = _StubBlueprint([_StubSite(["WT", "MUT", "X", "Y"])])
    assert block_labels(model, one) == ["WT", "MUT", "X", "Y"]                      # 1 site -> no prefix
    bad = _StubBlueprint([_StubSite(["only"])])                                     # count mismatch
    assert block_labels(model, bad) == ["lambda1", "lambda2", "lambda3", "lambda4"] # -> fallback


def test_metrics_written_via_run_direct_api():
    # the natural path: name the file + interval, no `with`, run opens/closes it
    dyn, _ = _dyn()
    path = _tmp()
    dyn.run(50, metrics=path, metrics_every=10, mapping=_MAP)    # -> 5 rows at steps 10..50

    lines = open(path).read().strip().split("\n")
    assert lines[0] == "step,time_ps,potential_kJ,theta_temp_K,s1:WT,s1:MUT,s2:A,s2:B"
    assert len(lines) == 1 + 5                                  # header + 5 samples

    labels, cols = read_trajectory(path)
    assert labels == ["s1:WT", "s1:MUT", "s2:A", "s2:B"]
    assert [int(s) for s in cols["step"]] == [10, 20, 30, 40, 50]
    assert np.allclose(cols["s1:WT"] + cols["s1:MUT"], 1.0, atol=1e-6)   # lambdas normalize / site
    assert np.allclose(cols["s2:A"] + cols["s2:B"], 1.0, atol=1e-6)      # (atol = CSV round-off)
    assert np.all(cols["time_ps"] > 0.0)                        # step * dt


def test_metrics_and_trajectory_have_independent_intervals():
    # metrics every 10, trajectory every 20, in ONE run -> 5 metric rows + 3 DCD frames (20,40,60)
    dyn, _ = _dyn()
    d = tempfile.mkdtemp()
    csv, dcd = os.path.join(d, "m.csv"), os.path.join(d, "t.dcd")

    top = app.Topology(); res = top.addResidue("SYS", top.addChain())
    for i in range(5):
        top.addAtom(f"A{i}", app.Element.getBySymbol("C"), res)
    pos = [Vec3(0.1 * i, 0.0, 0.0) for i in range(5)] * unit.nanometer
    struct = _StubStructure(top, pos)

    dyn.run(60, metrics=csv, metrics_every=10, mapping=_MAP,
            trajectory=dcd, trajectory_every=20, structure=struct)

    assert len(open(csv).read().strip().split("\n")) == 1 + 6   # header + 6 metric rows
    assert os.path.getsize(dcd) > 0                             # DCD frames written
    assert os.path.exists(os.path.join(d, "t.pdb"))            # companion topology PDB


def test_trajectory_pdb_bonds_the_alchemical_residue():
    # The companion topology PDB must let a viewer draw the block side chain. In the raw topology a
    # block fragment is its own residue named after a standard amino acid, so writeFile emits no
    # CONECT and the fragment renders as free-floating atoms. Passing `mapping` renames a block-only
    # residue to a non-standard name so writeFile emits CONECT for it (and the caller's structure is
    # left untouched).
    import warnings
    from openmm.app import PDBFile

    dyn, _ = _dyn()
    d = tempfile.mkdtemp()
    dcd = os.path.join(d, "t.dcd")

    top = app.Topology(); chain = top.addChain()
    env = top.addResidue("GLY", chain)                          # atoms 0,1 = environment
    a0 = top.addAtom("N", app.Element.getBySymbol("N"), env)
    a1 = top.addAtom("CB", app.Element.getBySymbol("C"), env)
    blk = top.addResidue("LEU", chain)                          # atoms 2,3,4 = a block fragment
    a2 = top.addAtom("CG", app.Element.getBySymbol("C"), blk)
    a3 = top.addAtom("CD1", app.Element.getBySymbol("C"), blk)
    a4 = top.addAtom("CD2", app.Element.getBySymbol("C"), blk)
    for x, y in [(a0, a1), (a1, a2), (a2, a3), (a2, a4)]:
        top.addBond(x, y)
    pos = [Vec3(0.10 * i, 0.0, 0.0) for i in range(5)] * unit.nanometer
    struct = _StubStructure(top, pos)
    block_map = _StubBlueprint([_StubBlockSite({2, 3, 4})])

    dyn.run(2, trajectory=dcd, trajectory_every=2, structure=struct, mapping=block_map)

    text = open(os.path.join(d, "t.pdb")).read()
    assert " HYB " in text, "block-only residue was not renamed in the companion PDB"
    assert "CONECT" in text, "no CONECT emitted for the alchemical residue"
    assert [r.name for r in struct.topology.residues()] == ["GLY", "LEU"], "structure names not restored"

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        p = PDBFile(os.path.join(d, "t.pdb"))
    deg = {}
    for bd in p.topology.bonds():
        for a in (bd.atom1, bd.atom2):
            deg[a.index] = deg.get(a.index, 0) + 1
    assert deg.get(3, 0) >= 1 and deg.get(4, 0) >= 1, "block atoms are unbonded in the companion PDB"

    # without a mapping the block residue is left as-is (raw topology)
    dcd2 = os.path.join(d, "t2.dcd")
    dyn.run(2, trajectory=dcd2, trajectory_every=2, structure=struct)
    assert " HYB " not in open(os.path.join(d, "t2.pdb")).read()


def test_populations_sums_to_one_per_site():
    dyn, _ = _dyn()
    path = _tmp()
    dyn.run(40, metrics=path, metrics_every=10, mapping=_MAP)
    pops = populations(path)
    assert set(pops) == {"s1:WT", "s1:MUT", "s2:A", "s2:B"}
    assert abs(pops["s1:WT"] + pops["s1:MUT"] - 1.0) < 1e-6   # 1e-6 = CSV round-off
    assert abs(pops["s2:A"] + pops["s2:B"] - 1.0) < 1e-6


def test_reporters_list_is_autoclosed_no_with():
    # a reporter passed via reporters=[...] carries its own `every` and is closed by run
    dyn, model = _dyn()
    path = _tmp()
    w = LambdaTrajectoryWriter(path, model, every=10, mapping=_MAP)
    dyn.run(30, reporters=[w])                                  # no `with`
    assert w._f.closed                                         # run closed it
    assert len(open(path).read().strip().split("\n")) == 1 + 3  # header + 3 rows (10,20,30)


def test_run_without_outputs_is_plain_step():
    dyn, _ = _dyn()
    lam0 = dyn.get_lambdas()
    dyn.run(20)                                                 # nothing to write -> just step(20)
    lam1 = dyn.get_lambdas()
    assert any(abs(lam1[b] - lam0[b]) > 1e-6 for b in dyn.dof)  # lambda moved


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nio tests passed")
