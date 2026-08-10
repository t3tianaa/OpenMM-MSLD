"""Block-scaled force construction.

The problem: OpenMM's built-in bond/angle/torsion forces use a fixed energy
formula, so you cannot multiply them by a lambda.

The fix: for every term that a substituent's lambda should scale, take it out of
the built-in force and re-add it to a CustomForce whose energy formula carries
that lambda as a factor, e.g.  lambda1 * 0.5*k*(r-r0)^2. Block b's coupling is a
global parameter named lambda{b}, shared by all of that block's terms. We also
ask OpenMM to track dU/dlambda{b} (addEnergyParameterDerivative).

Convention: block b's coupling is the Context global parameter  lambda{b}
(e.g. "lambda1"). The environment (block 0) is never scaled and never gets one.

Implemented (bonded family, bilinear scaling = product of the <=2 block lambdas
whose atoms appear in the term):
  add_scaled_bonds     : HarmonicBondForce    -> CustomBondForce(s)
  add_scaled_angles    : HarmonicAngleForce   -> CustomAngleForce(s)
  add_scaled_torsions  : PeriodicTorsionForce -> CustomTorsionForce(s)

Planned (nonbonded):
  electrostatics + PME via NonbondedForce parameter offsets
  LJ scaling + same-site rule via CustomNonbondedForce
  fixed + variable (ALF) biases
"""
from __future__ import annotations

from collections import defaultdict

import openmm as mm
from openmm import unit

_NM = unit.nanometer
_RAD = unit.radian
_KJ = unit.kilojoule_per_mole
_KJ_PER_NM2 = _KJ / _NM**2
_KJ_PER_RAD2 = _KJ / _RAD**2


# --------------------------------------------------------------------- 
# Helpers 
# --------------------------------------------------------------------- 
def lambda_name(b: int) -> str:
    """Context global-parameter name for block b's coupling."""
    # block 1 -> "lambda1"
    return f"lambda{b}"


def _forces_of_type(system: mm.System, cls):
    """Return all forces of a given type in a System."""
    return [system.getForce(i) for i in range(system.getNumForces())
            if isinstance(system.getForce(i), cls)]


def _lambda_prefix(signature: tuple[int, ...]) -> str:
    """'lambda1' or 'lambda1*lambda3' etc. for the energy expression."""
    return "*".join(lambda_name(b) for b in signature)


def _register_lambdas(force, signature: tuple[int, ...]) -> None:
    """Declare block's global parameter and request its energy derivative."""
    for b in signature:
        force.addGlobalParameter(lambda_name(b), 1.0)       # declare the global (default 1.0)
        force.addEnergyParameterDerivative(lambda_name(b))  # dU/dlambda_b


# --------------------------------------------------------------------- 
# Bonds 
# --------------------------------------------------------------------- 
def add_scaled_bonds(system: mm.System, model) -> list[mm.CustomBondForce]:
    """HarmonicBondForce -> block-scaled CustomBondForce(s)."""
    created = []
    for hbf in _forces_of_type(system, mm.HarmonicBondForce):
        groups = defaultdict(list)
        # Classify each bond, and remove the scaled ones from the base force
        for i in range(hbf.getNumBonds()):
            p1, p2, length, k = hbf.getBondParameters(i)    # read bond i
            sig = tuple(model.classify_bonded([p1, p2]))    # which λ's scale it?
            if not sig:
                continue    # env-only -> keep in base force
            groups[sig].append((p1, p2, length.value_in_unit(_NM),
                                k.value_in_unit(_KJ_PER_NM2)))
            hbf.setBondParameters(i, p1, p2, length, 0.0 * k)   # zero it in the base force

        # build one CustomBondForce per signature
        for sig, bonds in groups.items():
            f = mm.CustomBondForce(f"{_lambda_prefix(sig)}*0.5*k*(r-length)^2")
            f.setName("MSLDBond_" + "_".join(map(str, sig)))
            _register_lambdas(f, sig)
            f.addPerBondParameter("length")
            f.addPerBondParameter("k")
            for p1, p2, length, k in bonds:
                f.addBond(p1, p2, [length, k])
            system.addForce(f)
            created.append(f)
    return created


# --------------------------------------------------------------------- 
# Angles 
# --------------------------------------------------------------------- 
def add_scaled_angles(system: mm.System, model) -> list[mm.CustomAngleForce]:
    """HarmonicAngleForce -> block-scaled CustomAngleForce(s)."""
    created = []
    for haf in _forces_of_type(system, mm.HarmonicAngleForce):
        groups = defaultdict(list)
        for i in range(haf.getNumAngles()):
            a1, a2, a3, angle, k = haf.getAngleParameters(i)
            sig = tuple(model.classify_bonded([a1, a2, a3]))
            if not sig:
                continue
            groups[sig].append((a1, a2, a3, angle.value_in_unit(_RAD),
                                k.value_in_unit(_KJ_PER_RAD2)))
            haf.setAngleParameters(i, a1, a2, a3, angle, 0.0 * k)
        for sig, angles in groups.items():
            f = mm.CustomAngleForce(f"{_lambda_prefix(sig)}*0.5*k*(theta-theta0)^2")
            f.setName("MSLDAngle_" + "_".join(map(str, sig)))
            _register_lambdas(f, sig)
            f.addPerAngleParameter("theta0")
            f.addPerAngleParameter("k")
            for a1, a2, a3, theta0, k in angles:
                f.addAngle(a1, a2, a3, [theta0, k])
            system.addForce(f)
            created.append(f)
    return created


# --------------------------------------------------------------------- 
# Torsions 
# --------------------------------------------------------------------- 
def add_scaled_torsions(system: mm.System, model) -> list[mm.CustomTorsionForce]:
    """PeriodicTorsionForce -> block-scaled CustomTorsionForce(s)."""
    created = []
    for ptf in _forces_of_type(system, mm.PeriodicTorsionForce):
        groups = defaultdict(list)
        for i in range(ptf.getNumTorsions()):
            a1, a2, a3, a4, per, phase, k = ptf.getTorsionParameters(i)
            sig = tuple(model.classify_bonded([a1, a2, a3, a4]))
            if not sig:
                continue
            groups[sig].append((a1, a2, a3, a4, int(per),
                                phase.value_in_unit(_RAD), k.value_in_unit(_KJ)))
            ptf.setTorsionParameters(i, a1, a2, a3, a4, per, phase, 0.0 * k)
        for sig, tors in groups.items():
            f = mm.CustomTorsionForce(
                f"{_lambda_prefix(sig)}*k*(1+cos(per*theta-phase))")
            f.setName("MSLDTorsion_" + "_".join(map(str, sig)))
            _register_lambdas(f, sig)
            f.addPerTorsionParameter("per")
            f.addPerTorsionParameter("phase")
            f.addPerTorsionParameter("k")
            for a1, a2, a3, a4, per, phase, k in tors:
                f.addTorsion(a1, a2, a3, a4, [per, phase, k])
            system.addForce(f)
            created.append(f)
    return created


# ---------------------------------------------------------------------
# Electrostatics + PME
# ---------------------------------------------------------------------
# Scale each alchemical atom's charge linearly with lambda:
#     charge = lambda_b * q_i        (full charge at lambda_b = 1)
#
# Because the dependence is linear, no custom force is needed. We keep the
# standard NonbondedForce and add a per-atom parameter offset that contributes
# lambda_b * q_i to the charge. This preserves native PME handling of long-range
# electrostatics with the scaled charges.
#
# Only charges are modified here. Lennard-Jones (epsilon) is handled separately
# in add_scaled_lj().
#
# Note: NonbondedForce does not expose dU/dlambda for parameter offsets, so that
# derivative is obtained by finite difference elsewhere.
_E = unit.elementary_charge


def _alch_blocks(model) -> list[int]:
    """Non-environment blocks that actually own atoms."""
    return sorted({model.atom_block[a] for a in range(model.n_atoms)
                   if model.atom_block[a] != 0})


def _existing_exception_pairs(nbf: mm.NonbondedForce) -> set:
    pairs = set()
    for k in range(nbf.getNumExceptions()):
        p1, p2, *_ = nbf.getExceptionParameters(k)
        pairs.add((min(p1, p2), max(p1, p2)))
    return pairs


def add_same_site_exclusions(nbf: mm.NonbondedForce, model) -> int:
    """Fully exclude every pair of atoms in different blocks of the SAME site
    (mutually-exclusive overlapping substituents must never interact). Skips
    pairs that already have an exception. Returns the number added."""
    existing = _existing_exception_pairs(nbf)
    added = 0
    for s in range(model.n_sites):
        blocks = model.blocks_in_site(s)
        for x in range(len(blocks)):
            for y in range(x + 1, len(blocks)):
                for a in model.blocks[blocks[x]].atoms:
                    for c in model.blocks[blocks[y]].atoms:
                        key = (min(a, c), max(a, c))
                        if key in existing:
                            continue
                        nbf.addException(a, c, 0.0, 0.0, 0.0)  # full exclusion
                        existing.add(key)
                        added += 1
    return added


def add_scaled_electrostatics(system: mm.System, model) -> mm.NonbondedForce | None:
    """Scale each alchemical atom's charge to lambda_b * q_i via NonbondedForce
    parameter offsets, and add same-site exclusions. LJ (epsilon) untouched.
    Returns the NonbondedForce, or None if the System has none."""
    nbfs = _forces_of_type(system, mm.NonbondedForce)
    if not nbfs:
        return None
    nbf = nbfs[0]
    # declare one global parameter per alchemical block
    for b in _alch_blocks(model):
        nbf.addGlobalParameter(lambda_name(b), 1.0)     

    # rewrite each alchemical atom's charge as λ_b * q_i
    for i in range(model.n_atoms):
        b = model.atom_block[i]
        if b == 0:
            continue
        # read original
        q, sig, eps = nbf.getParticleParameters(i)
        q0 = q.value_in_unit(_E)
        # base charge -> 0 (keep sigma/eps) 
        nbf.setParticleParameters(i, 0.0, sig, eps)     
        if q0 != 0.0:
            # +λ_b*q0 
            nbf.addParticleParameterOffset(lambda_name(b), i, q0, 0.0, 0.0)  

    # exclude same-site pairs
    add_same_site_exclusions(nbf, model)
    return nbf


# ---------------------------------------------------------------------
# Lennard-Jones
# ---------------------------------------------------------------------
# Each pair must be scaled by lambda_i * lambda_j (the product of the two atoms'
# lambdas). NonbondedForce cannot express this, since scaling epsilon yields 
# sqrt(lambda_i * lambda_j) instead.
#
# We therefore remove LJ for all alchemical pairs from NonbondedForce and move it
# into CustomNonbondedForce, where the energy expression is defined explicitly and
# multiplied by the desired lambda factor.
#
# One CustomNonbondedForce is created per pair "kind", each carrying a fixed lambda
# prefactor, with addInteractionGroup selecting the pairs it covers:
#     block b with environment, or block b with itself   ->  * lambda_b
#     block b with block c at a different site           ->  * lambda_b * lambda_c
#
# Atoms of the same site (competing substituents) are placed in no group, so they
# never interact. Plain environment-environment LJ remains in NonbondedForce.
# CustomNonbondedForce does expose dU/dlambda.
#
# Currently disabled (see DEFERRED.md): soft-core and the long-range dispersion
# correction.


def _match_nonbonded_method(cnbf: mm.CustomNonbondedForce, nbf: mm.NonbondedForce):
    """Copy method / cutoff / switching from a NonbondedForce so the LJ matches."""
    NB, CN = mm.NonbondedForce, mm.CustomNonbondedForce
    m = nbf.getNonbondedMethod()
    if m == NB.NoCutoff:
        cnbf.setNonbondedMethod(CN.NoCutoff)
    elif m == NB.CutoffNonPeriodic:
        cnbf.setNonbondedMethod(CN.CutoffNonPeriodic)
        cnbf.setCutoffDistance(nbf.getCutoffDistance())
    else:  # CutoffPeriodic, Ewald, PME, LJPME -> real-space cutoff, periodic
        cnbf.setNonbondedMethod(CN.CutoffPeriodic)
        cnbf.setCutoffDistance(nbf.getCutoffDistance())
    if nbf.getUseSwitchingFunction():
        cnbf.setUseSwitchingFunction(True)
        cnbf.setSwitchingDistance(nbf.getSwitchingDistance())
    cnbf.setUseLongRangeCorrection(False)   # dispersion correction OFF (deferred)

# LJ energy expression, with Lorentz-Berthelot combining rules for sigma/epsilon
_LJ_EXPR = ("*4*epsilon*((sigma/r)^12-(sigma/r)^6);"
            "sigma=0.5*(sigma1+sigma2); epsilon=sqrt(epsilon1*epsilon2)")


def add_scaled_lj(system: mm.System, model) -> list[mm.CustomNonbondedForce]:
    """Move all alchemical-involving LJ from the NonbondedForce into grouped,
    block-scaled CustomNonbondedForce(s). env<->env LJ stays put. Returns the
    created forces."""
    nbfs = _forces_of_type(system, mm.NonbondedForce)
    if not nbfs:
        return []
    nbf = nbfs[0]
    npart = system.getNumParticles()

    # capture original per-particle LJ (sigma, epsilon) BEFORE we zero anything
    lj = []
    for i in range(npart):
        _, sig, eps = nbf.getParticleParameters(i)
        lj.append((sig.value_in_unit(_NM), eps.value_in_unit(_KJ)))
    excl = sorted(_existing_exception_pairs(nbf))          # 1-2/1-3 + same-site + 1-4

    alch = _alch_blocks(model)
    env_atoms = [i for i in range(npart) if model.atom_block[i] == 0]
    block_atoms = {b: list(model.blocks[b].atoms) for b in alch}

    def _make(sig_tuple):
        f = mm.CustomNonbondedForce(_lambda_prefix(sig_tuple) + _LJ_EXPR)
        f.setName("MSLDLJ_" + "_".join(map(str, sig_tuple)))
        _match_nonbonded_method(f, nbf)
        f.addPerParticleParameter("sigma")
        f.addPerParticleParameter("epsilon")
        for s, e in lj:
            f.addParticle([s, e])
        for a, c in excl:
            f.addExclusion(a, c)
        _register_lambdas(f, sig_tuple)         # globals + analytic dU/dlambda
        return f

    created = []
    # single-lambda: env<->block b and within block b
    for b in alch:
        f = _make((b,))
        if env_atoms and block_atoms[b]:
            f.addInteractionGroup(env_atoms, block_atoms[b])
        if len(block_atoms[b]) >= 2:
            f.addInteractionGroup(block_atoms[b], block_atoms[b])
        system.addForce(f)
        created.append(f)
    # product-lambda: block b <-> block c, different sites only
    for x in range(len(alch)):
        for y in range(x + 1, len(alch)):
            b, c = alch[x], alch[y]
            if model.blocks[b].site == model.blocks[c].site:
                continue                        # same site -> never interact
            f = _make((b, c))
            f.addInteractionGroup(block_atoms[b], block_atoms[c])
            system.addForce(f)
            created.append(f)

    # remove alchemical LJ from the stock NonbondedForce (keep charge & sigma)
    for i in range(npart):
        if model.atom_block[i] != 0:
            q, sig, eps = nbf.getParticleParameters(i)
            nbf.setParticleParameters(i, q, sig, 0.0)
    nbf.setUseDispersionCorrection(False)       # deferred
    return created


# ---------------------------------------------------------------------
# 1-4 exceptions  
# ---------------------------------------------------------------------
# An exception in NonbondedForce replaces the normal interaction for one specific
# atom pair. Two kinds exist:
#   full exclusion : charge and epsilon set to 0 -> pair does not interact.
#                    Covers 1-2 and 1-3 neighbours, plus same-site pairs.
#   scaled 1-4     : charge and epsilon carry the force field's reduced "1-4"
#                    values, applied to atoms three bonds apart.
#
# Only the scaled 1-4 interactions need lambda scaling. When both atoms fall under
# a single lambda (same block, or one atom in the environment), the dependence is
# again linear in lambda_b, so an exception parameter offset handles it exactly:
#     charge  = lambda_b * (1-4 charge)
#     epsilon = lambda_b * (1-4 epsilon)
# (dU/dlambda here is finite difference, as elsewhere in NonbondedForce.)
#
# A 1-4 whose atoms lie in different sites (requiring lambda_i * lambda_j) or in
# the same site is rare or disallowed, so it currently raises an error.

def add_scaled_14_exceptions(system: mm.System, model) -> int:
    """Scale alchemical 1-4 exceptions by their single block lambda via exception
    parameter offsets. Returns the number scaled. Raises on cross-site (product)
    or same-site 1-4 exceptions."""
    nbfs = _forces_of_type(system, mm.NonbondedForce)
    if not nbfs:
        return 0
    nbf = nbfs[0]
    scaled = 0
    for k in range(nbf.getNumExceptions()):
        p1, p2, cp, sig, eps = nbf.getExceptionParameters(k)
        cpv = cp.value_in_unit(_E**2)
        epsv = eps.value_in_unit(_KJ)
        if cpv == 0.0 and epsv == 0.0:
            continue                                 # full exclusion, nothing to scale
        if model.atom_block[p1] == 0 and model.atom_block[p2] == 0:
            continue                                 # environment 1-4, leave as-is
        cls = model.classify_pair(p1, p2)
        if cls[0] == "single":
            b = cls[1]
            nbf.setExceptionParameters(k, p1, p2, 0.0, sig, 0.0)   # base -> 0
            nbf.addExceptionParameterOffset(lambda_name(b), k, cpv, 0.0, epsv)
            scaled += 1
        elif cls[0] == "product":
            raise NotImplementedError(
                f"cross-site 1-4 exception scaling is deferred (rare); atoms {p1},{p2}")
        elif cls[0] == "exclude":
            raise NotImplementedError(
                f"same-site 1-4 exception (illegal MSLD topology?); atoms {p1},{p2}")
    return scaled


# ---------------------------------------------------------------------
# Biasing potentials (ALF)
# ---------------------------------------------------------------------
# MSLD needs biases on lambda to flatten the landscape (ALF). These are pure
# functions of the lambda globals -- no atom positions -- so we add ONE
# CustomExternalForce on a dummy particle whose energy is the whole bias sum
# written in terms of lambda{b}. Its atom force is zero (no x,y,z in the
# expression); its dU/dlambda is picked up by the finite-difference gradient.
#
# Fixed bias : sum_b  bias_b * lambda_b            (linear)
# Variable   : ALF coupling biases between two blocks i, j (BLaDE types):
#     6  quadratic : k * li * lj
#     8  endpoint  : k * li * lj / (li + l0)
#     10 skew      : k * lj * (1 - exp(l0 * li))


def _variable_bias_term(vb) -> str:
    li, lj = lambda_name(vb.i), lambda_name(vb.j)
    k, l0 = vb.k, vb.l0
    if vb.type == 6:
        return f"({k})*{li}*{lj}"
    if vb.type == 8:
        return f"({k})*{li}*{lj}/({li}+({l0}))"
    if vb.type == 10:
        return f"({k})*{lj}*(1-exp(({l0})*{li}))"
    raise NotImplementedError(
        f"variable bias type {vb.type} not implemented (have 6, 8, 10)")


def add_biases(system: mm.System, model) -> mm.CustomExternalForce | None:
    """Add fixed + variable lambda biases as one position-independent force.
    Returns the force, or None if there are no biases."""
    terms, refs = [], set()
    for b in range(1, model.n_blocks):
        bias = model.blocks[b].lambda_bias
        if bias != 0.0:
            terms.append(f"({bias})*{lambda_name(b)}")
            refs.add(b)
    for vb in model.variable_biases:
        terms.append(_variable_bias_term(vb))
        refs.update((vb.i, vb.j))
    if not terms:
        return None

    f = mm.CustomExternalForce(" + ".join(terms))
    f.setName("MSLDBias")
    for b in sorted(refs):
        f.addGlobalParameter(lambda_name(b), 1.0)
    f.addParticle(0, [])          # dummy anchor; energy does not depend on its position
    system.addForce(f)
    return f


# ---------------------------------------------------------------------
# Atom restraints (CATS) 
# ---------------------------------------------------------------------
# Keep each substituent's atoms near their own centroid so a "switched-off"
# substituent (lambda ~ 0) does not drift away. BLaDE: U = 0.5*k*sum_i |x_i - xbar|^2.
# That centroid restraint is IDENTICAL to a harmonic term over every in-group
# pair with force constant k/N, so we just add pair bonds -- no centroid needed:
#     0.5*k*sum_i |x_i - xbar|^2  ==  (k/(2N)) * sum_{i<j} |x_i - x_j|^2
# The restraint is NOT lambda-scaled (always on), matching BLaDE.


def add_atom_restraints(system: mm.System, model) -> mm.CustomBondForce | None:
    """Add centroid restraints for each group in model.atom_restraints."""
    if not model.atom_restraints:
        return None
    f = mm.CustomBondForce("0.5*kr*r^2")
    f.setName("MSLDAtomRestraint")
    f.addPerBondParameter("kr")
    added = 0
    for group in model.atom_restraints:
        n = len(group)
        if n < 2:
            continue
        kr = model.k_restraint / n               # per-pair constant (see identity above)
        for a in range(n):
            for c in range(a + 1, n):
                f.addBond(group[a], group[c], [kr])
                added += 1
    if added == 0:
        return None
    system.addForce(f)
    return f
