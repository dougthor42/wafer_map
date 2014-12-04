# -*- coding: utf-8 -*-

from distutils.core import setup
setup(
    name="wafer_map",
    packages=["wafer_map"],
    version="0.6.0",
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
=========
wafer_map
=========

Plots up a wafer map. Used in semiconductor processing and analysis.


Features
========

- Mouse and keyboard shortcuts!
- Knows SEMI M1-0302 wafer sizes!
- Something else!


Installation
============

Install from PyPI.

``pip install wafer_map``


Usage
=====

Since I'm still making the package, the usage will change. Since no
no documentation is better than wrong documentation, I'm leaving this section
mostly barren until I hash things out.

What I can show you is the example.py file. Navigate to the wafer_map
directory in your python installtion (``../Lib/site-packages/wafer_map``) and
run example.py in your cmd prompt or terminal:

    >>> python example.py

Example.py generates a fake data set and then displays it in 3 different ways:

1. As a standalone app. This requires only calling a single function in
   your code.
2. As a panel added to your own wx.Frame object. This allows you to add
   the wafer map to your own wxPython app.
3. As a panel added to your own wx.Frame object, but this time plotting
   discrete (rather than continuous) data.


Nomenclature
------------

For the entire project, the following nomenclature is used. This is to avoid
confusion between a die's coordinates on the wafer (floating-point
values representing the absolute postion of a die) and a die's grid location
(integer row-column or x-y values that are sometimes printed on die).

:coordinate:    Floating-point value representing the exact location of
                a die on the wafer.

                The coordinate origin is the center of the wafer and the
                center of the FloatCanvas panel.
:loc:           Alias for ``coordinate``.
:grid:          Integer value representing the printed die. Can only be mapped
                to a coordinate if a grid_center is defined.

                Each grid line falls on a die's center.
:grid_center:   The ``(float_x, float_y)`` tuple which is coincident with the
                wafer's center coordinate ``(0, 0)``.

                This is the only ``grid`` value that can be made up of floats.
:row:           Alias for ``grid_y``.
:col:           Alias for ``grid_x``.


Keyboard Shortcuts and Mouse Usage
----------------------------------

No matter if you use the standalone app or add the panel to your own wx.Frame
instance, keyboard shortcuts work. I've only added a few so far, but I plan
on adding more.

The panel also supports mouse controls. Middle click will pan, mouse wheel
will zoom in and out.

:Home:  Zoom to full wafer
:O:     Toggle display of wafer and exclusion outline
:C:     Toggle crosshair display
:L:     Toggle legend display


Notes
=====

**Currently in Alpha phase.**

This package is currently undergoing a lot of modification. I'm using this
to learn how to distribute things on PyPI and GitHub, so there will be a
lot of quick updates. Sometimes it won't work. Sometimes I'll break things.
Sometimes I'll completely change the API.

This package is not attempting to modify any files or write any data, so using
it in alpha phase should not cause any computer harm or data loss (unless I
do something stupid).

**Requires: wxPython**

Data is input into the primary class ``WaferMap`` as a list
of ``(x_coord, y_coord, data)`` tuples.

Expected capabilities:
----------------------

1. Draw wafer outline and flat or notch.
2. Draw edge exclusion outline.
3. Draw wafer center crosshairs.
4. Accept continuous or discrete data and color accordingly.
5. Provide zoom and pan capabilities.
6. Mouse-over to display die coordinate and value


Changelog
=========

* **0.6.0 / 2014-12-04**

  + Closed issues #1, 2, 3, 4, and 6 in the tracker.
  + Updated gen_fake_data to use better algorithm and actually output
    correct data.
  + Updated wm_core.WaferMapPanel so that the status bar text displays
    the correct grid values. Verified working with all sorts of
    grid_center values.
  + **Last Update before release, yay!** All that's left is to get the
    legend working.

* **0.5.0 / 2014-12-02**

  + renamed wafer_map.py to wm_core.py.
  + Finally figured out the imports for running in development from my
    own dev directory vs running in "production" from the site-packages
    directory.

* **0.4.0 / 2014-12-02**

  + Massive change to package hierarchy - separated app, frame, info, and fake
    data into individual modules.

* **0.3.0 / 2014-12-01**

  + Added kb shortcuts and menu items for display toggle
    of wafer outline and crosshairs.
  + Added placeholder for legend and kb shortcut for display toggle.
  + Added option for plotting discrete data.

* **0.2.0 / 2014-11-26**

  + Made it so a wafer map can be plotted with a single
    command.
  + Updated example.py to demo single-command usage.

* **0.1.0 / 2014-11-25**

  + First working code. Added example file.

* **0.0.1 / 2014-11-25**

  + Project Creation

""",
    )
