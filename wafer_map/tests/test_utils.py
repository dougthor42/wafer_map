# -*- coding: utf-8 -*-
"""
@name:          new_program.py
@vers:          0.1.0
@author:        dthor
@created:       Wed Dec 17 08:46:21 2014
@descr:         A new file

Usage:
    new_program.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.
"""

from __future__ import print_function, division, absolute_import
import unittest

from .. import wm_utils as utils


__author__ = "Douglas Thor"
__version__ = "v0.1.0"


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


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
