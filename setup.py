# -*- coding: utf-8 -*-

from distutils.core import setup
setup(
    name="wafer_map",
    packages=["wafer_map"],
    version="0.1.0",
    description="Semiconductor Wafer Mapping",
    author="Douglas Thor",
    author_email="doug.thor@gmail.com",
    url="https://github.com/dougthor42/wafer_map",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
        ],
    long_description="""
Plots up a wafer map. Used in semiconductor processing and analysis.

Currently in Planning phase.

Requires: wxPython


Expected capabilities:
    1. Draw wafer outline and flat or notch.
    2. Draw edge exclusion outline.
    3. Draw wafer center crosshairs.
    4. Accept continuous or discrete data and color accordingly.
    5. Provide zoom and pan capabilities.
    6. Mouse-over to display die coordinate and value

Changelog:
    2014-11-25: 0.1.0   First working code. Added example file.
    2014-11-25: 0.0.1   Project Creation
""",
    )
