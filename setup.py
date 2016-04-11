# -*- coding: utf-8 -*-

#from distutils.core import setup
# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
from setuptools import setup, find_packages
import logging

# Third Party

# Package / Application
from wafer_map import (__version__,
                       __project_url__,
                       __project_name__,
                       __long_descr__,
                       )

# turn off logging if we're going to build a distribution
logging.disable(logging.CRITICAL)

setup(
    name=__project_name__,
    packages=find_packages(),
    version=__version__,
    description="Semiconductor Wafer Mapping",
    author="Douglas Thor",
    author_email="doug.thor@gmail.com",
    url=__project_url__,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
#        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
        ],
    requires=["wxPython_Phoenix"],
    long_description=__long_descr__,
    )
