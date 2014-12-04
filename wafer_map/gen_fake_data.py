# -*- coding: utf-8 -*-
"""
@name:          new_program.py
@vers:          0.1.0
@author:        dthor
@created:       Tue Dec 02 10:33:58 2014
@descr:         A new file

Usage:
    new_program.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.
"""

from __future__ import print_function, division, absolute_import
#from __future__ import unicode_literals
from docopt import docopt
import math

# check to see if we can import local, otherwise import absolute
print(__file__)
if 'site-packages' in __file__:
    print("we're being run from site-pkg")
    from wafer_map import wm_info
else:
    print("running in dev mode")
    import wm_info


__author__ = "Douglas Thor"
__version__ = "v0.1.0"


# Library Constants
# Defined by SEMI M1-0302
FLAT_LENGTHS = {50: 15.88, 75: 22.22, 100: 32.5, 125: 42.5, 150: 57.5}


def max_dist_sqrd(center, size):
    """
    Calcualtes the largest distance from the origin for a rectangle of
    size (x, y), where the center of the rectangle's coordinates are known.
    If the rectangle's center is in the Q1, then the upper-right corner is
    the farthest away from the origin. If in Q2, then the upper-left corner
    is farthest away. Etc.
    Returns the magnitude of the largest distance squared.
    Does not include the Sqrt function for sake of speed.
    """
    half_x = size[0]/2.
    half_y = size[1]/2.
    if center[0] < 0:
        half_x = -half_x
    if center[1] < 0:
        half_y = -half_y
    dist = (center[0] + half_x)**2 + (center[1] + half_y)**2
    return dist


def generate_fake_data():
    """
    Another rewrite, this time starting from the top. We will not look at
    the wafer map until I'm satisfied with the numerical values.

    - Things to keep in mind:
    - grid coords fall on die centers
    - die are drawn from the lower-left corner
    - center of the wafer is coord (0, 0)
    - the center of the wafer is mapped to a
      floating-precision (grid_x, grid_y tuple)

    What wm_core needs is:

    - list of (grid_x, grid_y, plot_value) tuples
    - die_size (x, y) tuple
    - grid_center (grid_x, grid_y) tuple. Without this, we can't plot the
      wafer outline

    Here's the game plan:

    1. Generate a square grid of "die" that is guarenteed to cover the
       entire wafer.
    2. Choose an arbitrary center point ``grid_center``.
    3. Calculate the max_dist of each die based on grid_center.
    4. Remove any die that cross the exclusion boundary
    5. Calculate the lower-left coordinate of each of those die
    6. Complete.
    """
    # Generate random wafer attributes
    import random
    die_x = random.uniform(5, 10)
    die_y = random.uniform(5, 10)
    dia = random.choice([100, 150, 200, 210])
    die_size = (die_x, die_y)
    edge_excl = random.choice([0, 2.5, 5, 10])
    flat_excl = random.choice([i for i in [0, 2.5, 5, 10] if i >= edge_excl])

    # Determine where our wafer edge is for the flat area
    flat_y = -dia/2     # assume wafer edge at first
    if dia in FLAT_LENGTHS:
        # A flat is defined by SEMI M1-0302, so we calcualte where it is
        flat_y = -math.sqrt((dia/2)**2 - (FLAT_LENGTHS[dia] * 0.5)**2)

    # calculate the exclusion radius^2
    excl_sqrd = (dia/2)**2 + (edge_excl**2) - (dia * edge_excl)

    # 1. Generate square grid guarenteed to cover entire wafer
    #    We'll use 2x the wafer dia so that we can move center around a bit
    grid_max_x = 2 * int(math.ceil(dia / die_x))
    grid_max_y = 2 * int(math.ceil(dia / die_y))

    # 2. Choose arbitraty center point
    x_offset = random.choice([0, 0.5, -2, 0.24])
    y_offset = random.choice([0, 0.5, -2, 0.24])
    grid_center = (grid_max_x/2 + x_offset, grid_max_y/2 + y_offset)

    # This could be more efficient
    grid_points = []
    for _x in xrange(1, grid_max_x):
        for _y in xrange(1, grid_max_y):
            coord_die_center_x = die_x * (_x - grid_center[0])
            # we have to reverse the y coord, hence why it's
            # ``grid_center[1] - _y`` and not ``_y - grid_center[1]``
            coord_die_center_y = die_y * (grid_center[1] - _y)
            coord_die_center = (coord_die_center_x, coord_die_center_y)
            center_rad_sqrd = coord_die_center_x**2 + coord_die_center_y**2
            die_max_sqrd = max_dist_sqrd(coord_die_center, die_size)
#            coord_lower_left_x = coord_die_center_x - die_x/2
            coord_lower_left_y = coord_die_center_y - die_y/2
#            coord_lower_left = (coord_lower_left_x, coord_lower_left_y)
            if (die_max_sqrd > excl_sqrd
                    or coord_lower_left_y < (flat_y + flat_excl)):
                continue
            else:
                grid_points.append((_x,
                                    _y,
                                    center_rad_sqrd,
                                    # these items are for debug.
#                                    coord_lower_left,
#                                    center_rad_sqrd,
#                                    coord_die_center,
#                                    die_max_sqrd,
                                    ))

    print("\nPlotting {} die.".format(len(grid_points)))

    # put all the wafer info into the WaferInfo class.
    wafer_info = wm_info.WaferInfo(die_size,      # Die Size in (X, Y)
                                   grid_center,   # Center Coord (X, Y)
                                   dia,           # Wafer Diameter
                                   edge_excl,     # Edge Exclusion
                                   flat_excl,     # Flat Exclusion
                                   )
    print(wafer_info)

    return (wafer_info, grid_points)


def main():
    """ Main Code """
    docopt(__doc__, version=__version__)
    wafer, data = generate_fake_data()
    from pprint import pprint
    pprint(data)

#    print()
#    pprint([_i for _i in data if _i[0] in (17, 18, 19)])


if __name__ == "__main__":
    main()
