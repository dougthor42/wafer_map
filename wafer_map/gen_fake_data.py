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


def generate_fake_data_old():
    """
    Generate a fake wafer map, where the die values are the die's
    radius squared.

    Don't look too much into this code here. It's been hacked together
    and I'm not proud of it :-P
    """
    # Generate random wafer attributes
    import random
    die_x = random.uniform(5, 10)
    die_x = 6
    die_y = random.uniform(5, 10)
    die_y = 5
    dia = random.choice([100, 150, 200, 210])
    dia = 50
    die_size = (die_x, die_y)
    edge_excl = random.choice([0, 2.5, 5, 10])
    edge_excl = 5
    flat_excl = random.choice([i for i in [0, 2.5, 5, 10] if i >= edge_excl])
    flat_excl = 5

    xyd = []            # our list of (x_coord, x_coord, data) tuples

    # Create a temp wafer map for testing
    # Note that this assumes the center of the wafer lies in the die streets

    # Determine where our wafer edge is for the flat area
    flat_y = -dia/2     # assume wafer edge at first
    if dia in FLAT_LENGTHS:
        # A flat is defined by SEMI M1-0302, so we calcualte where it is
        flat_y = -math.sqrt((dia/2)**2 - (FLAT_LENGTHS[dia] * 0.5)**2)

    nX = int(math.ceil(dia/die_x))
    nY = int(math.ceil(dia/die_y))
    centers = []
    for i in xrange(nX):
        for j in xrange(nY):
            # die center coordinates, assume even-even (wafer center lands on streets)
            x_coord = (i - nX//2) * die_x + 0.5 * die_x
            y_coord = (j - nY//2) * die_y + 0.5 * die_y
            max_dist = max_dist_sqrd((x_coord, y_coord), (die_size))

            # if we're out of excl. zone, don't add the die
            excl_sq = (dia/2)**2 + (edge_excl**2) - (dia * edge_excl)
#            if max_dist > (dia/2)**2 or y_coord - die_y/2 < flat_y:
            if max_dist > excl_sq or y_coord < (flat_y + flat_excl):
                continue
            else:
                r_squared = (x_coord**2 + y_coord**2)
                # wxPython and FloatCanvas use lower-left corner as
                # rectangle origin so we need to adjust
                xyd.append((x_coord - die_x / 2,
                            y_coord - die_y / 2,
                            r_squared))
                centers.append((x_coord - die_x/2, y_coord - die_y/2))

    # Set comprehensions to generate individual lists of coords.
    # this might have an issue with floating point numbers, but I haven't
    # seen any issues yet.
    xCoords = {i[0] for i in centers}
    yCoords = {i[1] for i in centers}

    # Convert die center coodinates to die center row/column coordinates
    grid_x_list = range(1, len(xCoords) + 1)
    grid_y_list = range(1, len(yCoords) + 1)
    grid_y_list.reverse()
    grid_xy = []
    for c in grid_x_list:
        for r in grid_y_list:
            grid_xy.append((c, r))

    die_list = []
    i = 0
    for coord in centers:
        die_list.append((grid_xy[i][0], grid_xy[i][1],
                         coord[0], coord[1],
                         xyd[i][2]))
        i += 1

    print("Number of Die Plotted: {}".format(len(xyd)))

    # add 0.5 to each because DieLoc origin is center of die, while DieCoord
    # is lower-left corner.
    center_xy = (nX/2 + 0.5, nY/2 + 0.5)
    print("Calculated center_xy = {}".format(center_xy))
    center_xy = (5.5, 5.5)
    print("Using center_xy = {}".format(center_xy))

    # put all the wafer info into the WaferInfo class.
    wafer_info = wm_info.WaferInfo(die_size,      # Die Size in (X, Y)
                                   center_xy,     # Center Coord (X, Y)
                                   dia,           # Wafer Diameter
                                   edge_excl,     # Edge Exclusion
                                   flat_excl,     # Flat Exclusion
                                   )
    print(wafer_info)

    return (wafer_info, die_list)


def generate_fake_data():
    """
    """
    # Generate random wafer attributes
    import random
    die_x = random.uniform(5, 10)
    die_x = 6
    die_y = random.uniform(5, 10)
    die_y = 5
    dia = random.choice([100, 150, 200, 210])
    dia = 50
    die_size = (die_x, die_y)
    edge_excl = random.choice([0, 2.5, 5, 10])
    edge_excl = 5
    flat_excl = random.choice([i for i in [0, 2.5, 5, 10] if i >= edge_excl])
    flat_excl = 5

    origin = (0, 0)
    die_x, die_y = die_size
#    die_y = die_size[1]
    rad = dia/2

    # assume that the die lower-left corner is the wafer center
    dieCenter = list(origin)

    # even-even
    # offset the dieCenter by 1/2 the die size, X direction
    dieCenter[0] = 0.5 * die_x
    # offset the dieCenter by 1/2 the die size, Y direction
    dieCenter[1] = 0.5 * die_y

    # find out how many die we can fit on the wafer
    nX = int(math.ceil(dia/die_x))
    nY = int(math.ceil(dia/die_y))

    # make a list of (x, y) die center coordinate pairs
    # This could be switched so that we go across rows first, but i don't care.
    centers = []
    for i in xrange(nX):
        for j in xrange(nY):
            # Note, floor division is intentional
            centers.append(((i-nX//2) * die_x + dieCenter[0],
                            (j-nY//2) * die_y + dieCenter[1]))
            # if I don't "from __future__ import division"
#            centers.append(((i-nX/2) * die_x + dieCenter[0],
#                            (j-nY/2) * die_y + dieCenter[1]))
            # Note that "i-nX * 0.5" does NOT work

    if dia in FLAT_LENGTHS:
        # A flat is defined, so we draw it.
        flatSize = FLAT_LENGTHS[dia]
        x = flatSize * 0.5
        y = -math.sqrt(rad**2 - x**2)
    else:
        # A flat is not defined so...
        y = -rad

    yExcl = y + flat_excl

    # Set comprehensions to generate individual lists of coords.
    # this might have an issue with floating point numbers, but I haven't
    # seen any issues yet.
    xCoords = {i[0] for i in centers}
    yCoords = {i[1] for i in centers}

    # Convert die center coodinates to die center row/column coordinates
    colCoords = range(1, len(xCoords) + 1)
    rowCoords = range(1, len(yCoords) + 1)
    rowCoords.reverse()
    cr = []
    for c in colCoords:
        for r in rowCoords:
            cr.append((c, r))

    # Take only those that are within the wafer radius
    die_list = []
    i = 0
    for coord in centers:
        max_dist = max_dist_sqrd(coord, die_size)
        if max_dist > rad**2:
            # it's off the wafer
            status = "wafer"
        elif coord[1] - die_y/2 < y:
            # it's off the flat
            status = "flat"
        elif max_dist > (rad - edge_excl)**2:
            # it's outside of the exclusion
            status = "excl"
        elif coord[1] - die_y/2 < yExcl:
            # it's ouside the flat exclusion
            status = "flatExcl"
        else:
            # it's a good die, add it to the list
            status = "probe"
        rad_sqrd = (coord[0] + die_size[0]/2)**2 + (coord[1] + die_size[1]/2)**2

#        if max_dist > excl_sq or coord[1] - die_size[1]/2 < (flat_y + flat_excl):
#            continue
#        else:
        die_list.append((cr[i][0], cr[i][1], coord[0], coord[1], rad_sqrd))
        i += 1

    # add 0.5 to each because DieLoc origin is center of die, while DieCoord
    # is lower-left corner.
    center_xy = (nX/2 + 0.5, nY/2 + 0.5)
    print("Calculated center_xy = {}".format(center_xy))
    center_xy = (5.5, 5.5)
    print("Using center_xy = {}".format(center_xy))

    # put all the wafer info into the WaferInfo class.
    wafer_info = wm_info.WaferInfo(die_size,      # Die Size in (X, Y)
                                   center_xy,     # Center Coord (X, Y)
                                   dia,           # Wafer Diameter
                                   edge_excl,     # Edge Exclusion
                                   flat_excl,     # Flat Exclusion
                                   )
    print(wafer_info)

    return (wafer_info, die_list)


def main():
    """ Main Code """
    docopt(__doc__, version=__version__)
    wafer, data = generate_fake_data()
    from pprint import pprint
    pprint(data)


if __name__ == "__main__":
    main()
