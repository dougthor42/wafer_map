# -*- coding: utf-8 -*-
"""
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

<I still need to fill this out in detail.>

The easiest way to use this to to:

0. Import the ``wm_app`` module:

    >>> import wm_app

1.  Set up your data as a list of (grid_x, grid_y, value) tuples:

    >>> data = [(grid_x_1, grid_y_1, data_1),       # 1st die
    ...         (grid_x_2, grid_y_2, data_2),       # 2nd die
    ...         (grid_x_3, grid_y_3, data_3)        # 3rd die and so on
    ...         ]

2.  Call ``wm_app.WaferMapApp``.

    >>> wm_app.WaferMapApp(data,
    ...                    die_size,
    ...                    center_xy,
    ...                    dia,
    ...                    edge_excl,
    ...                    flat_excl)

    The input parameters for WaferMapApp are:

      :die_size:    The die size in (x, y). Units are mm.
      :center_xy:   The grid (x, y) coordinate that represents the physical
                    center of the wafer.
      :dia:         The wafer diameter. Units are in mm.
      :edge_excl:   The exclusion distance measured from the edge of the
                    wafer. Units are in mm.
      :flat_excl:   The exclusion distance measured from the wafer flat.
                    Units are in mm. Cannot be less than ``edge_excl``.

3.  An image should appear. Yay! Play around with it: middle-click+drag to
    pan, scroll wheel to zoom. See "Keyboard Shortcuts and Mouse Usage"
    section.


Example
-------

There is an example file which somewhat demonstrates how to use this package.
At the very least, you can run the example file and see how this wafer
mapping software looks.

Navigate to the wafer_map directory in your python installtion
(``../Lib/site-packages/wafer_map``) and run example.py in your cmd prompt
or terminal:

    ``python example.py``

Example.py generates a fake data set and then displays it in 3 different ways:

1.  As a standalone app. This requires only calling a single function in
    your code.
2.  As a panel added to your own wx.Frame object. This allows you to add
    the wafer map to your own wxPython app.
3.  As a standalone app, but this time plotting discrete (rather
    than continuous) data.


Nomenclature
------------

For the entire project, the following nomenclature is used. This is to avoid
confusion between a die's coordinates on the wafer (floating-point
values representing the absolute postion of a die) and a die's grid location
(integer row-column or x-y values that are sometimes printed on die).

:coordinate:    Floating-point value representing the exact location of
                a die on the wafer. Also sometimes called 'coord'

                The coordinate origin is the center of the wafer and the
                center of the FloatCanvas panel.
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

This package has been released to version 1.0.0. What this means is that it
*should* be usable in an engineering-type environment. I'm starting to use
it heavily myself. It's not very customizable yet, but I don't need that
capability yet. You can see the roadmap at:
``https://github.com/dougthor42/wafer_map/milestones``

There's still a fair amount of code cleanup and refactoring to do, especially
on the wm_legend.py module (as that was made last). So please do judge my
coding style too harshly (though constructive criticism is much appreciated!)

**Requires: wxPython**

Current capabilities:
----------------------

1. Draw wafer outline and flat or notch.
2. Draw edge exclusion outline.
3. Draw wafer center crosshairs.
4. Accept continuous or discrete data and color accordingly.
5. Provide zoom and pan capabilities.
6. Mouse-over to display die coordinate and value
7. Legend Display for both continuous and discrete data


Changelog
=========
* **1.0.11 / 2015-10-28**

  + Implemented #31 - added radius of die and mouse to status bar.

* **1.0.10 / 2015-05-04**

  + Playing around with imports. Trying to make it so that if I'm running
    a file from my development directory, it imports all the development
    modules and if I'm running something else, it imports from the
    released (site-packages) directory.

* **1.0.9 / 2015-05-04**

  + Fixed flicker issue.

* **1.0.8 / 2015-05-04**

  + I messed up on the PyPI release, so I have to release under a new file
    name. Oh well...

* **1.0.7 / 2015-05-04**

  + Minor import refactoring
  + Added some docstrings

* **1.0.6 / 2015-04-01**

  + Refactored wm_core.draw_wafer_outline so that there are fewer branches
  + Added wm_core.calc_flat_coords to reduce code duplication. This function
    calculates the start and end coordinates of a horizontal chord below
    the circle origin whos length spans a given angle. See doctring on
    wm_core.calc_flat_coords for more info.
  + Fixed issue where a flat exclusion of 0 would not work
  + Fixed issue where an exclusion of 0 would prevent the flat exclusion from
    being drawn.

* **1.0.5 / 2015-03-30**

  + Added optional "grid_center" input to gen_fake_data
  + Fixed Issue #28: Updated wm_utils.linear_gradient to act on HSL data
    rather than on RGB data.
  + Updated documentation for items in wm_utils.
  + Added option to plot the die centers as small red dots.
  + Added option to have the wafer map use a constant number of items for
    discrete legend.

* **1.0.4 / 2014-12-29**

  + Changed import statements to not be weird.

* **1.0.3 / 2014-12-17**

  + Fixed Issue #9: Users can now change the high and low colors for
    continuous data by passing in arguements or by using the app menu:
    ``Options --> Set High Color`` or ``Set Low Color``
  + Fixed Issue #26
  + Fixed Issue #25: Continuous data now generates colors from a single
    algorithm.
  + Fixed Issue #14: Discrete Data now uses an acceptable algorithm for
    determining colors.
  + Fixed Issue #16: The plot now zooms to fit upon first draw. However,
    this created issue #21.
  + Started to add unit tests
  + Updated fake data generator to accept parameter inputs. Any missing
    parameter is randomly generated.
  + The legend for continuous data now fills the entire available vertical
    area.
  + Added a color for invalid data points such as NaN or Inf.
  + Plot range can now be set manually. If it's not set, then it uses the
    2nd and 98th percentiles.
  + Added yellow circle representing the wafer as if the flat did not exist.
  + Created wm_constants.py to contain various default values such as colors.
  + Some other changes that I can't remember and foolishly didn't write
    down.


* **1.0.0 / 2014-12-05**

  + Official release.
  + The Legend should now work as intended.

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
"""

### Constants ###############################################################
__version__ = "1.0.12"
__project_url__ = "https://github.com/dougthor42/wafer_map"
__project_name__ = "wafer_map"
__description__ = "Semiconductor Wafer Mapping"
__long_descr__ = __doc__
#__all__ = ['wm_app', 'wm_constants', 'wm_core', 'wm_frame', 'wm_info',
#           'wm_legend', 'wm_utils']
