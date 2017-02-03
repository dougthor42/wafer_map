# -*- coding: utf-8 -*-
"""
wafer_map
=========

Plots up a wafer map. Used in semiconductor processing and analysis.

Please see README.md and CHANGELOG.md.

"""

### Constants ###############################################################
__version__ = "1.0.17"
__project_url__ = "https://github.com/dougthor42/wafer_map"
__project_name__ = "wafer_map"
__description__ = "Semiconductor Wafer Mapping"
__long_descr__ = __doc__
#__all__ = ['wm_app', 'wm_constants', 'wm_core', 'wm_frame', 'wm_info',
#           'wm_legend', 'wm_utils']


import sys
if sys.version_info < (3, ):
    PY2 = True
elif sys.version_info < (2, 6):
    raise RuntimeError("Only Python >= 2.7 is supported.")
else:
    PY2 = False


# Fix hashing for wx.Colour
# See https://groups.google.com/forum/#!topic/wxpython-dev/NLd4CZv9rII
import wx
ok = getattr(wx.Colour, "__hash__")
if ok is None:
    def _Colour___hash(self):
        return hash(tuple(self.Get()))
    wx.Colour.__hash__ = _Colour___hash
