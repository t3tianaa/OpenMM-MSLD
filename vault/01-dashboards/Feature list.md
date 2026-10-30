---
title: Feature list
type: dashboard
status: active
updated: 2026-09-27
---
# Feature list

```dataview
TABLE title, status, milestone, implements
FROM "60-work/features"
WHERE type = "feature"
SORT id ASC
```

## Static index (generated)
<!-- BEGIN GENERATED -->
| feature | title | status | milestone | implements | open issues |
|---|---|---|---|---|---|
| [[FEAT-001 MSLD data model\|FEAT-001]] | MSLD data model | done | M1 | [[REQ-001 Represent sites, blocks and environment\|REQ-001]], [[REQ-002 Lambda from theta with implicit constraints\|REQ-002]] | [[ISS-019 Fixed-block lambda semantics differ from BLaDE\|ISS-019]] |
| [[FEAT-002 Bonded term scaling\|FEAT-002]] | Bonded term scaling | done | M1 | [[REQ-003 Scale bonded terms by block lambdas\|REQ-003]], [[REQ-004 Configurable bonded scaling per term type\|REQ-004]], [[REQ-023 Lambda one reproduces the base system\|REQ-023]] | [[ISS-014 Bonded scaling defaults differ from BLaDE\|ISS-014]], [[ISS-023 Restrained-atom bonded scaling rule missing\|ISS-023]], [[ISS-015 Cross-site 1-4 and CMAP are refused\|ISS-015]] |
| [[FEAT-003 Electrostatics scaling\|FEAT-003]] | Electrostatics scaling | needs-rework | M1 | [[REQ-005 Nonbonded pair scaling rules\|REQ-005]], [[REQ-006 Same-site pairs never interact\|REQ-006]], [[REQ-007 PME electrostatics at partial lambda\|REQ-007]], [[REQ-025 Supported nonbonded methods are correct\|REQ-025]] | [[ISS-003 Within-block correction wrong for cutoff methods\|ISS-003]], [[ISS-006 Same-site PME differs from BLaDE and docs are backwards\|ISS-006]], [[ISS-008 PME alpha recomputed from the tolerance\|ISS-008]], [[ISS-010 Finite-difference dU-dlambda noisy in single precision\|ISS-010]] |
| [[FEAT-004 Lennard-Jones scaling\|FEAT-004]] | Lennard-Jones scaling | needs-rework | M1 | [[REQ-005 Nonbonded pair scaling rules\|REQ-005]], [[REQ-008 LJ scaling including NBFIX\|REQ-008]], [[REQ-024 Dispersion correction preserved\|REQ-024]] | [[ISS-004 CHARMM NBFIX systems fail on CPU\|ISS-004]], [[ISS-007 Dispersion correction removed for the whole system\|ISS-007]] |
| [[FEAT-005 1-4 exception scaling\|FEAT-005]] | 1-4 exception scaling | done | M1 | [[REQ-009 1-4 pair scaling\|REQ-009]] | [[ISS-015 Cross-site 1-4 and CMAP are refused\|ISS-015]] |
| [[FEAT-006 Lambda biases\|FEAT-006]] | Lambda biases | done | M2 | [[REQ-012 Fixed and variable lambda biases\|REQ-012]] | [[ISS-010 Finite-difference dU-dlambda noisy in single precision\|ISS-010]] |
| [[FEAT-007 Atom restraints\|FEAT-007]] | Atom restraints | needs-rework | M4 | [[REQ-014 Atom restraints between substituents\|REQ-014]] | [[ISS-001 Atom restraint groups have the wrong meaning\|ISS-001]], [[ISS-023 Restrained-atom bonded scaling rule missing\|ISS-023]] |
| [[FEAT-008 Lambda-dynamics integrator\|FEAT-008]] | Lambda-dynamics integrator | done | M2 | [[REQ-016 Canonical sampling of atoms and theta\|REQ-016]], [[REQ-017 Per-block theta mass, friction and fixing\|REQ-017]], [[REQ-018 Holonomic constraints and virtual sites\|REQ-018]], [[REQ-002 Lambda from theta with implicit constraints\|REQ-002]] | [[ISS-009 NPT impossible with the Python driver\|ISS-009]], [[ISS-017 Zero-mass particles break the integrator\|ISS-017]], [[ISS-018 Theta runs hot in MDM2\|ISS-018]], [[ISS-019 Fixed-block lambda semantics differ from BLaDE\|ISS-019]], [[ISS-002 Theta mass convention differs from BLaDE\|ISS-002]] |
| [[FEAT-009 Tier-0 analytic dU-dlambda\|FEAT-009]] | Tier-0 analytic dU/dlambda | done | M2 | [[REQ-020 Accurate dU-dlambda for every term\|REQ-020]] | [[ISS-010 Finite-difference dU-dlambda noisy in single precision\|ISS-010]] |
| [[FEAT-010 Multi-platform support\|FEAT-010]] | Multi-platform support | needs-rework | M3 | [[REQ-021 Runs on Reference, CPU, OpenCL, CUDA\|REQ-021]] | [[ISS-004 CHARMM NBFIX systems fail on CPU\|ISS-004]] |
| [[FEAT-011 Trajectory and lambda output\|FEAT-011]] | Trajectory and lambda output | done | M3 | [[REQ-027 Trajectory, lambda and energy output\|REQ-027]] | — |
| [[FEAT-012 ALF flattening heuristic\|FEAT-012]] | ALF flattening heuristic | needs-rework | M6 | [[REQ-030 Adaptive landscape flattening\|REQ-030]], [[REQ-060 Free energy per variant with uncertainty\|REQ-060]] | [[ISS-011 ALF is a heuristic and ddG is single-leg\|ISS-011]] |
| [[FEAT-013 Ingest pipeline\|FEAT-013]] | Ingest pipeline | done | M3 | [[REQ-040 Ingest Amber, CHARMM, PDB and SDF inputs\|REQ-040]] | [[ISS-022 Ingest does not validate geometry\|ISS-022]] |
| [[FEAT-014 CHARMM NBFIX preservation\|FEAT-014]] | CHARMM NBFIX preservation | done | M3 | [[REQ-041 Lossless parameters including NBFIX\|REQ-041]] | [[ISS-025 NBFIX recovery assumes the OpenMM table convention\|ISS-025]] |
| [[FEAT-015 Peptide backbone mapper\|FEAT-015]] | Peptide backbone mapper | done | M3 | [[REQ-042 Map amino-acid mutation sites\|REQ-042]] | — |
| [[FEAT-016 Ligand MCS mapper\|FEAT-016]] | Ligand MCS mapper | done | M3 | [[REQ-043 Map ligand R-group sites\|REQ-043]] | — |
| [[FEAT-017 Hybrid structure grafting\|FEAT-017]] | Hybrid structure grafting | done | M3 | [[REQ-044 Multiple sites per system\|REQ-044]], [[REQ-045 Place variant coordinates in the shared frame\|REQ-045]], [[REQ-048 No bonded term between same-site blocks\|REQ-048]] | [[ISS-024 Core-only bonded terms take reference parameters\|ISS-024]] |
| [[FEAT-018 Charge renormalization\|FEAT-018]] | Charge renormalization | done | M3 | [[REQ-046 Consistent charges across variants\|REQ-046]] | — |
| [[FEAT-019 Solvation and ions\|FEAT-019]] | Solvation and ions | done | M3 | [[REQ-047 Solvate and neutralize consistently\|REQ-047]] | — |
| [[FEAT-020 System build and bundle outputs\|FEAT-020]] | System build and bundle outputs | done | M3 | [[REQ-049 Prep hands off a plain System and a model\|REQ-049]], [[REQ-050 Inspectable prep artifacts\|REQ-050]] | — |
| [[FEAT-021 Prep facade\|FEAT-021]] | Prep facade | done | M3 | [[REQ-049 Prep hands off a plain System and a model\|REQ-049]] | — |
| [[FEAT-022 MDM2 test system\|FEAT-022]] | MDM2 test system | done | M3 | [[REQ-040 Ingest Amber, CHARMM, PDB and SDF inputs\|REQ-040]], [[REQ-042 Map amino-acid mutation sites\|REQ-042]], [[REQ-047 Solvate and neutralize consistently\|REQ-047]] | [[ISS-001 Atom restraint groups have the wrong meaning\|ISS-001]], [[ISS-018 Theta runs hot in MDM2\|ISS-018]], [[ISS-022 Ingest does not validate geometry\|ISS-022]] |
| [[FEAT-023 Minimization at fixed lambda\|FEAT-023]] | Minimization at fixed lambda | done | M3 | [[REQ-026 Energy minimization at fixed lambda\|REQ-026]] | — |
| [[FEAT-030 BLaDE cross-validation harness\|FEAT-030]] | BLaDE cross-validation harness | planned | M5 | [[REQ-070 Agree with BLaDE on a shared CHARMM system\|REQ-070]], [[REQ-052 Import a BLaDE or CHARMM MSLD setup\|REQ-052]] | — |
| [[FEAT-031 Soft-core\|FEAT-031]] | Soft-core | in-progress | M7 | [[REQ-011 Soft-core for alchemical nonbonded\|REQ-011]] | [[ISS-013 Soft-core off while BLaDE examples use it\|ISS-013]] |
| [[FEAT-032 NPT ensemble\|FEAT-032]] | NPT ensemble | planned | M7 | [[REQ-019 NPT ensemble\|REQ-019]] | [[ISS-009 NPT impossible with the Python driver\|ISS-009]] |
| [[FEAT-033 Analytic nonbonded plugin force\|FEAT-033]] | Analytic nonbonded plugin force | planned | M7 | [[REQ-020 Accurate dU-dlambda for every term\|REQ-020]], [[REQ-029 Production performance on GPU\|REQ-029]], [[REQ-007 PME electrostatics at partial lambda\|REQ-007]] | — |
| [[FEAT-034 Fused MSLD integrator plugin\|FEAT-034]] | Fused MSLD integrator plugin | planned | M7 | [[REQ-016 Canonical sampling of atoms and theta\|REQ-016]], [[REQ-019 NPT ensemble\|REQ-019]], [[REQ-029 Production performance on GPU\|REQ-029]] | — |
| [[FEAT-035 Standard ALF\|FEAT-035]] | Standard ALF | planned | M6 | [[REQ-030 Adaptive landscape flattening\|REQ-030]] | [[ISS-011 ALF is a heuristic and ddG is single-leg\|ISS-011]] |
| [[FEAT-036 CMAP scaling\|FEAT-036]] | CMAP scaling | deferred | M8 | [[REQ-010 CMAP scaling\|REQ-010]] | [[ISS-015 Cross-site 1-4 and CMAP are refused\|ISS-015]] |
| [[FEAT-037 Charge-changing perturbations\|FEAT-037]] | Charge-changing perturbations | deferred | M8 | [[REQ-015 Charge-changing perturbations\|REQ-015]] | — |
| [[FEAT-038 Theta biases\|FEAT-038]] | Theta biases | deferred | M6 | [[REQ-013 Theta biases\|REQ-013]] | [[ISS-016 Theta biases and charge restraints missing\|ISS-016]] |
| [[FEAT-039 Cross-site 1-4 scaling\|FEAT-039]] | Cross-site 1-4 scaling | deferred | M8 | [[REQ-009 1-4 pair scaling\|REQ-009]] | [[ISS-015 Cross-site 1-4 and CMAP are refused\|ISS-015]] |
| [[FEAT-040 Free-energy analysis subsystem\|FEAT-040]] | Free-energy analysis subsystem | planned | M6 | [[REQ-060 Free energy per variant with uncertainty\|REQ-060]], [[REQ-061 Relative ddG from two legs\|REQ-061]], [[REQ-062 Sampling and convergence diagnostics\|REQ-062]], [[REQ-063 Combinatorial multi-site free energies\|REQ-063]] | — |
| [[FEAT-041 Amber validation vs FEP or TI\|FEAT-041]] | Amber validation vs FEP or TI | planned | M8 | [[REQ-071 Agree with FEP or TI on Amber\|REQ-071]] | — |
| [[FEAT-042 Additional ingest routes\|FEAT-042]] | Additional ingest routes | deferred | M8 | [[REQ-040 Ingest Amber, CHARMM, PDB and SDF inputs\|REQ-040]] | — |
| [[FEAT-043 Input geometry validation\|FEAT-043]] | Input geometry validation | planned | M4 | [[REQ-051 Validate input geometry\|REQ-051]] | [[ISS-022 Ingest does not validate geometry\|ISS-022]] |
| [[FEAT-044 Knowledge vault and process\|FEAT-044]] | Knowledge vault and process | done | M4 | [[REQ-073 Documentation and traceability\|REQ-073]] | — |
| [[FEAT-045 Independent partial-lambda oracle tests\|FEAT-045]] | Independent partial-lambda oracle tests | planned | M4 | [[REQ-072 Every feature has an automated test\|REQ-072]], [[REQ-070 Agree with BLaDE on a shared CHARMM system\|REQ-070]] | [[ISS-012 No validation at partial lambda\|ISS-012]] |
| [[FEAT-046 Checkpoint and restart\|FEAT-046]] | Checkpoint and restart | planned | M6 | [[REQ-028 Checkpoint and restart\|REQ-028]] | — |
| [[FEAT-047 Engine hardening\|FEAT-047]] | Engine hardening | planned | M4 | [[REQ-022 Refuse unsupported input loudly\|REQ-022]], [[REQ-024 Dispersion correction preserved\|REQ-024]], [[REQ-025 Supported nonbonded methods are correct\|REQ-025]], [[REQ-018 Holonomic constraints and virtual sites\|REQ-018]] | [[ISS-003 Within-block correction wrong for cutoff methods\|ISS-003]], [[ISS-004 CHARMM NBFIX systems fail on CPU\|ISS-004]], [[ISS-005 Unsupported force types silently unscaled\|ISS-005]], [[ISS-007 Dispersion correction removed for the whole system\|ISS-007]], [[ISS-008 PME alpha recomputed from the tolerance\|ISS-008]], [[ISS-017 Zero-mass particles break the integrator\|ISS-017]] |
<!-- END GENERATED -->
