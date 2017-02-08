# -*- coding: utf-8 -*-
"""
__init__ for wafer_map.

Determines the python version and monkeypatches wx.Colour.
"""
import os
import sys


### Constants ###############################################################
#__all__ = ['wm_app', 'wm_constants', 'wm_core', 'wm_frame', 'wm_info',
#           'wm_legend', 'wm_utils']


if sys.version_info < (3, ):
    PY2 = True
elif sys.version_info < (2, 6):
    raise RuntimeError("Only Python >= 2.7 is supported.")
else:
    PY2 = False


# if we're building docs, don't try and import or monkeypatch wxPython.
if os.getenv("READTHEDOCS", "False") == "True":
    pass
else:
    # Fix hashing for wx.Colour
    # See https://groups.google.com/forum/#!topic/wxpython-dev/NLd4CZv9rII
    import wx
    ok = getattr(wx.Colour, "__hash__")
    if ok is None:
        def _Colour___hash(self):
            return hash(tuple(self.Get()))
        wx.Colour.__hash__ = _Colour___hash
