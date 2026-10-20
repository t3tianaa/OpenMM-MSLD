import os, sys
from pathlib import Path
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO)

import openmm as mm
from msld.prep import ingest, build_msld_system, Site
from msld.integrator import LambdaDynamics
from msld.io import populations

MDM2 = Path('/Users/tetiana/Documents/sampling_project/msld/test_systems/mdm2')
OUT = MDM2 / 'out'

protein = ingest(MDM2/"mdm2_protein.pdb", forcefield=["amber14-all.xml"],
                 add_hydrogens=True)
peptide = ingest(MDM2/"mdm2_peptide.pdb", forcefield=["amber14-all.xml"],
                 add_hydrogens=True)
# Both input PDBs are chain A; the peptide is a separate (non-covalent) binding partner, so put it
# on its own chain. Otherwise protein + peptide read as one continuous chain A and viewers draw a
# spurious peptide bond across the (33 A) gap between the protein C-terminus and the peptide.
for r in peptide.residues:
    r.chain = "B"
env = protein + peptide

site = len(protein.residues) + 3

bundle = build_msld_system(
    environment=env,
    sites=[Site(
        residue=site,
        variants={
            "ILE": MDM2/"ILE_var.pdb",
            "LEU": MDM2/"LEU_var.pdb",
            "SER": MDM2/"SER_var.pdb",
            "VAL": MDM2/"VAL_var.pdb",
        },
        mapper="backbone",
    )],
    forcefield=["amber14-all.xml"],
    renormalize=True,
    solvate=True,
)

model = bundle.to_model()
# BLaDE convention: do NOT scale bond/angle terms by lambda (only torsions + nonbonded). If the
# bonds/angles were scaled, a switched-off variant (lambda->0) would lose its bonded restraints and
# its side chain would drift away from the shared core (held only by the weak CATS centroid). With
# bond/angle scaling off, every variant stays rigidly attached; only its coupling to the environment
# turns on/off. (The engine default is True so the scaling-machinery tests can exercise it.)
model.scale_bond = False
model.scale_angle = False
model.scale_system(bundle.system)
print("blocks at the site:", bundle.mapping.sites[0].block_names)

# theta-parameter choice (from a stability sweep on this site, see DEFERRED.md 'ALF'): with
# scale_bond/angle off + minimization the run is STABLE for any reasonable theta params (nothing
# blows up). theta_temp is governed by FRICTION only (not mass, not the FD step): higher friction
# cools it, but the finite-difference theta-force keeps theta hot (~1400 K at friction 20, ~2400 K
# at 10) -- it does NOT reach 300 K with this engine (the analytic-derivative plugin is the real
# fix). So: light-ish mass (mobile) + strong friction (coolest theta available). Populations are
# still approximate until the plugin / ALF flattening.
for bl in model.blocks[1:]:
    bl.theta_mass = 10.0
    bl.theta_friction = 20.0

# OpenCL is ~380x faster than Reference for this ~26k-atom solvated system, and the CPU platform
# now works too (all nonbonded forces share one exclusion set). Reference is far too slow here.
ctx = mm.Context(bundle.system, mm.VerletIntegrator(0.001),
                 mm.Platform.getPlatform("OpenCL"))
ctx.setPositions(bundle.structure.positions)

dyn = LambdaDynamics(ctx, model, temperature=300.0, timestep=0.001)
bundle.save(str(OUT))

# A freshly built/solvated hybrid has steric clashes -> MUST minimize or dynamics blows up step 1.
print(f"PE before minimize: {dyn.potential_energy():.1f} kJ/mol")
dyn.minimize(max_iterations=5000)
print(f"PE after  minimize: {dyn.potential_energy():.1f} kJ/mol")

dyn.run(10000,
        metrics=str(OUT/'metrics.csv'), metrics_every=100, mapping=bundle.mapping,
        trajectory=str(OUT/'traj.dcd'), trajectory_every=200, structure=bundle.structure)

print(populations(str(OUT/'metrics.csv')))
