# -*- coding: utf-8 -*-

from distutils.core import setup
setup(
    name="wafer_map",
    packages=["wafer_map"],
    version="0.3.0",
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
    requires=["wxPython"],
    long_description="""
wafer_map.py

Plots up a wafer map. Used in semiconductor processing and analysis.


**Currently in Alpha phase.**

Requires: wxPython

**Usage:**

First, just try and run example.py. This *should* work out of the box and
display a wafer map generated from random parameters. The wafer map
can be interacted with (to a limited extent right now) with middle-click
and scroll wheel.

**Scroll forward:** zoom in, centered on the mouse cursor

**Scroll backward:** zoom out, centered on the mouse cursor

**Middle-click + drag:** Pan

**Left-click + drag:** Not yet implemented (probably zoom-to-box)

**Right-click + drag:** Not yet implemented

Data is input into the primary class ``WaferMap`` as a list
of ``(x_coord, y_coord, data)`` tuples.


Expected capabilities:

1. Draw wafer outline and flat or notch.
2. Draw edge exclusion outline.
3. Draw wafer center crosshairs.
4. Accept continuous or discrete data and color accordingly.
5. Provide zoom and pan capabilities.
6. Mouse-over to display die coordinate and value

Changelog:

* 2014-12-01: 0.3.0   Added kb shortcuts and menu items for display toggle
                      of wafer outline and crosshairs. Added placeholder
                      for legend and kb shortcut for display toggle.
                      Added option for plotting discrete data.
* 2014-11-26: 0.2.0   Made it so a wafer map can be plotted with a single
                      command. Updated example.py to demo this.
* 2014-11-25: 0.1.0   First working code. Added example file.
* 2014-11-25: 0.0.1   Project Creation
""",
    )
