"""Minimization + nonbonded-exclusion parity.

Two things introduced together:
  * LambdaDynamics.minimize() -- relax atom clashes (at the current lambda) before dynamics, so a
    freshly grafted/solvated hybrid does not blow up on step 1.
  * every nonbonded force in the lambda-scaled System carries the SAME exclusion set. The
    within-block electrostatics correction used to omit the same-site exclusions (it runs before
    they are added), which is fine on the Reference platform but makes the CPU/OpenCL/CUDA
    platforms reject the System ("All Forces must have identical exclusions") and breaks
    minimization on OpenCL. The correction now adds them too (zero-energy: those pairs are
    cross-block and never in its within-block interaction group).
"""
import os
import sys

import numpy as np
import openmm as mm
from openmm import unit, Vec3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.model import MSLDModel
from msld.builder import scale_msld_system
from msld.integrator import LambdaDynamics

_REF = mm.Platform.getPlatform("Reference")
_KJ = unit.kilojoule_per_mole
_NM = unit.nanometer


def _clash_system():
    """env atom 0 ; site1 blocks b1={2}, b2={3}. Block atom 2 is placed on top of env atom 0."""
    system = mm.System()
    for _ in range(4):
        system.addParticle(12.0)
    bond = mm.HarmonicBondForce()
    bond.addBond(0, 1, 0.15, 200000.0)      # env-env, holds the frame
    bond.addBond(1, 2, 0.15, 200000.0)      # env-b1
    bond.addBond(1, 3, 0.15, 200000.0)      # env-b2
    system.addForce(bond)
    nb = mm.NonbondedForce()
    nb.setNonbondedMethod(mm.NonbondedForce.NoCutoff)
    for i in range(4):
        nb.addParticle(0.0, 0.30, 1.0)      # LJ, no charge
    system.addForce(nb)
    # atom 2 (block 1) sits 0.02 nm from env atom 0 -> huge LJ repulsion (scaled by lambda1)
    pos = [Vec3(0, 0, 0), Vec3(0.15, 0, 0), Vec3(0.02, 0, 0), Vec3(0.15, 0.15, 0)] * _NM
    m = MSLDModel(4)
    m.add_block(site=1, atoms=[2]); m.add_block(site=1, atoms=[3]); m.finalize()
    return system, pos, m


def test_minimize_relaxes_a_clash():
    system, pos, model = _clash_system()
    scale_msld_system(system, model)
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(pos)
    dyn = LambdaDynamics(ctx, model, temperature=300.0, timestep=0.001)

    pe0 = dyn.potential_energy()
    f0 = np.array(ctx.getState(getForces=True).getForces(asNumpy=True)
                  .value_in_unit(_KJ / _NM))
    dyn.minimize(max_iterations=1000)
    pe1 = dyn.potential_energy()
    f1 = np.array(ctx.getState(getForces=True).getForces(asNumpy=True)
                  .value_in_unit(_KJ / _NM))

    assert pe1 < pe0 - 100.0, f"minimize should lower the energy: {pe0} -> {pe1}"
    assert np.linalg.norm(f1, axis=1).max() < np.linalg.norm(f0, axis=1).max() / 10.0
    # the relaxed positions are reloaded into the driver
    assert np.allclose(dyn.x, ctx.getState(getPositions=True)
                       .getPositions(asNumpy=True).value_in_unit(_NM))
    print("PASS test_minimize_relaxes_a_clash", f"({pe0:.1f} -> {pe1:.1f} kJ/mol)")


def _chain_block_system():
    """env atom 0 ; site1 b1 = 5-atom chain {1..5} (has a 1-5 full pair -> elec correction),
    b2 = {6}. Charges on all so the within-block elec-correction force is created."""
    system = mm.System()
    for _ in range(7):
        system.addParticle(12.0)
    bond = mm.HarmonicBondForce()
    for a, b in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 6)]:
        bond.addBond(a, b, 0.15, 200000.0)
    system.addForce(bond)
    nb = mm.NonbondedForce()
    nb.setNonbondedMethod(mm.NonbondedForce.NoCutoff)
    for i in range(7):
        nb.addParticle(0.2 if i % 2 else -0.2, 0.30, 0.5)
    system.addForce(nb)
    m = MSLDModel(7)
    m.add_block(site=1, atoms=[1, 2, 3, 4, 5]); m.add_block(site=1, atoms=[6]); m.finalize()
    return system, m


def _exclusion_pairs(force):
    if isinstance(force, mm.NonbondedForce):
        return {tuple(sorted(force.getExceptionParameters(k)[:2]))
                for k in range(force.getNumExceptions())}
    return {tuple(sorted(force.getExclusionParticles(k)))
            for k in range(force.getNumExclusions())}


def test_scaled_forces_share_one_exclusion_set():
    system, model = _chain_block_system()
    scale_msld_system(system, model)
    nb_forces = [f for f in system.getForces()
                 if isinstance(f, (mm.NonbondedForce, mm.CustomNonbondedForce))]
    names = [f.getName() or f.__class__.__name__ for f in nb_forces]
    # the within-block elec correction must actually be present (else the test is vacuous)
    assert any(n.startswith("MSLDWBElec") for n in names), names
    ref = _exclusion_pairs(nb_forces[0])
    for f, n in zip(nb_forces, names):
        assert _exclusion_pairs(f) == ref, f"{n} has a different exclusion set"
    print("PASS test_scaled_forces_share_one_exclusion_set",
          f"({len(nb_forces)} forces, {len(ref)} exclusions each)")


if __name__ == "__main__":
    test_minimize_relaxes_a_clash()
    test_scaled_forces_share_one_exclusion_set()
    print("\nminimize + exclusion-parity tests passed")
