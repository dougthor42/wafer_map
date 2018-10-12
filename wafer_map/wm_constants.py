# -*- coding: utf-8 -*-
"""
Constants for the wafer_map package.
"""
# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
from __future__ import absolute_import, division, print_function, unicode_literals
from enum import Enum

# Third-Party
import wx


# ---------------------------------------------------------------------------
### Constants
# ---------------------------------------------------------------------------
# Colors
wm_OOR_HIGH_COLOR = wx.Colour(255, 0, 128, 255)
wm_OOR_LOW_COLOR = wx.Colour(255, 128, 0, 255)
#wm_HIGH_COLOR = wx.Colour(255, 0, 0, 255)
wm_HIGH_COLOR = wx.Colour(0, 255, 128, 255)
#wm_LOW_COLOR = wx.Colour(0, 192, 0, 255)
wm_LOW_COLOR = wx.Colour(128, 0, 255, 255)
wm_INVALID_COLOR = wx.Colour(255, 255, 255, 255)
wm_OUTLINE_COLOR = wx.Colour(255, 255, 0, 255)          # yellow
wm_WAFER_EDGE_COLOR = wx.Colour(255, 0, 0, 255)         # red
wm_WAFER_CENTER_DOT_COLOR = wx.Colour(255, 0, 0, 255)   # red
wm_DIE_CENTER_DOT_COLOR = wx.Colour(255, 0, 0, 255)     # red
wm_CROSSHAIR_COLOR = wx.Colour(0, 255, 255, 255)        # cyan
wm_TICK_COUNT = 11

# Continuous Data Gradient sizez in px.
wm_GRAD_W = 30
wm_GRAD_H = 500
wm_TICK_W = 20
wm_SPACER = 5

wm_ZOOM_FACTOR = 1.1 / 120

# Wafer Flat lengths, defined by SEMI M1-0302
wm_FLAT_LENGTHS = {50: 15.88, 75: 22.22, 100: 32.5, 125: 42.5, 150: 57.5}


class NoValueEnum(Enum):
    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)


class DataType(NoValueEnum):
    CONTINUOUS = 'continuous'
    DISCRETE = 'discrete'


class CoordType(NoValueEnum):
    ABSOLUTE = 'absolute'
    RELATIVE = 'relative'
