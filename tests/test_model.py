"""Tests for the MSLD data model.

Toy system, 10 atoms:
  atoms 0-3  = environment (block 0)
  site 1: block 1 = {4,5}, block 2 = {6}      (two substituents)
  site 2: block 3 = {7,8}, block 4 = {9}      (two substituents)
"""
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.model import MSLDModel


def build_toy():
    m = MSLDModel(n_atoms=10, fnex=5.5)
    m.add_block(site=1, atoms=[4, 5], theta0=0.3)
    m.add_block(site=1, atoms=[6], theta0=-0.2)
    m.add_block(site=2, atoms=[7, 8], theta0=0.1)
    m.add_block(site=2, atoms=[9], theta0=0.0)
    return m.finalize()


def test_site_bookkeeping():
    m = build_toy()
    assert m.n_blocks == 5
    assert m.n_sites == 3
    assert m.blocks_per_site == [1, 2, 2]
    assert m.site_bound == [0, 1, 3, 5]
    assert m.blocks_in_site(1) == [1, 2]
    assert m.blocks_in_site(2) == [3, 4]


def test_classify_bonded():
    m = build_toy()
    # all-environment term -> no scaling
    assert m.classify_bonded([0, 1, 2]) == []
    # within one substituent -> single factor
    assert m.classify_bonded([4, 5]) == [1]
    # environment + substituent -> single factor
    assert m.classify_bonded([3, 4]) == [1]
    # bridges two DIFFERENT sites -> product of two lambdas
    assert sorted(m.classify_bonded([5, 7])) == [1, 3]
    # bridges two blocks of the SAME site -> illegal
    try:
        m.classify_bonded([4, 6])
        assert False, "expected same-site error"
    except ValueError:
        pass


def test_classify_pair():
    m = build_toy()
    assert m.classify_pair(0, 1) == ("env",)          # both environment
    assert m.classify_pair(0, 4) == ("single", 1)     # env <-> substituent
    assert m.classify_pair(4, 5) == ("single", 1)     # same block
    assert m.classify_pair(6, 4) == ("exclude",)      # same site, diff block
    assert m.classify_pair(5, 9) == ("product", 1, 4) # different sites


def test_softmax_normalization_and_value():
    m = build_toy()
    theta = [0.0, 0.3, -0.2, 0.1, 0.0]  # index by block
    lam = m.lambda_from_theta(theta)
    assert abs(lam[0] - 1.0) < 1e-12                  # environment
    assert abs((lam[1] + lam[2]) - 1.0) < 1e-12       # site 1 sums to 1
    assert abs((lam[3] + lam[4]) - 1.0) < 1e-12       # site 2 sums to 1
    # hand-check block 1 vs 2 at site 1
    w1 = math.exp(5.5 * math.sin(0.3))
    w2 = math.exp(5.5 * math.sin(-0.2))
    assert abs(lam[1] - w1 / (w1 + w2)) < 1e-12


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nall model tests passed")
    print(build_toy().summary())
