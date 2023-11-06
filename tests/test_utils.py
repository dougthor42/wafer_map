# -*- coding: utf-8 -*-
"""
Unittests for the :module:`wafer_map.utils` module.
"""
# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

# Package/Application
from .. import wm_utils as utils


class LinearGradient(unittest.TestCase):

    known_values = (((0, 0, 0), (255, 255, 255), 0.5, (127, 127, 127)),
                    ((0, 0, 0), (255, 0, 0), 0.5, (95, 31, 31)),
                    ((0, 0, 0), (0, 255, 0), 0.5, (95, 95, 31)),
                    ((0, 0, 0), (0, 0, 255), 0.5, (31, 95, 31)),
                    )

    def test_known_values(self):
        for _start, _end,  _value, _expected in self.known_values:
            result = utils.linear_gradient(_start, _end, _value)
            self.assertEqual(result, _expected)
