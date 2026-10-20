"""Phase C: CoordinateAligner (Kabsch/SVD) + BackboneAligner + IdentityAligner.

The aligner returns the rigid transform mapping a variant into the reference frame, fitted on
the shared core (default: backbone). Verified:
  - kabsch recovers a known rigid motion exactly (and never a reflection),
  - after BackboneAligner the fit atoms overlay to ~0 RMSD,
  - a variant's BLOCK atom, transformed by the fit, lands in the reference frame,
  - IdentityAligner is a no-op, and the >=3-atom guard fires.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from msld.prep import (CoordinateAligner, BackboneAligner, IdentityAligner,
                       RigidTransform, kabsch)


# ---- tiny duck-typed structure (aligner reads only .name and .xx/.xy/.xz) -----
class _Atom:
    def __init__(self, name, xyz):
        self.name = name
        self.xx, self.xy, self.xz = float(xyz[0]), float(xyz[1]), float(xyz[2])


class _Struct:
    def __init__(self, named_xyz):
        self.atoms = [_Atom(n, xyz) for n, xyz in named_xyz]


def _random_rotation(seed=0):
    rng = np.random.default_rng(seed)
    Q, _ = np.linalg.qr(rng.standard_normal((3, 3)))
    if np.linalg.det(Q) < 0:                     # force a proper rotation (det +1)
        Q[:, 0] *= -1
    return Q


# --------------------------------------------------------------- kabsch
def test_kabsch_recovers_known_transform():
    rng = np.random.default_rng(1)
    P = rng.standard_normal((6, 3))
    R_true = _random_rotation(2)
    t_true = np.array([3.0, -1.0, 2.0])
    Q = P @ R_true.T + t_true                     # exact rigid image of P

    T = kabsch(P, Q)
    assert T.rmsd(P, Q) < 1e-9
    assert np.allclose(T.R, R_true, atol=1e-9)
    assert np.allclose(T.t, t_true, atol=1e-9)
    assert abs(np.linalg.det(T.R) - 1.0) < 1e-9   # proper rotation, no reflection


def test_kabsch_no_reflection_on_planar_data():
    # coplanar points must still yield a proper rotation (det +1), not a mirror
    P = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0]], float)
    R_true = _random_rotation(5)
    Q = P @ R_true.T + np.array([1.0, 2.0, 3.0])
    T = kabsch(P, Q)
    assert abs(np.linalg.det(T.R) - 1.0) < 1e-9
    assert T.rmsd(P, Q) < 1e-9


def test_kabsch_needs_three_points():
    try:
        kabsch(np.zeros((2, 3)), np.zeros((2, 3)))
        assert False, "expected a >=3-points error"
    except ValueError as ex:
        assert "3 points" in str(ex)


# --------------------------------------------------------------- RigidTransform
def test_matrix_round_trip_and_identity():
    T = kabsch(np.random.default_rng(3).standard_normal((5, 3)) * 2,
               np.random.default_rng(4).standard_normal((5, 3)) * 2)
    back = RigidTransform.from_matrix(T.as_matrix())
    assert np.allclose(back.R, T.R) and np.allclose(back.t, T.t)
    I = RigidTransform.identity()
    pts = np.random.default_rng(6).standard_normal((4, 3))
    assert np.allclose(I.apply(pts), pts)


# --------------------------------------------------------------- BackboneAligner
def _backbone(coords):
    # coords: dict name->xyz for at least N, CA, C, O
    return _Struct([(n, coords[n]) for n in coords])


def test_backbone_aligner_zero_rmsd_after_fit():
    ref_bb = {"N": (0, 0, 0), "CA": (1.5, 0, 0), "C": (2.5, 1.0, 0), "O": (2.5, 2.2, 0)}
    G = _random_rotation(7)
    shift = np.array([5.0, -3.0, 1.0])
    var_bb = {n: tuple(G @ np.array(xyz) + shift) for n, xyz in ref_bb.items()}

    T = BackboneAligner().align(_backbone(ref_bb), _backbone(var_bb))
    mob = np.array([var_bb[n] for n in ("N", "CA", "C", "O")])
    tgt = np.array([ref_bb[n] for n in ("N", "CA", "C", "O")])
    assert T.rmsd(mob, tgt) < 1e-9


def test_block_atom_lands_in_reference_frame():
    # a "true" residue in the reference frame: backbone + one side-chain (block) atom
    true = {"N": (0, 0, 0), "CA": (1.5, 0, 0), "C": (2.5, 1.0, 0), "O": (2.5, 2.2, 0),
            "CB": (1.5, -1.4, 0.3)}
    G = _random_rotation(9)
    shift = np.array([-2.0, 4.0, 6.0])
    variant = {n: tuple(G @ np.array(xyz) + shift) for n, xyz in true.items()}

    reference = _Struct([(n, true[n]) for n in ("N", "CA", "C", "O")])   # env/core only
    var_struct = _Struct([(n, variant[n]) for n in variant])
    T = BackboneAligner().align(reference, var_struct)

    # transforming the variant's block atom (CB) must recover its true reference-frame coord
    cb_back = T.apply(np.array(variant["CB"]))
    assert np.allclose(cb_back, true["CB"], atol=1e-9)


def test_backbone_aligner_needs_three_shared_atoms():
    ref = _Struct([("N", (0, 0, 0)), ("CA", (1, 0, 0))])       # only 2 backbone atoms
    var = _Struct([("N", (0, 0, 1)), ("CA", (1, 0, 1))])
    try:
        BackboneAligner().align(ref, var)
        assert False, "expected a >=3-shared-atoms error"
    except ValueError as ex:
        assert "3 shared fit atoms" in str(ex)


# --------------------------------------------------------------- IdentityAligner
def test_identity_aligner_is_noop():
    a = IdentityAligner()
    assert isinstance(a, CoordinateAligner)
    T = a.align(None, None)
    pts = np.array([[1.0, 2, 3], [4, 5, 6]])
    assert np.allclose(T.apply(pts), pts)


def test_backbone_aligner_is_coordinate_aligner():
    assert isinstance(BackboneAligner(), CoordinateAligner)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nPhase C aligner tests passed")
