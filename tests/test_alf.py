"""ALF Phase 1 -- adaptive fixed lambda-biases.

Two checks:
  * tunable bias globals: with model.bias_flattening the scaled System exposes biascoef{b} knobs,
    and builder.set_biases pushes model coefficients into the live Context.
  * the flattening loop RECOVERS a known free-energy offset: a 2-block site whose blocks are
    otherwise identical carries an injected intrinsic bias dG*lambda2 (so block 2 is disfavoured).
    ALF must flatten the two populations to ~50/50 and learn biascoef2 - biascoef1 ~= -dG.
"""
import os
import sys

import numpy as np
import openmm as mm
from openmm import unit, Vec3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.model import MSLDModel
from msld.builder import scale_msld_system, set_biases
from msld.forces import bias_coef_name
from msld.integrator import LambdaDynamics
from msld.alf import (flatten, LambdaHistogram, add_flattening_biases, ref_overlap, estimate_ddg)

_REF = mm.Platform.getPlatform("Reference")
_DG = 6.0    # kJ/mol injected free-energy offset (block 2 disfavoured); ~2.4 kT at 300 K


def _biased_two_block_system(dG):
    """Site-1 blocks b1={1}, b2={2}; the ONLY lambda-dependent energy is an injected dG*lambda2 term
    (no bonds/nonbonded), so the intrinsic free energy DeltaG(b1->b2) = dG EXACTLY and the flat point
    is biascoef2 - biascoef1 = -dG. Atoms carry no force, so there is no atomic-sampling noise."""
    system = mm.System()
    for _ in range(3):
        system.addParticle(12.0)
    off = mm.CustomExternalForce(f"({dG})*lambda2")   # injected intrinsic offset, block 2 disfavoured
    off.setName("Intrinsic")
    off.addGlobalParameter("lambda2", 1.0)
    off.addParticle(0, [])
    system.addForce(off)
    pos = [Vec3(0, 0, 0), Vec3(0.15, 0, 0), Vec3(-0.15, 0, 0)] * unit.nanometer
    return system, pos


def _model():
    # fnex=2 (gentler than the 5.5 default) so theta can cross between the two blocks in a short
    # toy run -- Phase-1 fixed biases flatten the ENDPOINT free energies, not the barrier, so a
    # sharply bistable, barrier-trapped theta needs the Phase-2 coupling biases (not built yet).
    m = MSLDModel(3, fnex=2.0)
    m.add_block(site=1, atoms=[1])
    m.add_block(site=1, atoms=[2])
    m.bias_flattening = True                # make the bias coefficients tunable knobs
    return m.finalize()


def _dyn(dG=_DG, seed=1):
    system, pos = _biased_two_block_system(dG)
    model = _model()
    scale_msld_system(system, model)
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(pos)
    return LambdaDynamics(ctx, model, temperature=300.0, timestep=0.001, seed=seed), model, ctx


def test_bias_flattening_exposes_tunable_globals():
    dyn, model, ctx = _dyn()
    present = ctx.getParameters()
    assert bias_coef_name(1) in present and bias_coef_name(2) in present   # knobs exist, init 0
    assert ctx.getParameter(bias_coef_name(2)) == 0.0
    model.blocks[2].lambda_bias = -3.5
    set_biases(ctx, model)                                                 # push it live
    assert abs(ctx.getParameter(bias_coef_name(2)) - (-3.5)) < 1e-9


def test_histogram_reports_mean_lambda():
    dyn, model, _ = _dyn()
    h = LambdaHistogram(model, every=50)
    dyn.run(200, reporters=[h])
    occ = h.occupancy()
    assert set(occ) == {1, 2}
    assert abs((occ[1] + occ[2]) - 1.0) < 1e-6      # one site -> occupancies sum to 1


def test_flatten_recovers_injected_free_energy():
    dyn, model, _ = _dyn(dG=_DG, seed=7)

    # baseline: with dG>0 and no learned bias, block 2 is under-populated
    base = LambdaHistogram(model, every=100)
    dyn.run(4000, reporters=[base])
    b0 = base.occupancy()
    assert b0[2] < b0[1] - 0.05, (b0[1], b0[2])     # block 2 disfavoured before flattening

    rep = flatten(dyn, n_iters=60, steps_per_iter=2500, sample_every=50,
                  rate=0.3, floor=5e-3, tol=0.0, verbose=False)   # tol=0 -> run all iters

    # the learned bias oscillates around the fixed point, so average over the converged tail
    tail = rep["bias_history"][-25:]
    learned = np.mean([bh[2] - bh[1] for bh in tail])
    assert abs(learned - (-_DG)) < 2.0, (learned, -_DG)          # recovers the injected offset

    occ_tail = rep["history"][-25:]
    mean_occ2 = np.mean([o[2] for o in occ_tail])
    assert abs(mean_occ2 - 0.5) < 0.15, mean_occ2                # both variants sampled on average


# ---------------------------------------------------------------------
# Phase 2 -- pairwise coupling biases (barrier flattening)
# ---------------------------------------------------------------------
def _trapped_two_block_system(A):
    """2 degenerate blocks with an injected midpoint well -A*l1*l2 (theta gets stuck at ~0.5)."""
    system = mm.System()
    for _ in range(3):
        system.addParticle(12.0)
    trap = mm.CustomExternalForce(f"({-A})*lambda1*lambda2")
    for nm in ("lambda1", "lambda2"):
        trap.addGlobalParameter(nm, 1.0)
    trap.addParticle(0, [])
    system.addForce(trap)
    pos = [Vec3(0, 0, 0), Vec3(0.15, 0, 0), Vec3(-0.15, 0, 0)] * unit.nanometer
    return system, pos


def test_add_flattening_biases_adds_pairwise_couplings():
    m = MSLDModel(4, fnex=4.0)
    m.add_block(site=1, atoms=[1]); m.add_block(site=1, atoms=[2]); m.add_block(site=1, atoms=[3])
    m.finalize()
    add_flattening_biases(m, couple=True)
    assert m.bias_flattening is True
    pairs = {(vb.i, vb.j) for vb in m.variable_biases}
    assert pairs == {(1, 2), (1, 3), (2, 3)}                 # every pair at the site
    assert all(vb.type == 6 and vb.k == 0.0 for vb in m.variable_biases)


def test_phase2_coupling_untraps_midpoint():
    A = 20.0                                                 # injected midpoint trap depth (kJ/mol)
    system, pos = _trapped_two_block_system(A)
    m = MSLDModel(3, fnex=4.0)
    m.add_block(site=1, atoms=[1]); m.add_block(site=1, atoms=[2]); m.finalize()
    add_flattening_biases(m, couple=True)                    # tunable fixed biases + one coupling
    scale_msld_system(system, m)
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(pos)
    dyn = LambdaDynamics(ctx, m, temperature=300.0, timestep=0.001, seed=3)

    oref = ref_overlap(m.fnex, 2)                            # flat target (bare softmax)
    base = LambdaHistogram(m, every=50); dyn.run(4000, reporters=[base])
    o_base = base.overlap()[(1, 2)]
    assert o_base > oref + 0.03, (o_base, oref)              # trapped: midpoint over-occupied

    rep = flatten(dyn, couple=True, n_iters=50, steps_per_iter=2500, sample_every=50,
                  rate=0.4, couple_rate=0.6, max_step=4.0, floor=5e-3, tol=0.0, verbose=False)

    # the learned coupling counteracts the trap: k > 0 and roughly +A (tail-averaged)
    k_tail = np.mean([ch[0] for ch in rep["coupling_history"][-20:]])
    assert 0.4 * A < k_tail < 1.6 * A, (k_tail, A)

    after = LambdaHistogram(m, every=50); dyn.run(4000, reporters=[after])
    assert after.overlap()[(1, 2)] < o_base                  # un-trapped: overlap pulled back down


# ---------------------------------------------------------------------
# Phase 3 -- free-energy estimate (bias-corrected)
# ---------------------------------------------------------------------
def test_estimate_ddg_bias_difference_and_reference():
    # DDG(ref->b) = -(b_b - b_ref), tail-averaged over the flatten history; block 1 is the reference.
    model = MSLDModel(3, fnex=2.0)
    model.add_block(site=1, atoms=[1]); model.add_block(site=1, atoms=[2]); model.finalize()
    # synthetic bias_history: b1 = 0, b2 oscillating around -5  -> DDG(1->2) = -(-5) = +5
    report = {"bias_history": [{1: 0.0, 2: -5.0 + (0.5 if i % 2 else -0.5)} for i in range(20)]}
    ddg = estimate_ddg(report, model, tail=10)
    assert ddg[1] == (0.0, 0.0)                          # reference
    assert abs(ddg[2][0] - 5.0) < 1e-9 and ddg[2][1] > 0.0   # mean +5, non-zero SEM from the oscillation


def test_estimate_ddg_recovers_known_offset():
    dG = 6.0                                             # true DeltaDeltaG(block1 -> block2)
    system, pos = _biased_two_block_system(dG)          # injected dG*lambda2, no atomic forces
    m = _model()                                         # fnex=2, bias_flattening (Phase-1 model)
    scale_msld_system(system, m)
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions(pos)
    dyn = LambdaDynamics(ctx, m, temperature=300.0, timestep=0.001, seed=11)

    rep = flatten(dyn, couple=False, n_iters=60, steps_per_iter=2500, sample_every=50,
                  rate=0.3, floor=5e-3, tol=0.0, verbose=False)     # learn the bias
    ddg = estimate_ddg(rep, m, tail=25)

    assert ddg[1] == (0.0, 0.0)                          # reference variant
    mean2, sem2 = ddg[2]
    assert abs(mean2 - dG) < 2.0, (mean2, sem2, dG)      # recovers the injected free-energy offset


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nALF (Phase 1 + 2 + 3) tests passed")
