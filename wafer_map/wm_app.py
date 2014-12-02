# -*- coding: utf-8 -*-
"""
@name:          wm_app.py
@vers:          0.1.0
@author:        dthor
@created:       Tue Dec 02 09:58:48 2014
@descr:         A self-contained Window for a Wafer Map.

Usage:
    wm_app.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.
"""

from __future__ import print_function, division, absolute_import
#from __future__ import unicode_literals
import wx
import wm_frame
import wm_info
import gen_fake_data

__author__ = "Douglas Thor"
__version__ = "v0.1.0"


class WaferMapApp(object):
    """
    A self-contained Window for a Wafer Map.
    """
    def __init__(self,
                 xyd,
                 die_size,
                 center_xy=(0, 0),
                 dia=150,
                 edge_excl=5,
                 flat_excl=5,
                 ):
        """
        __init__(self,
                 list xyd,
                 tuple die_size,
                 tuple center_xy=(0, 0),
                 float dia=150,
                 float edge_excl=5,
                 float flat_exlc=5) -> object
        """
        self.app = wx.App()
        self.wafer_info = wm_info.WaferInfo(die_size,
                                            (0, 0),
                                            dia,
                                            edge_excl,
                                            flat_excl,
                                            )
        self.xyd = xyd

        self.frame = wm_frame.WaferMapWindow("Wafer Map",
                                             self.xyd,
                                             self.wafer_info)

        self.frame.Show()
        self.app.MainLoop()


def main():
    """ Main Code """
#    raise RuntimeError("This module is not meant to be run by itself.")
    wafer_info, xyd = gen_fake_data.generate_fake_data()
    WaferMapApp(xyd,
                wafer_info.die_size,
                wafer_info.center_xy,
                wafer_info.dia,
                wafer_info.edge_excl,
                wafer_info.flat_excl,
                )


if __name__ == "__main__":
    main()
