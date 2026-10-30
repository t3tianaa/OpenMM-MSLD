"""Multi-site lambda-dynamics (MSLD) for OpenMM.

MSLD lets several chemical variants of a molecule live in one simulation and
compete. A coupling variable, lambda, decides how "present" each variant is,
and lambda itself moves during the run, so the system samples which variants
are favorable instead of us running each one separately.

This is a from-scratch implementation on top of stock OpenMM. BLaDE does the
same thing and we keep it only as the reference to check our
numbers against.
"""

__version__ = "0.0.0"

