# -*- coding: utf-8 -*-
"""
Unittests for the two required changes to wxPython_Phoenix source code.

Created on Fri Mar 25 12:14:25 2016

@author: dthor
"""
# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
import unittest

# Third-Party
import wx
from wx.lib.floatcanvas import FloatCanvas


class TestWxPython(unittest.TestCase):

    def setUp(cls):
        cls.app = wx.App()

    def tearDown(cls):
        pass

    def test_colour_hashable(self):
        try:
            hash(wx.Colour(0, 0, 0))
        except TypeError:
            self.fail("Has wx/core.py been edited correctly?")

    def test_floatcanvas_group(self):
        item1 = FloatCanvas.Circle((0, 0), 10)
        item2 = FloatCanvas.Circle((0, 5), 10)
        item3 = FloatCanvas.Circle((5, 5), 10)
        try:
            FloatCanvas.Group([item1, item2, item3])
        except AttributeError:
            self.fail("Has wx/lib/floatcanvas/FCObjects.py been edited correctly?")
