"""Phase J: the ligand path — MCSMapper + the shared hybrid-local assembly.

MCS discovery uses RDKit (a normal dependency, declared in env/environment.yml):
  - build_hybrid_local_mapping turns a per-variant core correspondence into the same
    hybrid-local CoreMapping the peptide mapper produces (env core first, blocks appended,
    variant_index_maps filled, names made unique),
  - molecular_graph reads a structure into (adjacency, elements),
  - MCSMapper.get_mapping finds the shared scaffold by rdFMCS and feeds build_hybrid_local_mapping.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import parmed as pmd
from msld.prep import (build_hybrid_local_mapping, molecular_graph, MCSMapper, Mapper)


class _Atom:
    def __init__(self, name, z=6):
        self.name = name
        self.atomic_number = z


class _Struct:
    def __init__(self, atoms):
        self.atoms = atoms


# --------------------------------------------------------------- shared assembly helper
def test_build_hybrid_local_mapping_from_correspondence():
    # reference & variant share a 2-atom core (CA, CB); each has one unique tail atom
    ref = _Struct([_Atom("CA"), _Atom("CB"), _Atom("OX", 8)])
    var = _Struct([_Atom("CA"), _Atom("CB"), _Atom("NX", 7)])
    m = build_hybrid_local_mapping(
        {"REF": ref, "V": var},
        {"REF": {0: 0, 1: 1}, "V": {0: 0, 1: 1}},        # local pos -> core slot
        ["CA", "CB"], metadata={"reference": "REF"})

    assert sorted(m.atom_names[i] for i in m.env_atoms) == ["CA", "CB"]
    assert sorted(m.source_names[i] for i in m.blocks["REF"]) == ["OX"]
    assert sorted(m.source_names[i] for i in m.blocks["V"]) == ["NX"]
    # core atoms of both variants share the env indices; tails are appended past the core
    assert m.variant_index_maps["REF"][0] == m.variant_index_maps["V"][0]     # CA
    assert min(m.blocks["REF"] | m.blocks["V"]) >= len(m.env_atoms)
    m.validate()


def test_build_hybrid_local_mapping_renames_colliding_block_atoms():
    # both variants have a unique atom literally named "X"; the hybrid names must stay unique
    ref = _Struct([_Atom("CA"), _Atom("X")])
    var = _Struct([_Atom("CA"), _Atom("X")])
    m = build_hybrid_local_mapping({"REF": ref, "V": var},
                                   {"REF": {0: 0}, "V": {0: 0}}, ["CA"])
    names = list(m.atom_names.values())
    assert len(names) == len(set(names))
    srcs = [m.source_names[i] for blk in m.blocks.values() for i in blk]
    assert srcs.count("X") == 2                          # originals preserved


# --------------------------------------------------------------- molecular graph
def test_molecular_graph_from_parmed():
    st = pmd.Structure()
    for nm, z in [("C1", 6), ("C2", 6), ("O3", 8)]:
        st.add_atom(pmd.Atom(name=nm, atomic_number=z), "L", 1)
    st.bonds.append(pmd.Bond(st.atoms[0], st.atoms[1]))
    st.bonds.append(pmd.Bond(st.atoms[1], st.atoms[2]))
    adj, elem = molecular_graph(st)
    assert adj == [{1}, {0, 2}, {1}]
    assert elem == [6, 6, 8]


# --------------------------------------------------------------- the real MCS path (RDKit)
def test_mcs_is_a_mapper():
    assert isinstance(MCSMapper(), Mapper)


def test_mcs_requires_reference_and_variants():
    try:
        MCSMapper().get_mapping(None, {})
        assert False
    except ValueError as ex:
        assert "reference" in str(ex)


def _lig(tail_name, tail_z, tail_type):
    """A tiny C-C-tail molecule (real ParmEd Structure with bonds, for the rdFMCS path)."""
    st = pmd.Structure()
    for nm, z, ty in [("C1", 6, "CT"), ("C2", 6, "CT"), (tail_name, tail_z, tail_type)]:
        st.add_atom(pmd.Atom(name=nm, atomic_number=z, type=ty), "LIG", 1)
    st.bonds.append(pmd.Bond(st.atoms[0], st.atoms[1]))
    st.bonds.append(pmd.Bond(st.atoms[1], st.atoms[2]))
    return st


def test_mcs_finds_shared_scaffold():
    # reference C-C-O vs variant C-C-N: rdFMCS finds the 2-carbon core; O/N become the blocks.
    ref, var = _lig("O3", 8, "OH"), _lig("N3", 7, "N")
    m = MCSMapper(reference_name="REF").get_mapping(ref, {"V": var})
    assert len(m.env_atoms) == 2                                       # the shared scaffold
    assert sorted(m.atom_names[i] for i in m.env_atoms) == ["C1", "C2"]
    assert sorted(m.source_names[i] for i in m.blocks["REF"]) == ["O3"]
    assert sorted(m.source_names[i] for i in m.blocks["V"]) == ["N3"]
    m.validate()


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nPhase J MCS/assembly tests passed")
