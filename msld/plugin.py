"""Nonbonded terms through the C++ plugin (t3tianaa/openmm-ld) instead of stock OpenMM forces.

Opt-in (`model.use_plugin = True` or `scale_msld_system(..., use_plugin=True)`). One
`msldplugin.MSLDNonbondedForce`, built from the system's NonbondedForce (plus ParmEd's acoef/bcoef
LJ table on CHARMM/NBFIX systems), replaces the NonbondedForce, the within-block correction, the
soft-core forces, the scaled LJ forces and the 1-4 offsets. It computes the same energy (frozen spec,
vault: MSLD energy function spec) and gives dU/dlambda analytically, so LambdaDynamics needs no
finite difference for it. Bonded, bias and restraint forces stay as they are.

The kernels run on the Reference and CPU platforms. `msldplugin` has to be importable and its kernel
library loaded: either `cmake --install` in openmm-ld, or PYTHONPATH=<build>/python and
MSLD_REFERENCE_PLUGIN=<path to libOpenMMMSLDReference>.
"""
from __future__ import annotations

import os

import openmm as mm

from . import forces

PLUGIN_FORCE_NAME = "MSLDNonbondedForce"

_loaded_library = None


def load_msldplugin():
    """Import msldplugin and, when MSLD_REFERENCE_PLUGIN is set, load its kernel library once."""
    global _loaded_library
    try:
        import msldplugin
    except ImportError as e:
        raise ImportError("use_plugin needs the msldplugin module from t3tianaa/openmm-ld "
                          "(cmake --install, or PYTHONPATH=<build>/python)") from e
    library = os.environ.get("MSLD_REFERENCE_PLUGIN")
    if library and library != _loaded_library:
        msldplugin.loadReferencePlugin(library)
        _loaded_library = library
    return msldplugin


def is_plugin_force(force) -> bool:
    """True for the plugin's force. System.getForce returns it as a plain Force, so go by name."""
    return force.getName() == PLUGIN_FORCE_NAME


def _is_tabulated_lj(f, n_particles) -> bool:
    """A non-MSLD CustomNonbondedForce spanning all particles: the CHARMM tabulated LJ."""
    return (isinstance(f, mm.CustomNonbondedForce) and f.getNumParticles() == n_particles
            and not (f.getName() or "").startswith("MSLD"))


def _apply_tabulated_lj(force, lj):
    """LJ types and per-type-pair (sigma, epsilon) from ParmEd's acoef/bcoef tables, in which
    U = (a/r^6)^2 - b/r^6, so sigma^6 = a^2/b and 4 eps = b^2/a^2. Every pair of types goes in as an
    override, so the table is reproduced exactly (NBFIX already folded in)."""
    per_params = [lj.getPerParticleParameterName(k) for k in range(lj.getNumPerParticleParameters())]
    tabs = {lj.getTabulatedFunctionName(t): lj.getTabulatedFunction(t)
            for t in range(lj.getNumTabulatedFunctions())}
    if not forces._is_parmed_ab_table(per_params, list(tabs.items())):
        raise NotImplementedError("use_plugin needs ParmEd's acoef/bcoef LJ table; this tabulated "
                                  f"LJ has parameters {per_params} and tables {sorted(tabs)}")
    nx, ny, acoef = tabs["acoef"].getFunctionParameters()
    _, _, bcoef = tabs["bcoef"].getFunctionParameters()
    if nx != ny:
        raise NotImplementedError(f"use_plugin: non-square LJ table ({nx} x {ny})")

    for t1 in range(nx):
        for t2 in range(t1, nx):
            a, b = acoef[t1 + nx * t2], bcoef[t1 + nx * t2]
            if a != acoef[t2 + nx * t1] or b != bcoef[t2 + nx * t1]:
                raise NotImplementedError(f"use_plugin: asymmetric LJ table at types {t1}, {t2}")
            if b > 0.0 and a != 0.0:
                force.addNBFixPair(t1, t2, (a * a / b) ** (1.0 / 6.0), b * b / (4.0 * a * a))
            elif a == 0.0 and b == 0.0:
                force.addNBFixPair(t1, t2, 1.0, 0.0)
            else:
                raise NotImplementedError(f"use_plugin: LJ table entry a={a}, b={b} at types {t1}, "
                                          f"{t2} has no (sigma, epsilon) form")
    for i in range(lj.getNumParticles()):
        force.setParticleLJType(i, int(lj.getParticleParameters(i)[0]))


def replace_nonbonded_with_plugin(system: mm.System, model) -> tuple:
    """Replace the system's nonbonded forces by one MSLDNonbondedForce, in place.

    Returns (the force, the number of alchemical 1-4 exceptions it scales). Raises where the stock
    route does (cross-site or same-site 1-4 exceptions) and on anything the plugin cannot represent.
    """
    msldplugin = load_msldplugin()
    NB, P = mm.NonbondedForce, msldplugin.MSLDNonbondedForce
    nbfs = forces._forces_of_type(system, mm.NonbondedForce)
    if len(nbfs) != 1:
        raise ValueError(f"use_plugin needs exactly one NonbondedForce, found {len(nbfs)}")
    nbf = nbfs[0]
    if nbf.getNumParticleParameterOffsets() or nbf.getNumExceptionParameterOffsets():
        raise ValueError("use_plugin: the NonbondedForce already has parameter offsets")
    methods = {NB.NoCutoff: P.NoCutoff, NB.CutoffNonPeriodic: P.CutoffNonPeriodic,
               NB.CutoffPeriodic: P.CutoffPeriodic, NB.PME: P.PME}
    if nbf.getNonbondedMethod() not in methods:
        raise NotImplementedError(f"use_plugin: nonbonded method {nbf.getNonbondedMethod()} "
                                  "is not supported (Ewald, LJPME)")
    n_particles = system.getNumParticles()
    tabulated = [f for f in system.getForces() if _is_tabulated_lj(f, n_particles)]
    if len(tabulated) > 1:
        raise NotImplementedError("use_plugin: more than one tabulated LJ force")
    lj_force = tabulated[0] if tabulated else None

    force = P()
    force.setName(PLUGIN_FORCE_NAME)
    force.setNonbondedMethod(methods[nbf.getNonbondedMethod()])
    force.setCutoffDistance(nbf.getCutoffDistance().value_in_unit(forces._NM))
    # the switching function acts on LJ only, so it comes from whichever force holds the LJ
    switch_source = lj_force if lj_force is not None else nbf
    force.setUseSwitchingFunction(switch_source.getUseSwitchingFunction())
    force.setSwitchingDistance(switch_source.getSwitchingDistance().value_in_unit(forces._NM))
    force.setReactionFieldDielectric(nbf.getReactionFieldDielectric())
    force.setEwaldErrorTolerance(nbf.getEwaldErrorTolerance())
    alpha, nx, ny, nz = nbf.getPMEParameters()
    force.setPMEParameters(alpha.value_in_unit(forces._NM ** -1), nx, ny, nz)
    force.setExceptionsUsePeriodicBoundaryConditions(nbf.getExceptionsUsePeriodicBoundaryConditions())
    force.setSoftcoreAlpha(forces.softcore_alpha(model))
    force.setSoftcoreSigmaQ(float(model.softcore_sigma_q))
    if lj_force is not None and nbf.getNonbondedMethod() != NB.NoCutoff:
        if abs(lj_force.getCutoffDistance().value_in_unit(forces._NM)
               - nbf.getCutoffDistance().value_in_unit(forces._NM)) > 1e-12:
            raise NotImplementedError("use_plugin: tabulated LJ and NonbondedForce cutoffs differ")

    for b in range(1, model.n_blocks):
        if force.addBlock(model.blocks[b].site) != b:
            raise RuntimeError("use_plugin: block numbering mismatch")
    for i in range(n_particles):
        q, sig, eps = nbf.getParticleParameters(i)
        force.addParticle(q.value_in_unit(forces._E), sig.value_in_unit(forces._NM),
                          eps.value_in_unit(forces._KJ), model.atom_block[i])

    scaled = 0
    excluded = set()
    for k in range(nbf.getNumExceptions()):
        p1, p2, cp, sig, eps = nbf.getExceptionParameters(k)
        cpv, epsv = cp.value_in_unit(forces._E ** 2), eps.value_in_unit(forces._KJ)
        if cpv != 0.0 or epsv != 0.0:
            cls = model.classify_pair(p1, p2)
            if cls[0] == "product":
                raise NotImplementedError(f"cross-site 1-4 exception; atoms {p1},{p2}")
            if cls[0] == "exclude":
                raise NotImplementedError(f"same-site 1-4 exception (illegal MSLD topology?); "
                                          f"atoms {p1},{p2}")
            scaled += cls[0] == "single"
        force.addException(p1, p2, cpv, sig.value_in_unit(forces._NM), epsv)
        excluded.add((min(p1, p2), max(p1, p2)))

    if lj_force is not None:
        _apply_tabulated_lj(force, lj_force)
        for k in range(lj_force.getNumExclusions()):
            p1, p2 = lj_force.getExclusionParticles(k)
            if (min(p1, p2), max(p1, p2)) not in excluded:
                raise NotImplementedError(f"use_plugin: atoms {p1},{p2} are excluded from the "
                                          "tabulated LJ but not from the NonbondedForce")

    for i in reversed(range(system.getNumForces())):
        f = system.getForce(i)
        if isinstance(f, mm.NonbondedForce) or _is_tabulated_lj(f, n_particles):
            system.removeForce(i)
    system.addForce(force)
    return force, scaled


def exception_pairs(system: mm.System) -> set:
    """All (i, j), i < j, with an exception on the plugin force."""
    msldplugin = load_msldplugin()
    pairs = set()
    for f in system.getForces():
        if is_plugin_force(f):
            p = msldplugin.MSLDNonbondedForce.cast(f)
            for k in range(p.getNumExceptions()):
                i, j, *_ = p.getExceptionParameters(k)
                pairs.add((min(i, j), max(i, j)))
    return pairs
