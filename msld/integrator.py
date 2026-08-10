"""
Drives theta (lambda) together with the atoms on top of an OpenMM Context
whose System was built by build_msld_system(). It is a python driver
(not a pure CustomIntegrator) because electrostatics dU/dlambda is only available
by finite difference.

Integrator: one combined VRORV / BAOAB Langevin step over both the atoms and the
theta variables. OpenMM is used only to evaluate forces/energies.

Per force evaluation:
  1. project theta -> lambda (softmax per site), push lambdas to the Context
  2. atom force  = -dU/dx           (OpenMM getForces, at the current lambda)
  3. theta force = -dU/dtheta       (chain rule, dU/dlambda by finite difference)

Limitations: no holonomic constraints (SHAKE), and the finite-difference theta 
force costs O(n_blocks) energy evaluations per step.
Both are removed by the plugin.
"""
from __future__ import annotations

import math

import numpy as np
from openmm import unit

from .builder import set_lambdas
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

    # -----------------------------------------------------------
    # gradients
    # -----------------------------------------------------------
    def dUdlambda(self):
        """Fcomputes dU/dlambda_b for each block by finite difference of the total energy."""
        lam = self.project()
        d = [0.0] * self.model.n_blocks
        present = self.context.getParameters()
        for b in self.dof:
            name = lambda_name(b)
            if name not in present:          # no force uses this lambda -> dU/dlambda = 0
                continue
            base = self.context.getParameter(name)
            self.context.setParameter(name, base + self.h); ep = self.potential_energy()
            self.context.setParameter(name, base - self.h); em = self.potential_energy()
            self.context.setParameter(name, base)
            d[b] = (ep - em) / (2.0 * self.h)
        return d, lam

    def dUdtheta(self):
        """Softmax chain rule: dU/dtheta_i from dU/dlambda (per site)."""
        d, lam = self.dUdlambda()
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
        g = self.dUdtheta()                         # sets lambda, returns dU/dtheta
        fx = np.array(self.context.getState(getForces=True)     # atom forces = −dU/dx, at the current lambda
                      .getForces(asNumpy=True).value_in_unit(_F_UNIT))
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
    # diagnostics
    # -----------------------------------------------------------
    def theta_temperature(self):
        if not self.dof:
            return 0.0
        ke = 0.5 * sum(self.mass[b] * self.vtheta[b] ** 2 for b in self.dof)
        return 2.0 * ke / (len(self.dof) * KB)
