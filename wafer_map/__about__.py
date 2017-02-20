# -*- coding: utf-8 -*-
"""
Plots up a wafer map. Used in semiconductor processing and analysis.

Please see README.md and CHANGELOG.md at
https://github.com/dougthor42/wafer_map

"""

import os

__all__ = (
    "__author__",
    "__email__",
    "__license__",
    "__version__",
    "__released__",
    "__created__",
    "__project_name__",
    "__project_url__",
    "__package_name__",
    "__description__",
    "__long_descr__",
)


__author__ = "Douglas Thor"
__email__ = "doug.thor@gmail.com"

__license__ = "GNU General Public License v3 (GPLv3)"
__version__ = "1.0.21"
__released__ = "2017-02-20"
__created__ = "2014-11-25"

__project_name__ = "Wafer Map"
__project_url__ = "https://github.com/dougthor42/wafer_map"
__package_name__ = "wafer_map"

__description__ = "Semiconductor Wafer Mapping"
__long_descr__ = __doc__

# Try to read the README file and use that as our long description.
try:
    base_dir = os.path.dirname(__file__)
    with open(os.path.join(base_dir, os.pardir, "README.md")) as f:
        __long_descr__ = f.read()
except Exception:
    pass
