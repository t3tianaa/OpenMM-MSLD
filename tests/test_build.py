"""build_msld_system façade: ingest-per-part + site wiring, on the real MDM2 peptide (Amber ff14SB).

Verifies:
  - the gate THROUGH the façade: with the WT block on, the hybrid reproduces the untouched
    peptide energy exactly (same correctness bar as test_hybrid_system, now via build_msld_system),
  - a site can be given as a residue index OR as explicit atom indices,
  - the per-part force-field logic (inherit / override / extend) that lets a non-standard residue
    carry its OWN ffxml on top of the standard one,
  - the mapper shorthands ('backbone' / 'mcs') and their errors.
"""
import copy
import os
import sys
import warnings

import numpy as np
import openmm as mm
import parmed as pmd
from openmm import app, unit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from msld.prep import (build_msld_system, Site, Part,
                       AminoAcidBackboneMapper, MCSMapper)
from msld.prep.build import _effective_ff, _resolve_mapper, _resolve_part
from msld.builder import scale_msld_system, set_lambdas

_REF = mm.Platform.getPlatform("Reference")
_KJ = unit.kilojoule_per_mole
_PDB = os.path.join(os.path.dirname(__file__), "..", "test_systems", "mdm2", "mdm2_peptide.pdb")
_cache = {}


def _fixture():
    """Parametrized, clash-minimized peptide + a SER donor side chain (from residue 2)."""
    if "st" not in _cache:
        pdb = app.PDBFile(_PDB)
        ff = app.ForceField("amber14-all.xml")
        mod = app.Modeller(pdb.topology, pdb.positions)
        mod.addHydrogens(ff)
        sysm = ff.createSystem(mod.topology, nonbondedMethod=app.NoCutoff)
        ctx = mm.Context(sysm, mm.VerletIntegrator(0.001), _REF)
        ctx.setPositions(mod.positions)
        mm.LocalEnergyMinimizer.minimize(ctx, maxIterations=200)
        xyz = np.array(ctx.getState(getPositions=True).getPositions()
                       .value_in_unit(unit.nanometer)) * 10.0
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            st = pmd.openmm.load_topology(mod.topology, system=sysm, xyz=xyz)
        ser = _extract(st, [a.idx for a in list(st.residues)[1].atoms])
        e_wt = _energy(st.createSystem(nonbondedMethod=app.NoCutoff), st.coordinates)
        _cache.update(st=st, ser=ser, e_wt=e_wt)
    return _cache["st"], _cache["ser"], _cache["e_wt"]


def _extract(st, idx):
    sub = copy.copy(st)
    keep = set(idx)
    sub.strip(np.array([i not in keep for i in range(len(st.atoms))]))
    return sub


def _energy(system, coords_ang, lambdas=None):
    ctx = mm.Context(system, mm.VerletIntegrator(0.001), _REF)
    ctx.setPositions((np.array(coords_ang) / 10.0).tolist() * unit.nanometer)
    if lambdas is not None:
        set_lambdas(ctx, lambdas)
    return ctx.getState(getEnergy=True).getPotentialEnergy().value_in_unit(_KJ)


# --------------------------------------------------------------- the gate, via the façade
def test_build_msld_system_wt_on_reproduces_peptide():
    st, ser, e_wt = _fixture()
    bundle = build_msld_system(
        environment=st,                                  # a Structure directly (no file)
        sites=[Site(residue=3, variants={"SER": ser}, mapper="backbone")],   # ALA4 is residue index 3
        renormalize=False, solvate=False)

    model = bundle.to_model(add_restraints=False)
    scale_msld_system(bundle.system, model)
    e_on = _energy(bundle.system, bundle.structure.coordinates, [1.0, 1.0, 0.0])   # WT on, SER off
    assert abs(e_on - e_wt) / max(1.0, abs(e_wt)) < 1e-9, (e_on, e_wt)
    assert model.blocks_in_site(1) == [1, 2]             # WT + SER


def test_site_by_explicit_atom_indices():
    st, ser, _ = _fixture()
    ala4 = [a.idx for a in list(st.residues)[3].atoms]
    bundle = build_msld_system(
        environment=st,
        sites=[Site(residue=ala4, variants={"SER": ser}, mapper="backbone")],   # explicit atoms
        renormalize=False, solvate=False)
    assert len(bundle.mapping.sites) == 1
    assert bundle.mapping.sites[0].block_names == ["WT", "SER"]


# --------------------------------------------------------------- per-part force field (>1 ffxml)
def test_effective_ff_inherit_override_extend():
    default = ["amber14-all.xml"]
    assert _effective_ff(Part("x.pdb"), default) == ["amber14-all.xml"]                        # inherit
    assert _effective_ff(Part("x.pdb", forcefield=["charmm36.xml"]), default) == ["charmm36.xml"]  # override
    # a NON-STANDARD residue: standard ffxml + its own residue ffxml
    assert _effective_ff(Part("ptr.pdb", extra_forcefield=["phosphotyr.xml"]), default) == \
        ["amber14-all.xml", "phosphotyr.xml"]                                                   # extend
    assert _effective_ff(Part("val.prmtop"), None) is None                                     # self-contained


# --------------------------------------------------------------- mapper shorthands
def test_mapper_shorthands_and_errors():
    m = _resolve_mapper("backbone", "WT")
    assert isinstance(m, AminoAcidBackboneMapper) and m.reference_name == "WT"
    assert isinstance(_resolve_mapper("mcs", "REF"), MCSMapper)
    inst = AminoAcidBackboneMapper(reference_name="WT")
    assert _resolve_mapper(inst, "WT") is inst           # a Mapper instance passes through
    for bad, msg in [(None, "needs a mapper"), ("bogus", "unknown mapper")]:
        try:
            _resolve_mapper(bad, "WT")
            assert False
        except ValueError as ex:
            assert msg in str(ex)


# --------------------------------------------------------------- monomer variant (no caps)
def _monomer_ser_pdb():
    """A lone IN-CHAIN SER residue written to a PDB (no caps, no OXT) -- the user's monomer input."""
    if "monopdb" not in _cache:
        import tempfile
        st, _, _ = _fixture()
        ser_res = _extract(st, [a.idx for a in list(st.residues)[1].atoms])   # in-chain SER
        path = os.path.join(tempfile.mkdtemp(), "ser_monomer.pdb")
        ser_res.save(path, overwrite=True)                   # PDB drops params -> a bare monomer
        _cache["monopdb"] = path
    return _cache["monopdb"]


def test_resolve_part_accepts_pathlib_path():
    # a variant given as a pathlib.Path (not str) is ingested, not mistaken for a Structure
    from pathlib import Path
    st = _resolve_part(Path(_monomer_ser_pdb()), ["amber14-all.xml"], False,
                       ignore_external_bonds=True)
    assert [r.name for r in st.residues] == ["SER"] and st.bonds


def test_monomer_without_ignore_external_bonds_fails():
    # a lone residue has NO template unless external bonds are ignored -- this is exactly why the
    # old caps trick existed. OpenMM: "No template found ... missing a terminal capping group".
    try:
        _resolve_part(Part(_monomer_ser_pdb(), forcefield=["amber14-all.xml"]),
                      None, False, ignore_external_bonds=False)
        assert False, "expected a template error for a lone monomer"
    except Exception as ex:
        assert "template" in str(ex).lower(), ex


def test_monomer_variant_parametrized_with_ignore_external_bonds():
    # THE user route now: a plain MONOMER residue PDB (no caps) + an OpenMM ffxml, ingested with
    # ignore_external_bonds -> correct IN-CHAIN params, no terminal OXT/H, full bonded side chain.
    st = _resolve_part(Part(_monomer_ser_pdb(), forcefield=["amber14-all.xml"]),
                       None, False, ignore_external_bonds=True)      # the variant site default
    assert [r.name for r in st.residues] == ["SER"]
    atoms = {a.name for a in st.atoms}
    assert {"N", "CA", "C", "O", "CB", "OG"} <= atoms        # backbone + side chain
    assert "OXT" not in atoms                                # no terminal artifact
    assert abs(round(sum(a.charge for a in st.atoms))) == 0  # SER net charge is an integer (0)
    assert any(abs(a.charge) > 1e-6 for a in st.atoms)       # parametrized
    assert st.bonds and st.angles and st.dihedrals           # full bonded set
    cacb = [b for b in st.bonds if {b.atom1.name, b.atom2.name} == {"CA", "CB"}]
    assert cacb and cacb[0].type is not None                 # side-chain attachment bond, typed


def test_build_msld_system_ingests_monomer_variant_from_pdb():
    # a variant given as a plain MONOMER PDB path (no caps): build_msld_system ingests it with
    # ignore_external_bonds=True automatically (a variant is a fragment) and assembles the hybrid.
    st, _, _ = _fixture()
    bundle = build_msld_system(
        environment=st,
        sites=[Site(residue=3, variants={"SER": _monomer_ser_pdb()}, mapper="backbone")],
        forcefield=["amber14-all.xml"],
        renormalize=True, solvate=False)
    assert bundle.mapping.sites[0].block_names == ["WT", "SER"]
    assert bundle.mapping.sites[0].blocks["SER"]             # SER side chain grafted as a block


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("\nfaçade build tests passed")
