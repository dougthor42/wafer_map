# -*- coding: utf-8 -*-

#from distutils.core import setup
# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
import os
from setuptools import setup, find_packages
import sys

# Third Party

# Package / Application

# Read the "__about__.py" file.
# This is how the `cryptography` package does it. Seems like a decent
# way because it prevents the main package from being imported.
# I'm not sure how I feel about `exec()` though...
about = {}
base_dir = os.path.dirname(__file__)
sys.path.insert(0, base_dir)
with open(os.path.join(base_dir, "wafer_map", "__about__.py")) as f:
    exec(f.read(), about)

with open(os.path.join(base_dir, "README.md")) as f:
    long_description = f.read()


classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Manufacturing",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Information Analysis",
    "Topic :: Scientific/Engineering :: Visualization",
]

setup(
    name=about["__package_name__"],
    version=about["__version__"],

    description=about["__description__"],
    long_description_content_type="text/markdown",
    long_description=long_description,
    url=about["__project_url__"],

    author=about["__author__"],
    license=about["__license__"],

    packages=find_packages(),
    classifiers=classifiers,

    install_requires=["wxPython>=4.0.0", "numpy>=1.12.1", "colour>=0.1.4"],
    )
