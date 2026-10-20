"""
Drives theta (lambda) together with the atoms on top of an OpenMM Context
whose System was built by scale_msld_system(). It is a python driver
(not a pure CustomIntegrator) because the NonbondedForce electrostatics
dU/dlambda is only available by finite difference.

Integrator: one combined VRORV / BAOAB Langevin step over both the atoms and the
theta variables. OpenMM is used only to evaluate forces/energies.

Per force evaluation:
  1. project theta -> lambda (softmax per site), push lambdas to the Context
  2. atom force  = -dU/dx           (OpenMM getForces, at the current lambda)
  3. theta force = -dU/dtheta       (chain rule from dU/dlambda)

dU/dlambda is a hybrid: bonded + LJ + within-block correction come back analytically
(addEnergyParameterDerivative, one getState merged with the atom forces); the
remainder -- electrostatics (which OpenMM cannot expose), the biases, and anything
injected -- is finite-differenced over the FD_FORCE_GROUP energy alone. builder.py
splits the forces into those two groups.

Limitations: no holonomic constraints (SHAKE), and the remainder finite difference
still costs O(n_blocks) group-energy evaluations per step (electrostatics dominates).
Both are removed by the plugin (analytic PME charge-derivative).
"""
from __future__ import annotations

import math

import numpy as np
from openmm import unit

from .builder import set_lambdas, FD_FORCE_GROUP
from .forces import lambda_name

_NM = unit.nanometer
_KJ = unit.kilojoule_per_mole
_F_UNIT = _KJ / _NM
_VEL = _NM / unit.picosecond
KB = 0.00831446261815324          # kJ/mol/K


class LambdaDynamics:
    """Owns theta + atom state; integrates both with combined VRORV Langevin."""

    def __init__(self, context, model, temperature=300.0, timestep=0.001,
                 atom_friction=1.0, fd_step=1e-4, seed=None):
        self.context = context
        self.model = model
        self.kT = KB * temperature
        self.dt = timestep                       # ps
        self.h = fd_step                         # FD step in lambda
        self.rng = np.random.default_rng(seed)

        system = context.getSystem()
        self.n_atoms = system.getNumParticles()
        #  per atom masses 
        self.mass_x = np.array([system.getParticleMass(i).value_in_unit(unit.dalton)
                                for i in range(self.n_atoms)])

        # theta state (per block, block 0 = env, never moves)
        self.theta = [bl.theta0 for bl in model.blocks]
        self.vtheta = [bl.theta_velocity0 for bl in model.blocks]
        self.mass = [bl.theta_mass for bl in model.blocks]
        self.dof = [b for b in range(1, model.n_blocks) if not model.blocks[b].fixed]

        # atom state (positions from the Context, velocities from Maxwell-Boltzmann)
        st = context.getState(getPositions=True)
        self.x = np.array(st.getPositions(asNumpy=True).value_in_unit(_NM))
        self.vx = (self.rng.standard_normal((self.n_atoms, 3))
                   * np.sqrt(self.kT / self.mass_x)[:, None])
        for b in self.dof:
            self.vtheta[b] = self.rng.standard_normal() * math.sqrt(self.kT / self.mass[b])

        # VRORV Langevin coefficients (a = exp(-gamma dt), noise = sqrt((1-a^2) kT/m))
        dt = self.dt
        ax = math.exp(-atom_friction * dt)
        self.ax = ax
        self.bx = math.sqrt((1 - ax * ax) * self.kT) / np.sqrt(self.mass_x)   # (N,)
        self.ath, self.bth = {}, {}
        for b in self.dof:
            g = model.blocks[b].theta_friction
            a = math.exp(-g * dt)
            self.ath[b] = a
            self.bth[b] = math.sqrt((1 - a * a) * self.kT / self.mass[b])

        # holonomic constraints (SHAKE/RATTLE) on atoms, if the System has any
        self.has_constraints = system.getNumConstraints() > 0
        self.constraint_tol = 1e-6

        # dU/dlambda = analytic part (bonded + LJ + within-block correction, via
        # addEnergyParameterDerivative) + a finite difference of the FD_FORCE_GROUP remainder
        # (electrostatics + biases + anything injected). scale_msld_system put the analytic
        # forces in ANALYTIC_FORCE_GROUP and left this remainder in group 0. If group 0 is
        # empty (everything analytic), the FD is skipped.
        self._fd_group = FD_FORCE_GROUP
        self._has_fd = any(system.getForce(i).getForceGroup() == FD_FORCE_GROUP
                           for i in range(system.getNumForces()))

        self._F = None
        self.project()

    # -----------------------------------------------------------
    # lambda
    # -----------------------------------------------------------
    def project(self):
        """Project theta -> lambda, push to the Context."""
        lam = self.model.lambda_from_theta(self.theta)
        set_lambdas(self.context, lam)
        return lam

    def get_lambdas(self):
        return self.model.lambda_from_theta(self.theta)

    def potential_energy(self):
        return self.context.getState(getEnergy=True).getPotentialEnergy().value_in_unit(_KJ)

    def _fd_energy(self):
        """Energy of ONLY the finite-difference force group (electrostatics + biases + injected)."""
        return (self.context.getState(getEnergy=True, groups={self._fd_group})
                .getPotentialEnergy().value_in_unit(_KJ))

    # -----------------------------------------------------------
    # minimization
    # -----------------------------------------------------------
    def minimize(self, max_iterations=0, tolerance=10.0):
        """Energy-minimize the ATOMS at the current lambda, then reload the relaxed positions.

        Freshly grafted / freshly solvated hybrids start with steric clashes (alternate side
        chains placed by backbone alignment, new water). Running dynamics straight from that state
        blows up on step 1, so relax the geometry first.

        Only the atomic coordinates move: theta (and thus lambda) are held fixed at the current
        projection while OpenMM's LocalEnergyMinimizer runs on the *lambda-scaled* energy surface.
        This MUST be called after the System has been lambda-scaled (scale_system adds the same-site
        block exclusions); minimizing the unscaled System would let the mutually-exclusive variant
        side chains -- which deliberately overlap in space -- clash. `tolerance` is kJ/mol/nm;
        `max_iterations=0` runs to convergence. Returns self.
        """
        from openmm import LocalEnergyMinimizer
        self.project()                                  # push current lambda to the Context
        self.context.setPositions(self.x * _NM)
        LocalEnergyMinimizer.minimize(self.context, tolerance * _F_UNIT, max_iterations)
        self.x = np.array(self.context.getState(getPositions=True)
                          .getPositions(asNumpy=True).value_in_unit(_NM))
        self._F = None                                  # cached force is stale -> recompute
        return self

    # -----------------------------------------------------------
    # gradients
    # -----------------------------------------------------------
    def dUdlambda(self, analytic_deriv=None):
        """dU/dlambda_b for each block.

        Analytic part (bonded + LJ + within-block correction) comes straight from OpenMM's
        addEnergyParameterDerivative; the remainder -- electrostatics (charge offsets + PME
        reciprocal + 1-4 offsets, which OpenMM cannot expose), the biases, and anything a caller
        injected -- is a central finite difference of the FD_FORCE_GROUP energy ALONE.

        `analytic_deriv` lets the caller pass a dict of dU/dparam it already fetched alongside
        the atom forces (one merged getState), avoiding a second energy evaluation.
        """
        lam = self.project()
        if analytic_deriv is None:
            analytic_deriv = self.context.getState(
                getParameterDerivatives=True).getEnergyParameterDerivatives()
        d = [0.0] * self.model.n_blocks
        present = self.context.getParameters()
        for b in self.dof:
            name = lambda_name(b)
            if name not in present:          # no force uses this lambda -> dU/dlambda = 0
                continue
            a = analytic_deriv[name] if name in analytic_deriv else 0.0
            e = 0.0
            if self._has_fd:                 # finite-difference the non-analytic remainder only
                base = self.context.getParameter(name)
                self.context.setParameter(name, base + self.h); ep = self._fd_energy()
                self.context.setParameter(name, base - self.h); em = self._fd_energy()
                self.context.setParameter(name, base)
                e = (ep - em) / (2.0 * self.h)
            d[b] = a + e
        return d, lam

    def dUdtheta(self, analytic_deriv=None):
        """Softmax chain rule: dU/dtheta_i from dU/dlambda (per site)."""
        d, lam = self.dUdlambda(analytic_deriv)
        g = [0.0] * self.model.n_blocks
        fnex = self.model.fnex
        for s in range(1, self.model.n_sites):
            js = self.model.blocks_in_site(s)
            wmean = sum(lam[j] * d[j] for j in js)
            for i in js:
                if self.model.blocks[i].fixed:
                    continue
                g[i] = lam[i] * fnex * math.cos(self.theta[i]) * (d[i] - wmean)
        return g

    # -----------------------------------------------------------
    # dynamics
    # -----------------------------------------------------------
    def _forces(self):
        """Physical forces (= -gradient) on atoms and theta at the current state."""
        self.context.setPositions(self.x * _NM)     # sync atom positions into the Context
        self.project()                              # push current lambda to the Context
        # one evaluation gives BOTH the atom forces and the analytic dU/dlambda parts
        st = self.context.getState(getForces=True, getParameterDerivatives=True)
        fx = np.array(st.getForces(asNumpy=True).value_in_unit(_F_UNIT))   # atom forces = −dU/dx
        deriv = st.getEnergyParameterDerivatives()  # analytic dU/dlambda (bonded+LJ+within-block+bias)
        g = self.dUdtheta(deriv)                    # theta force (+ electrostatics-only FD inside)
        fth = {b: -g[b] for b in self.dof}          # theta force = -dU/dtheta
        return fx, fth

    # holonomic constraints on atoms (SHAKE positions, RATTLE velocities) 
    def _drift_x(self, hdt):
        """Half drift of the atoms, with SHAKE if the System has constraints."""
        if not self.has_constraints:
            self.x += hdt * self.vx
            return
        x_pred = self.x + hdt * self.vx
        self.context.setPositions(x_pred * _NM)
        self.context.applyConstraints(self.constraint_tol)          # SHAKE
        x_con = np.array(self.context.getState(getPositions=True)
                         .getPositions(asNumpy=True).value_in_unit(_NM))
        self.vx += (x_con - x_pred) / hdt          # constraint impulse -> velocity
        self.x = x_con

    def _rattle(self):
        """Remove atom-velocity components along the constraints (RATTLE)."""
        self.context.setPositions(self.x * _NM)
        self.context.setVelocities(self.vx * _VEL)
        self.context.applyVelocityConstraints(self.constraint_tol)
        self.vx = np.array(self.context.getState(getVelocities=True)
                           .getVelocities(asNumpy=True).value_in_unit(_VEL))

    def step(self, nsteps=1):
        """Combined VRORV Langevin: B A O A B, over atoms and theta together."""
        hdt = 0.5 * self.dt
        mx = self.mass_x[:, None]
        if self._F is None:
            self._F = self._forces()
        for _ in range(nsteps):
            fx, fth = self._F
            # B (half kick): v += (dt/2)·F/m  (both x and θ)
            self.vx += hdt * fx / mx
            if self.has_constraints:
                self._rattle()
            for b in self.dof:
                self.vtheta[b] += hdt * fth[b] / self.mass[b]
            # A (half drift): q += (dt/2)·v
            self._drift_x(hdt)                       # SHAKE inside if constrained
            for b in self.dof:
                self.theta[b] += hdt * self.vtheta[b]
            # O (friction + noise = thermostat): v  = a·v + b·ξ (epsilon ~ N(0,1))
            self.vx = self.ax * self.vx + self.bx[:, None] * self.rng.standard_normal(self.vx.shape)
            if self.has_constraints:
                self._rattle()
            for b in self.dof:
                self.vtheta[b] = self.ath[b] * self.vtheta[b] + self.bth[b] * self.rng.standard_normal()
            # A (half drift): q += (dt/2)·v
            self._drift_x(hdt)                       # SHAKE inside if constrained
            for b in self.dof:
                self.theta[b] += hdt * self.vtheta[b]
            # force at the new state
            self._F = self._forces()
            fx, fth = self._F
            # B (half kick): v += (dt/2)·F/m 
            self.vx += hdt * fx / mx
            if self.has_constraints:
                self._rattle()
            for b in self.dof:
                self.vtheta[b] += hdt * fth[b] / self.mass[b]
        self.project()

    # -----------------------------------------------------------
    # run with reporters
    # -----------------------------------------------------------
    def run(self, nsteps, *, minimize=False, metrics=None, metrics_every: int = 100, mapping=None,
            trajectory=None, trajectory_every: int = 1000, structure=None, reporters=()):
        """Integrate `nsteps`, saving metrics / a trajectory at their OWN step intervals.

        Just name the outputs and their intervals — the files are opened and closed here, so no
        `with` is needed:

            dyn.run(10_000, minimize=True,
                            metrics="out/metrics.csv", metrics_every=100, mapping=bundle.mapping,
                            trajectory="out/traj.dcd", trajectory_every=500, structure=bundle.structure)

          minimize   : energy-minimize the atoms once before stepping (see `minimize`); True runs to
                       convergence, an int caps the iterations. Do this for any freshly built /
                       solvated hybrid or dynamics will blow up on step 1.
          metrics    : CSV path; every `metrics_every` steps append per-block lambda + energy
                       (`mapping` names the columns; optional).
          trajectory : DCD path; every `trajectory_every` steps append the atom coordinates
                       (needs `structure`, the hybrid Structure, for the topology; also writes a
                       companion `<stem>.pdb`).
          reporters  : extra custom reporters, each with `.every`, `.report(dyn, step)`, `.close()`.

        Every reporter carries its own interval; `run` steps only as finely as needed (the gcd of
        the intervals) and reports each one when the cumulative step is a multiple of its `every`.
        With no outputs this is just `step(nsteps)`. Returns self.
        """
        import math

        if minimize:
            self.minimize(max_iterations=(0 if minimize is True else int(minimize)))

        reps = list(reporters)
        if metrics is not None:
            from .io import LambdaTrajectoryWriter
            reps.append(LambdaTrajectoryWriter(metrics, self.model, every=metrics_every,
                                               mapping=mapping))
        if trajectory is not None:
            if structure is None:
                raise ValueError("trajectory= needs structure= (the hybrid Structure) for its topology")
            from .io import TrajectoryWriter
            reps.append(TrajectoryWriter(trajectory, structure, every=trajectory_every,
                                         mapping=mapping))

        if not reps:
            self.step(nsteps)
            return self

        intervals = [r.every for r in reps if getattr(r, "every", 0)]
        stride = math.gcd(*intervals, nsteps) if intervals else nsteps
        done = 0
        try:
            while done < nsteps:
                chunk = min(stride, nsteps - done)
                self.step(chunk)
                done += chunk
                for r in reps:
                    if getattr(r, "every", 0) and done % r.every == 0:
                        r.report(self, done)
        finally:
            for r in reps:
                close = getattr(r, "close", None)
                if callable(close):
                    close()
        return self

    # -----------------------------------------------------------
    # diagnostics
    # -----------------------------------------------------------
    def theta_temperature(self):
        if not self.dof:
            return 0.0
        ke = 0.5 * sum(self.mass[b] * self.vtheta[b] ** 2 for b in self.dof)
        return 2.0 * ke / (len(self.dof) * KB)
