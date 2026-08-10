"""Atom restraints (CATS).

The centroid restraint U = 0.5*k*sum_i |x_i - xbar|^2 is implemented as pair
bonds; check it equals the direct centroid formula.
"""
import os
import sys

import numpy as np
import openmm as mm
from openmm import unit, Vec3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.model import MSLDModel
from msld.builder import build_msld_system

_REF = mm.Platform.getPlatform("Reference")


def test_atom_restraint_matches_centroid_formula():
    system = mm.System()
    for _ in range(4):
        system.addParticle(12.0)
    pos = np.array([[0.10, 0.00, 0.00],
                    [0.20, 0.05, 0.00],
                    [0.15, 0.20, 0.10],
                    [1.00, 1.00, 1.00]])          # atom 3 is not restrained
    group = [0, 1, 2]

    m = MSLDModel(4)
    m.add_atom_restraint(group)
    m.finalize()
    info = build_msld_system(system, m)
    assert info["atom_restraint_force"] == "MSLDAtomRestraint"

    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(pos * unit.nanometer)
    e = ctx.getState(getEnergy=True).getPotentialEnergy().value_in_unit(
        unit.kilojoule_per_mole)

    g = pos[group]
    centroid = g.mean(axis=0)
    expect = 0.5 * m.k_restraint * ((g - centroid) ** 2).sum()
    assert abs(e - expect) < 1e-6 * max(1.0, expect), (e, expect)

    # a spread-out group costs more than a tight one (sanity of sign/scale)
    assert e > 0.0


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\natom-restraint tests passed")
