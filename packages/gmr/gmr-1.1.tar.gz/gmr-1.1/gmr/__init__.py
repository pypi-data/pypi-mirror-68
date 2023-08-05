"""
gmr
===

Gaussian Mixture Models (GMMs) for clustering and regression in Python.
"""

__version__ = "1.1"

from . import gmm, mvn, utils

__all__ = ['gmm', 'mvn', 'utils']

from .mvn import MVN, plot_error_ellipse
from .gmm import GMM, plot_error_ellipses
