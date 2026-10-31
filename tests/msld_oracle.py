"""Independent NumPy oracle for the MSLD energy at partial lambda (NoCutoff systems).

Written from the definition of the MSLD energy function (vault: Multisite lambda dynamics,
Alchemical scaling rules in MSLD, BLaDE bonded term scaling, ADR-0043 soft-core), NOT from
msld/forces.py: plain pair and term loops, no OpenMM. It is the reference the Python engine is
tested against (FEAT-045 / TASK-067) and the specification the C++ plugin must reproduce.

Units: nm, kJ/mol, elementary charge, radians.

The energy, for lambda per block (block 0 = environment, lambda 1):

  bonded term   : prod(lambda_b for the distinct non-env blocks among its atoms) * U_term
                  (bonds 0.5 k (r-r0)^2, angles 0.5 k (t-t0)^2, torsions k (1+cos(n phi - phase)))
  nonbonded pair (i < j, not a 1-2/1-3/1-4 pair):
      both env                     : L = 1, plain LJ + Coulomb
      same block b, or env + b     : L = lambda_b
      blocks b, c at different sites: L = lambda_b * lambda_c
      different blocks, same site  : no interaction
    for L < 1 (and soft-core alpha > 0), Beutler soft-core on LJ and Coulomb:
      U_LJ  = L * 4 eps (1/s^2 - 1/s),           s    = (r/sigma)^6 + alpha (1 - L)
      U_C   = L * KE q_i q_j / r_sc,             r_sc = (r^6 + alpha (1 - L) sigma_q^6)^(1/6)
    (alpha = 0: plain L * (LJ + Coulomb)). Lorentz-Berthelot combining.
  1-4 pair      : L * (KE qq14 / r + 4 eps14 ((s14/r)^12 - (s14/r)^6)), L as above (no soft-core;
                  a 1-4 between blocks of different sites or of the same site is not supported)
  biases        : sum_b c_b lambda_b
                  + sum over variable biases (i, j, type, l0, k):
                      6  : k li lj
                      8  : k li lj / (li + l0)
                      10 : k lj (1 - exp(l0 li))
  restraints    : 0.5 k_r sum_i |x_i - centroid|^2 per group (not lambda-scaled)

lambda = softmax_site(fnex sin theta).

dU/dlambda_b is taken by complex-step differentiation of this same energy (exact to rounding), so
the oracle has no hand-written derivatives to get wrong. Every function used is complex-analytic.
"""
from __future__ import annotations

import numpy as np

KE = 138.935456          # OpenMM ONE_4PI_EPS0, kJ/mol nm / e^2


def _dist(xi, xj):
    d = xj - xi
    return np.sqrt(np.sum(d * d))


def _angle(x1, x2, x3):
    a, b = x1 - x2, x3 - x2
    return np.arccos(np.dot(a, b) / np.sqrt(np.dot(a, a) * np.dot(b, b)))


def _dihedral(x1, x2, x3, x4):
    b1, b2, b3 = x2 - x1, x3 - x2, x4 - x3
    """IUPAC sign convention (cis = 0, positive clockwise looking down 2->3), as OpenMM."""
    n1, n2 = np.cross(b1, b2), np.cross(b2, b3)
    return np.arctan2(np.sqrt(np.dot(b2, b2)) * np.dot(b1, n2), np.dot(n1, n2))


class Oracle:
    """spec: dict with
        positions  (N, 3) nm
        charge, sigma, epsilon        per atom
        atom_block                    per atom (0 = env)
        block_site                    per block (block 0 -> site 0)
        bonds    [(i, j, r0, k)], angles [(i, j, l, t0, k)], torsions [(i, j, l, m, n, phase, k)]
        pairs14  [(i, j, qq, sigma, eps)]  (already scaled 1-4 parameters)
        excluded set of (i, j), i < j: 1-2 and 1-3 pairs (and the 1-4 pairs)
        alpha, sigma_q                soft-core (alpha 0 = off)
        fixed_bias  per block; variable_biases [(i, j, type, l0, k)]
        restraints  [(atoms, k)]
        fnex
    """

    def __init__(self, spec):
        self.s = spec
        self.x = np.asarray(spec["positions"], dtype=float)
        self.block = list(spec["atom_block"])
        self.site = list(spec["block_site"])
        n = len(self.block)
        self.excluded = {(min(i, j), max(i, j)) for i, j in spec["excluded"]}
        # pair list classified once (geometry-independent)
        self.pairs = []
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) in self.excluded:
                    continue
                bi, bj = self.block[i], self.block[j]
                if bi and bj and bi != bj and self.site[bi] == self.site[bj]:
                    continue                                      # same site, different block
                self.pairs.append((i, j))

    # -- lambda --------------------------------------------------------------------------------
    def lambdas_from_theta(self, theta):
        lam = np.ones(len(self.site), dtype=complex if np.iscomplexobj(theta) else float)
        for s in sorted(set(self.site[1:])):
            js = [b for b in range(1, len(self.site)) if self.site[b] == s]
            w = np.exp(self.s["fnex"] * np.sin(np.array([theta[b] for b in js])))
            for b, wb in zip(js, w / w.sum()):
                lam[b] = wb
        return lam

    def _pair_L(self, lam, i, j):
        bi, bj = self.block[i], self.block[j]
        if bi == 0 and bj == 0:
            return None
        if bi == bj:
            return lam[bi]
        if bi == 0:
            return lam[bj]
        if bj == 0:
            return lam[bi]
        return lam[bi] * lam[bj]

    def _term_scale(self, lam, atoms):
        f = 1.0
        for b in sorted({self.block[a] for a in atoms if self.block[a] != 0}):
            f = f * lam[b]
        return f

    # -- energy --------------------------------------------------------------------------------
    def energy(self, lam):
        """Total MSLD potential energy (kJ/mol) at lambda (per block, index 0 = env)."""
        s, x = self.s, self.x
        q, sig, eps = s["charge"], s["sigma"], s["epsilon"]
        alpha, sq6 = s["alpha"], s["sigma_q"] ** 6
        U = 0.0
        for i, j, r0, k in s["bonds"]:
            U = U + self._term_scale(lam, (i, j)) * 0.5 * k * (_dist(x[i], x[j]) - r0) ** 2
        for i, j, l, t0, k in s["angles"]:
            U = U + self._term_scale(lam, (i, j, l)) * 0.5 * k * (_angle(x[i], x[j], x[l]) - t0) ** 2
        for i, j, l, m, n, ph, k in s["torsions"]:
            phi = _dihedral(x[i], x[j], x[l], x[m])
            U = U + self._term_scale(lam, (i, j, l, m)) * k * (1 + np.cos(n * phi - ph))
        for i, j in self.pairs:
            r = _dist(x[i], x[j])
            sg = 0.5 * (sig[i] + sig[j])
            ep = np.sqrt(eps[i] * eps[j])
            qq = KE * q[i] * q[j]
            L = self._pair_L(lam, i, j)
            if L is None:                                             # env-env
                U = U + 4 * ep * ((sg / r) ** 12 - (sg / r) ** 6) + qq / r
                continue
            if alpha > 0:
                sc = (r / sg) ** 6 + alpha * (1 - L)
                rsc = (r ** 6 + alpha * (1 - L) * sq6) ** (1.0 / 6.0)
                U = U + L * 4 * ep * (1 / sc ** 2 - 1 / sc) + L * qq / rsc
            else:
                U = U + L * (4 * ep * ((sg / r) ** 12 - (sg / r) ** 6) + qq / r)
        for i, j, qq14, s14, e14 in s["pairs14"]:
            r = _dist(x[i], x[j])
            L = self._pair_L(lam, i, j)
            u = KE * qq14 / r + 4 * e14 * ((s14 / r) ** 12 - (s14 / r) ** 6)
            U = U + (u if L is None else L * u)
        for b, c in enumerate(s["fixed_bias"]):
            if b:
                U = U + c * lam[b]
        for i, j, typ, l0, k in s["variable_biases"]:
            li, lj = lam[i], lam[j]
            if typ == 6:
                U = U + k * li * lj
            elif typ == 8:
                U = U + k * li * lj / (li + l0)
            elif typ == 10:
                U = U + k * lj * (1 - np.exp(l0 * li))
            else:
                raise ValueError(typ)
        for atoms, k in s["restraints"]:
            xa = x[list(atoms)]
            d = xa - xa.mean(axis=0)
            U = U + 0.5 * k * np.sum(d * d)
        return U

    def dU_dlambda(self, lam, h=1e-30):
        """Exact dU/dlambda_b (b >= 1) by complex step."""
        lam = np.asarray(lam, dtype=float)
        out = np.zeros(len(lam))
        for b in range(1, len(lam)):
            lc = lam.astype(complex)
            lc[b] += 1j * h
            out[b] = np.imag(self.energy(lc)) / h
        return out

    def dU_dtheta(self, theta, h=1e-30):
        """Exact dU/dtheta_b through the softmax, by complex step."""
        theta = np.asarray(theta, dtype=float)
        out = np.zeros(len(theta))
        for b in range(1, len(theta)):
            tc = theta.astype(complex)
            tc[b] += 1j * h
            out[b] = np.imag(self.energy(self.lambdas_from_theta(tc))) / h
        return out
