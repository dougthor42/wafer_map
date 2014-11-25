=========
wafer_map
=========
Plots up a wafer map. Used in semiconductor processing and analysis.
--------------------------------------------------------------------

**Currently in Alpha phase.**

Requires: wxPython

**Usage:**

First, just try and run example.py. This *should* work out of the box and display a wafer map generated from random parameters. The wafer map can be interacted with (to a limited extent right now) with middle-click and scroll wheel.

**Scroll forward:** zoom in, centered on the mouse cursor

**Scrolling backward:** zoom out, centered on the mouse cursor

**Middle-click + drag:** Pan

Data is input into the primary class ``WaferMap`` as a list of ``(x_coord, y_coord, data)`` tuples.


Expected capabilities:

    1. Draw wafer outline and flat or notch.
    2. Draw edge exclusion outline.
    3. Draw wafer center crosshairs.
    4. Accept continuous or discrete data and color accordingly.
    5. Provide zoom and pan capabilities.
    6. Mouse-over to display die coordinate and value

Changelog:

    * 2014-11-25: 0.1.0   First working code. Added example file.
    * 2014-11-25: 0.0.1   Project Creation
