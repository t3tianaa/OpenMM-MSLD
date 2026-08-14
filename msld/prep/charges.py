"""Partial-charge policy for the hybrid topology.

  * Environment atoms keep one fixed charge (they are shared and appear once).
  * Each block (variant) keeps its own charges, but we renormalize them by a small
    amount so that sum(env charges) + sum(block charges) == a whole-number target
    (the correct net charge of that variant's residue/molecule).
  * Net-charge guard: every variant at a site must reach the same integer target.
    If they differ, the total system charge would change with lambda, which breaks
    PME. Charge-changing perturbations need charge restraints that the engine does 
    not have yet.
"""
from __future__ import annotations

import warnings
from dataclasses import dataclass

from .mapping import CoreMapping


@dataclass
class ChargeResult:
    """Outcome of renormalization.

    charges    : final per-atom charge (env atoms unchanged, block atoms adjusted).
    target     : variant name -> integer net charge it was forced to.
    raw_net    : variant name -> net charge BEFORE adjustment (env_local + raw block).
    correction : variant name -> total charge added to that block (target - raw_net).
    final_net  : variant name -> net charge AFTER adjustment (should equal target).
    """
    charges: dict[int, float]
    target: dict[str, int]
    raw_net: dict[str, float]
    correction: dict[str, float]
    final_net: dict[str, float]


# ---------------------------------------------------------------------
# Environment-charge averaging (needed for Amber)
# ---------------------------------------------------------------------
# The shared environment must carry one charge per atom.
# In CHARMM the backbone charges are standardized, so every variant already agrees.
# In Amber the charges are RESP-fit per residue, so a shared atom can carry a different
# charge in different variants. This is treated the following way: each atom charge becomes
# the per-atom average charge across the variants. The small residual is then absorbed by
# renormalize_charges.


@dataclass
class EnvChargeReport:
    """Outcome of averaging env charges across variants.

    averaged   : per-env-atom mean charge (same order as the input).
    differing  : list of (label, spread, avg, values) for atoms that were not equal.
    max_spread : the largest across-variant spread seen (in e).
    """
    averaged: list[float]
    differing: list[tuple]
    max_spread: float


def average_env_charges(per_variant, *, labels=None, equal_tol: float = 1e-6,
                        refuse_spread: float = 0.5, warn: bool = True) -> EnvChargeReport:
    """Average the environment charges across variants, per shared atom.

    per_variant : list over variants; each item is that variant's env charges in the
                  same order (position i is the same shared atom in every variant).
    labels      : optional names for the env atoms.

    Returns an EnvChargeReport. When any atom's charge differs across variants, 
    emits a warning saying we take the average. Raises if any atom's spread exceeds
    `refuse_spread`.
    """
    if not per_variant:
        raise ValueError("no variants given")
    n = len(per_variant[0])
    for k, pv in enumerate(per_variant):
        if len(pv) != n:
            raise ValueError(
                f"variant {k} has {len(pv)} env charges, expected {n} "
                f"(env atoms must correspond across variants)")

    averaged: list[float] = []
    differing: list[tuple] = []
    max_spread = 0.0
    for i in range(n):
        vals = [pv[i] for pv in per_variant]
        spread = max(vals) - min(vals)
        avg = sum(vals) / len(vals)
        averaged.append(avg)
        max_spread = max(max_spread, spread)
        if spread > equal_tol:
            label = labels[i] if labels is not None else i
            if spread > refuse_spread:
                raise ValueError(
                    f"env atom {label} charge varies by {spread:.3f} e across variants "
                    f"(> {refuse_spread}); it is not really a shared atom. This looks "
                    f"like a backbone mutation, not a side-chain site.")
            differing.append((label, spread, avg, list(vals)))

    if differing and warn:
        names = ", ".join(str(d[0]) for d in differing[:6])
        more = "" if len(differing) <= 6 else f" (+{len(differing) - 6} more)"
        warnings.warn(
            f"env charges differ across variants for {len(differing)} atom(s) "
            f"[{names}{more}], max spread {max_spread:.3f} e; taking the per-atom "
            f"average. Amber charges are residue-specific (RESP-fit), so this is "
            f"expected.", stacklevel=2)
    return EnvChargeReport(averaged=averaged, differing=differing, max_spread=max_spread)


def _require_charges(mapping: CoreMapping, charges: dict[int, float]) -> None:
    """Every env atom and every block atom must have a charge."""
    needed = set(mapping.env_atoms) | mapping.all_block_atoms()
    missing = sorted(needed - set(charges))
    if missing:
        raise ValueError(f"charges missing for atoms {missing}")


def variant_net_charges(mapping: CoreMapping,
                        charges: dict[int, float]) -> dict[str, float]:
    """Net charge of each variant's end state = sum(env charges) + sum(block charges).

    The environment sum is the same for every variant (env is shared), so the only
    thing that changes between variants is their own block.
    """
    _require_charges(mapping, charges)
    env_sum = sum(charges[a] for a in mapping.env_atoms)
    out: dict[str, float] = {}
    for name, atoms in mapping.blocks.items():
        out[name] = env_sum + sum(charges[a] for a in atoms)
    return out


def _resolve_targets(nets: dict[str, float], targets: dict[str, int] | None,
                     tol: float) -> dict[str, int]:
    """Decide the integer target for each variant.

    If `targets` is given, use it. Otherwise auto-detect: a correctly parametrized
    residue sums to an integer already, so we round - but only if we are close to an
    integer. If a raw net is far from any integer and no target was given, we refuse
    (it usually means missing atoms or wrong charges), and ask for explicit targets.
    """
    resolved: dict[str, int] = {}
    for name, net in nets.items():
        if targets is not None and name in targets:
            resolved[name] = int(targets[name])
            continue
        nearest = round(net)
        if abs(net - nearest) > tol:
            raise ValueError(
                f"variant '{name}' raw net charge {net:.4f} is far from an integer "
                f"(nearest {nearest}, tol {tol}). Pass explicit `targets` or check the "
                f"charges -- auto-rounding could pick the wrong integer.")
        resolved[name] = nearest
    return resolved


def assert_iso_charge(mapping: CoreMapping, charges: dict[int, float], *,
                      targets: dict[str, int] | None = None,
                      tol: float = 0.25) -> int:
    """Net-charge guard. Raises unless all variants share one integer net charge.

    Returns that shared integer. Use this to fail fast before building anything.
    """
    nets = variant_net_charges(mapping, charges)
    resolved = _resolve_targets(nets, targets, tol)
    distinct = set(resolved.values())
    if len(distinct) != 1:
        detail = ", ".join(f"{k}={v:+d}" for k, v in resolved.items())
        raise ValueError(
            f"variants at this site have different net charges ({detail}). MSLD needs "
            f"the same net charge on every variant; charge-changing perturbations need "
            f"charge restraints, which are not implemented (see DEFERRED.md).")
    return distinct.pop()


def renormalize_charges(mapping: CoreMapping, charges: dict[int, float], *,
                        targets: dict[str, int] | None = None,
                        tol: float = 0.25,
                        method: str = "spread") -> ChargeResult:
    """Adjust each block's charges so its end state hits a clean integer net charge.

    Environment charges are left untouched. The small correction (target - raw_net) is
    distributed over the block's atoms:
      - method "spread"       : equal share to every block atom (simplest, default).
      - method "proportional" : share weighted by |charge| (leaves near-zero atoms
                                 almost untouched).

    Enforces the net-charge guard (all variants same integer). Returns a ChargeResult.
    """
    _require_charges(mapping, charges)
    if mapping.buffer_atoms:
        raise NotImplementedError(
            "buffer_atoms (per-variant charge on shared atoms) is deferred to the "
            "ligand/MCS path (P6); the fix there is to move boundary atoms into the "
            "blocks. Leave buffer_atoms empty for now.")
    if method not in ("spread", "proportional"):
        raise ValueError(f"unknown method '{method}' (use 'spread' or 'proportional')")

    raw_net = variant_net_charges(mapping, charges)
    target = _resolve_targets(raw_net, targets, tol)

    # net-charge guard: one shared integer for the whole site
    distinct = set(target.values())
    if len(distinct) != 1:
        detail = ", ".join(f"{k}={v:+d}" for k, v in target.items())
        raise ValueError(
            f"variants at this site have different net charges ({detail}). MSLD needs "
            f"the same net charge on every variant; charge-changing perturbations need "
            f"charge restraints, which are not implemented (see DEFERRED.md).")

    new_charges = dict(charges)          # copy; env atoms stay as-is
    correction: dict[str, float] = {}
    final_net: dict[str, float] = {}

    for name, atoms in mapping.blocks.items():
        atoms = sorted(atoms)
        corr = target[name] - raw_net[name]
        correction[name] = corr

        if method == "spread":
            weights = [1.0] * len(atoms)
        else:  # proportional to |charge|
            weights = [abs(charges[a]) for a in atoms]
        wsum = sum(weights)
        if wsum == 0.0:                  # all-zero charges -> fall back to equal spread
            weights = [1.0] * len(atoms)
            wsum = float(len(atoms))

        for a, w in zip(atoms, weights):
            new_charges[a] = charges[a] + corr * (w / wsum)

        env_sum = sum(new_charges[e] for e in mapping.env_atoms)
        final_net[name] = env_sum + sum(new_charges[a] for a in atoms)

    return ChargeResult(charges=new_charges, target=target, raw_net=raw_net,
                        correction=correction, final_net=final_net)
