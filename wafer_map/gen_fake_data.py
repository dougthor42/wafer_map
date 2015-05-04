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

from __future__ import print_function, division#, absolute_import
#from __future__ import unicode_literals
import math
import random

import wafer_map.wm_info as wm_info
import wafer_map.wm_utils as wm_utils
import wafer_map.wm_constants as wm_const


def generate_fake_data(**kwargs):
    """
    Generates fake data for wafer_map.

    Keyword Arguments:
    ------------------

    die_x : float
        Die x size in mm
    die_y : float
        Die y size in mm
    dia : float
        Wafer diameter in mm
    edge_excl : float
        Edge exclusion in mm
    flat_excl : float
        Wafer Flat exclusion in mm
    x_offset : float
        The center die's x offset.
        (0-1), where 0.5 means that the center of the
        wafer is located on a vertical street (edge of a die).
    y_offset : float
        The center die's y offset.
        (0-1), where 0.5 means that the center of the
        wafer is located on a horizontal street (edge of a die).
    grid_center : tuple of floats
        The grid coordinates (x_col, y_row) that denote the
        center of the wafer. Defaults to None, which determines
        the center grid coordinates based on the total number of
        rows and columns.
    dtype : string
        Datatype. Valid options are "discrete" and "continuous".
        Defaults to "continuous".

    Examples of Offsets:
    --------------------

    The ``X`` denotes the center of the wafer::

      x_offset = 0          x_offset = 0
      y_offset = 0          y_offset = 0.5
      |-----------|         |-----------|
      |           |         |           |
      |     X     |         |           |
      |           |         |           |
      |-----------|         |-----X-----|

      x_offset = 0.5        x_offset = 0.5
      y_offset = 0          y_offset = 0.5
      |-----------|         |-----------|
      |           |         |           |
      X           |         |           |
      |           |         |           |
      |-----------|         X-----------|

    Notes:
    ------

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
    dia_list = [100, 150, 200, 210]
    excl_list = [0, 2.5, 5, 10]
    offset_list = [0, 0.5, -2, 0.24]
    DEFAULT_KWARGS = {'die_x': random.uniform(5, 10),
                      'die_y': random.uniform(5, 10),
                      'dia': random.choice(dia_list),
                      'edge_excl': random.choice(excl_list),
                      'flat_excl': random.choice(excl_list),
                      'x_offset': random.choice(offset_list),
                      'y_offset': random.choice(offset_list),
                      'grid_center': None,
                      'dtype': 'continuous',
                      }

    # parse the keyword arguements, asigning defaults if not found.
    for key in DEFAULT_KWARGS:
        if key not in kwargs:
            kwargs[key] = DEFAULT_KWARGS[key]

    die_x = kwargs['die_x']
    die_y = kwargs['die_y']
    dia = kwargs['dia']
    edge_excl = kwargs['edge_excl']
    flat_excl = kwargs['flat_excl']
    x_offset = kwargs['x_offset']
    y_offset = kwargs['y_offset']
    grid_center = kwargs['grid_center']
    dtype = kwargs['dtype']

    die_size = (die_x, die_y)

    # Determine where our wafer edge is for the flat area
    flat_y = -dia/2     # assume wafer edge at first
    if dia in wm_const.wm_FLAT_LENGTHS:
        # A flat is defined by SEMI M1-0302, so we calcualte where it is
        flat_y = -math.sqrt((dia/2)**2 - (wm_const.wm_FLAT_LENGTHS[dia] * 0.5)**2)

    # calculate the exclusion radius^2
    excl_sqrd = (dia/2)**2 + (edge_excl**2) - (dia * edge_excl)

    # 1. Generate square grid guarenteed to cover entire wafer
    #    We'll use 2x the wafer dia so that we can move center around a bit
    grid_max_x = 2 * int(math.ceil(dia / die_x))
    grid_max_y = 2 * int(math.ceil(dia / die_y))

    # 2. Determine the centerpoint
    if grid_center is None:
        grid_center = (grid_max_x/2 + x_offset, grid_max_y/2 + y_offset)
    print("Offsets: {}".format((x_offset, y_offset)))

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
            die_max_sqrd = wm_utils.max_dist_sqrd(coord_die_center, die_size)
#            coord_lower_left_x = coord_die_center_x - die_x/2
            coord_lower_left_y = coord_die_center_y - die_y/2
#            coord_lower_left = (coord_lower_left_x, coord_lower_left_y)
            if (die_max_sqrd > excl_sqrd
                    or coord_lower_left_y < (flat_y + flat_excl)):
                continue
            else:
                if dtype == 'discrete':
                    grid_points.append((_x,
                                        _y,
                                        random.choice(['a', 'b', 'c']),
                                        # these items are for debug.
#                                        coord_lower_left,
#                                        center_rad_sqrd,
#                                        coord_die_center,
#                                        die_max_sqrd,
                                        ))

                else:
                    grid_points.append((_x,
                                        _y,
                                        center_rad_sqrd,
                                        # these items are for debug.
#                                        coord_lower_left,
#                                        center_rad_sqrd,
#                                        coord_die_center,
#                                        die_max_sqrd,
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
    wafer, data = generate_fake_data(dtype='discrete')
    from pprint import pprint
    pprint(data)

#    print()
#    pprint([_i for _i in data if _i[0] in (17, 18, 19)])


if __name__ == "__main__":
    main()
