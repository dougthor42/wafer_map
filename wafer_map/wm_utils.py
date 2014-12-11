# -*- coding: utf-8 -*-
"""
@name:          new_program.py
@vers:          0.1.0
@author:        dthor
@created:       Thu Dec 04 16:12:07 2014
@descr:         A new file

Usage:
    new_program.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.
"""

from __future__ import print_function, division, absolute_import
#from __future__ import unicode_literals
import numpy as np
import math


def frange(start, stop, step):
    """ Generator that creates an arbitrary-stepsize range. """
    r = start
    while r < stop:
        yield r
        r += step


def coord_to_grid(coord, die_size, grid_center):
    """
    Converts a panel coordinate to a grid value.
    """
    # TODO: seems have a error with negative 0 grid values.
    grid_x = int(grid_center[0] + 0.5 + (coord[0] / die_size[0]))
    grid_y = int(grid_center[1] + 0.5 - (coord[1] / die_size[1]))
    return (grid_x, grid_y)


def grid_to_rect_coord(grid, die_size, grid_center):
    """
    Converts a die's grid value to the origin point of the rectangle to draw.

    Adjusts for the fact that the grid falls on the center of a die by
    subtracting die_size/2 from the coordinate.

    Adjusts for the fact that Grid +y is down while panel +y is up by
    taking ``grid_center - grid`` rather than ``grid - grid_center`` as is
    done in the X case.
    """
    _x = die_size[0] * (grid[0] - grid_center[0] - 0.5)
    _y = die_size[1] * (grid_center[1] - grid[1] - 0.5)
    return (_x, _y)


def nanpercentile(a, percentile):
    """
    Performs a numpy.percentile(a, percentile) calculation while
    ignoring NaN values.

    Only works on a 1D array.
    """
    if type(a) != np.ndarray:
        a = np.array(a)
    return np.percentile(a[np.logical_not(np.isnan(a))], percentile)


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


def rescale(x, (original_min, original_max), (new_min, new_max)=(0, 1)):
    """
    Rescales x (which was part of scale original_min to original_max)
    to run over a range new_min to new_max such
    that the value x maintains position on the new scale new_min to new_max.
    If x is outside of xRange, then y will be outside of yRange.

    Default new scale range is 0 to 1 inclusive.

    Examples:
    rescale(5, (10, 20), (0, 1)) = -0.5
    rescale(27, (0, 200), (0, 5)) = 0.675
    rescale(1.5, (0, 1), (0, 10)) = 15.0
    """
    part_a = x * (new_max - new_min)
    part_b = original_min * new_max - original_max * new_min
    denominator = original_max - original_min
    result = (part_a - part_b)/denominator
    return float(result)


def rescale_clip(x, (original_min, original_max), (new_min, new_max)=(0, 1)):
    """
    Same as rescale, but also clips the new data. Any result that is
    below new_min or above new_max is listed as new_min or
    new_max, respectively

    Example:
    rescale_clip(5, (10, 20), (0, 1)) = 0
    rescale_clip(15, (10, 20), (0, 1)) = 0.5
    rescale_clip(25, (10, 20), (0, 1)) = 1
    """
    result = rescale(x, (original_min, original_max), (new_min, new_max))
    if result > new_max:
        return new_max
    elif result < new_min:
        return new_min
    else:
        return result
