"""Phase E: ChargeRenormalization (env averaging + block renorm + net-charge guard).

Thin class facade over the validated prep/charges numerics, operating IN PLACE on the hybrid.
Verified on small controlled structures (duck-typed: the class reads/writes only atom.charge /
atom.name):
  - shared env atoms that differ across variants get the per-atom average,
  - each block is nudged so its end-state net charge is a clean integer,
  - "spread" vs "proportional" distribute the correction differently,
  - the net-charge guard refuses variants that reach different integers.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.prep import (CoreMapping, ChargeRenormalization, SpreadRenormalizer,
                       ProportionalRenormalizer, BufferAwareRenormalizer)


class _Atom:
    def __init__(self, name, charge):
        self.name = name
        self.charge = float(charge)


class _Struct:
    def __init__(self, atoms):
        self.atoms = atoms


def _mapping():
    # hybrid atoms: 0,1 = shared env ; 2 = WT block ; 3 = VAR block
    return CoreMapping(
        env_atoms={0, 1}, blocks={"WT": {2}, "VAR": {3}},
        variant_index_maps={"WT": {0: 0, 1: 1, 2: 2}, "VAR": {0: 0, 1: 1, 2: 3}},
        metadata={"reference": "WT"},
    )


# --------------------------------------------------------------- env averaging + renorm
def test_env_average_and_block_renorm():
    # WT env = (0.1, -0.2), WT block = 0.1  -> WT residue net 0
    hybrid = _Struct([_Atom("N", 0.1), _Atom("O", -0.2), _Atom("CB", 0.1), _Atom("OG", -0.1)])
    # VAR's OWN env charges differ: (0.2, -0.1); VAR block = -0.1 -> VAR residue net 0
    var = _Struct([_Atom("N", 0.2), _Atom("O", -0.1), _Atom("OG", -0.1)])

    rep = SpreadRenormalizer().apply(hybrid, _mapping(), variants={"VAR": var})

    # env atoms averaged: (0.1,0.2)->0.15 ; (-0.2,-0.1)->-0.15
    assert abs(hybrid.atoms[0].charge - 0.15) < 1e-12
    assert abs(hybrid.atoms[1].charge - (-0.15)) < 1e-12
    # both blocks renormalized so each residue net is exactly the integer 0
    assert abs(hybrid.atoms[2].charge - 0.0) < 1e-12          # WT block: 0.1 -> 0.0
    assert abs(hybrid.atoms[3].charge - 0.0) < 1e-12          # VAR block: -0.1 -> 0.0
    assert rep.env is not None and len(rep.env.differing) == 2
    assert rep.block.target == {"WT": 0, "VAR": 0}
    for v in rep.block.final_net.values():
        assert abs(v - round(v)) < 1e-9


def test_apply_is_in_place():
    hybrid = _Struct([_Atom("N", 0.1), _Atom("O", -0.2), _Atom("CB", 0.1), _Atom("OG", -0.1)])
    var = _Struct([_Atom("N", 0.1), _Atom("O", -0.2), _Atom("OG", -0.1)])
    before = hybrid.atoms[2]
    SpreadRenormalizer().apply(hybrid, _mapping(), variants={"VAR": var})
    assert hybrid.atoms[2] is before                          # same object, mutated in place


def test_no_variants_skips_env_averaging():
    hybrid = _Struct([_Atom("N", 0.1), _Atom("O", -0.2), _Atom("CB", 0.1), _Atom("OG", -0.1)])
    rep = SpreadRenormalizer(average_env=True).apply(hybrid, _mapping(), variants=None)
    assert rep.env is None                                    # nothing to average against
    assert abs(hybrid.atoms[0].charge - 0.1) < 1e-12          # env unchanged


# --------------------------------------------------------------- method: spread vs proportional
def test_spread_vs_proportional_distribution():
    # a 2-atom WT block with unequal |charge|; correction of +0.2 to reach net 0 (within tol)
    #   env sum 0 ; block atoms (0.0, -0.2) -> raw net -0.2 -> target 0 -> +0.2 correction
    m = CoreMapping(env_atoms={0}, blocks={"WT": {1, 2}, "VAR": {3}},
                    variant_index_maps={"WT": {0: 0, 1: 1, 2: 2}, "VAR": {0: 0, 1: 3}},
                    metadata={"reference": "WT"})

    def run(cls):
        h = _Struct([_Atom("N", 0.0), _Atom("Ca", 0.0), _Atom("Cb", -0.2), _Atom("X", 0.0)])
        cls(average_env=False).apply(h, m, variants=None)
        return h.atoms[1].charge, h.atoms[2].charge

    s1, s2 = run(SpreadRenormalizer)          # equal: +0.1 each -> (0.1, -0.1)
    p1, p2 = run(ProportionalRenormalizer)    # weighted by |q|: all onto the -0.2 atom -> (0, 0)
    assert abs(s1 - 0.1) < 1e-9 and abs(s2 - (-0.1)) < 1e-9
    assert abs(p1 - 0.0) < 1e-9 and abs(p2 - 0.0) < 1e-9
    assert (s1, s2) != (p1, p2)


# --------------------------------------------------------------- net-charge guard
def test_guard_refuses_unequal_integer_nets():
    # WT residue net 0 ; VAR block pushed so VAR net rounds to +1 -> different integers -> raise
    hybrid = _Struct([_Atom("N", 0.0), _Atom("O", 0.0), _Atom("W", 0.0), _Atom("V", 0.9)])
    m = CoreMapping(env_atoms={0, 1}, blocks={"WT": {2}, "VAR": {3}},
                    variant_index_maps={"WT": {0: 0, 1: 1, 2: 2}, "VAR": {0: 0, 1: 1, 2: 3}},
                    metadata={"reference": "WT"})
    try:
        SpreadRenormalizer(average_env=False).apply(hybrid, m, variants=None)
        assert False, "expected a net-charge guard error"
    except ValueError as ex:
        assert "net charge" in str(ex)


# --------------------------------------------------------------- buffer atoms (ligand path)
def test_plain_renormalizer_refuses_buffer_atoms():
    hybrid = _Struct([_Atom("N", 0.0), _Atom("B", 0.2), _Atom("W", -0.2), _Atom("V", -0.2)])
    m = CoreMapping(env_atoms={0, 1}, blocks={"WT": {2}, "VAR": {3}}, buffer_atoms={1},
                    variant_index_maps={"WT": {0: 0, 1: 1, 2: 2}, "VAR": {0: 0, 1: 1, 2: 3}},
                    metadata={"reference": "WT"})
    try:
        SpreadRenormalizer(average_env=False).apply(hybrid, m, variants=None)
        assert False, "expected buffer_atoms to be refused by the plain renormalizer"
    except NotImplementedError as ex:
        assert "buffer" in str(ex)


def test_buffer_aware_keeps_buffer_and_averages_the_rest():
    # env {0=N (regular), 1=B (buffer)} ; blocks WT={2}, VAR={3}. Nets are integer (0).
    hybrid = _Struct([_Atom("N", 0.1), _Atom("B", 0.2), _Atom("W", -0.4), _Atom("V", -0.4)])
    m = CoreMapping(env_atoms={0, 1}, blocks={"WT": {2}, "VAR": {3}}, buffer_atoms={1},
                    variant_index_maps={"WT": {0: 0, 1: 1, 2: 2}, "VAR": {0: 0, 1: 1, 2: 3}},
                    metadata={"reference": "WT"})
    var = _Struct([_Atom("N", 0.3), _Atom("B", 0.9), _Atom("V", -0.4)])   # B differs a lot

    rep = BufferAwareRenormalizer().apply(hybrid, m, variants={"VAR": var})
    assert abs(hybrid.atoms[0].charge - 0.2) < 1e-12          # N (regular env) averaged: 0.2
    assert abs(hybrid.atoms[1].charge - 0.2) < 1e-12          # B (buffer) kept the reference value
    for v in rep.block.final_net.values():                   # nets still land on the integer
        assert abs(v - round(v)) < 1e-9


def test_default_is_spread():
    assert ChargeRenormalization().method == "spread"
    assert SpreadRenormalizer().method == "spread"
    assert ProportionalRenormalizer().method == "proportional"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nPhase E charge-renormalization tests passed")
