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

from __future__ import print_function, division#, absolute_import
#from __future__ import unicode_literals
import wx
import wm_frame
import wm_info
import wafer_map.gen_fake_data as gen_fake_data
import wafer_map.wm_constants as wm_const


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
                 data_type='continuous',
                 high_color=wm_const.wm_HIGH_COLOR,
                 low_color=wm_const.wm_LOW_COLOR,
                 plot_range=None,
                 plot_die_centers=False,
                 ):
        """
        __init__(self,
                 list xyd,
                 tuple die_size,
                 tuple center_xy=(0, 0),center_xy
                 float dia=150,
                 float edge_excl=5,
                 float flat_exlc=5,
                 string data_type='continuous',
                 ) -> object
        """
        self.app = wx.App()

        self.wafer_info = wm_info.WaferInfo(die_size,
                                            center_xy,
                                            dia,
                                            edge_excl,
                                            flat_excl,
                                            )
        self.xyd = xyd
        self.data_type = data_type
        self.high_color = high_color
        self.low_color = low_color
        self.plot_range = plot_range
        self.plot_die_centers = plot_die_centers

        self.frame = wm_frame.WaferMapWindow("Wafer Map",
                                             self.xyd,
                                             self.wafer_info,
                                             data_type=self.data_type,
                                             high_color=self.high_color,
                                             low_color=self.low_color,
#                                             high_color=wx.Colour(255, 0, 0),
#                                             low_color=wx.Colour(0, 0, 255),
                                             plot_range=self.plot_range,
                                             size=(600, 500),
                                             plot_die_centers=self.plot_die_centers,
                                             )

        self.frame.Show()
        self.app.MainLoop()


def main():
    """ Main Code """
    wafer_info, xyd = gen_fake_data.generate_fake_data(die_x=4.43,
                                                       die_y=6.3,
                                                       dia=150,
                                                       edge_excl=4.5,
                                                       flat_excl=4.5,
                                                       x_offset=0,
                                                       y_offset=0.5,
                                                       grid_center=(29, 21.5),
                                                       )

    import random
    bins = ["Bin1", "Bin1", "Bin1", "Bin2", "Dragons", "Bin1", "Bin2"]
    discrete_xyd = [(_x, _y, random.choice(bins))
                    for _x, _y, _
                    in xyd]

    discrete = False
    dtype = 'continuous'

#    discrete = True         # uncomment this line to use discrete data
    if discrete:
        xyd = discrete_xyd
        dtype = 'discrete'

    WaferMapApp(xyd,
                wafer_info.die_size,
                wafer_info.center_xy,
                wafer_info.dia,
                wafer_info.edge_excl,
                wafer_info.flat_excl,
                data_type=dtype,
#                plot_range=(0.0, 75.0**2),
                plot_die_centers=True,
                )


if __name__ == "__main__":
    main()
