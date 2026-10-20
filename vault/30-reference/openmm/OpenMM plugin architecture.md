---
title: OpenMM plugin architecture
type: reference
status: draft
system: openmm
version: 8.5.2
related: ["[[Production plugin architecture]]", "[[ADR-0027 Plugin technology choices|ADR-0027]]"]
updated: 2026-09-27
---
# OpenMM plugin architecture

How to add a new `Force` or `Integrator` to OpenMM without modifying OpenMM itself (template:
github.com/openmm/openmmexampleplugin).

```
 openmmapi/      public API class (MyForce : Force) + MyForceImpl (ForceImpl) — platform independent
 platforms/
   reference/    ReferenceCalcMyForceKernel — plain C++, double precision
   common/       CommonCalcMyForceKernel — ONE kernel source for OpenCL + CUDA + HIP
   (opencl/, cuda/  thin registration layers)
 serialization/  XML proxy so Systems with the force can be saved/loaded
 python/         SWIG wrapper
```

- Kernels are registered per platform through a `KernelFactory`; the API class creates a
  `ForceImpl` that asks the platform for its kernel by name.
- The `common/` compute layer (`ComputeContext`, `ComputeKernel`, `ComputeArray`) lets one source
  compile for OpenCL and CUDA — present in the installed headers (`include/openmm/common`,
  verified 2026-09-23).
- A C++ program linking `libOpenMM` compiles and runs in the `msld` env (verified 2026-09-23);
  `swig` is not installed yet.
- Existing plugins worth reading as templates: `openmm/plugins/rpmd` (custom integrator),
  `openmm/plugins/drude` (custom force + integrator), `openmm/plugins/amoeba`.

Status: **draft** — the kernel APIs (how to access neighbour lists, PME grids, how to accumulate an
extra per-block energy derivative in fixed point) still need to be read before S1/S2
([[TASK-075 Study OpenMM nonbonded kernels for the plugin|TASK-075]]).
