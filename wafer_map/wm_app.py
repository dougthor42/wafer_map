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

# check to see if we can import from the dev folder, otherwise import
# from the standard install folder, site-packages
if 'site-packages' in __file__:
    from wafer_map import wm_frame
    from wafer_map import wm_info
    from wafer_map import gen_fake_data
    from wafer_map.wm_constants import *
else:
    print("Running wm_app from Development Location")
    import wm_frame
    import wm_info
    import gen_fake_data
    from wm_constants import *


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
                 high_color=wm_HIGH_COLOR,
                 low_color=wm_LOW_COLOR,
                 plot_range=None,
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
#        self.app = wit.InspectableApp()

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

        self.frame = wm_frame.WaferMapWindow("Wafer Map",
                                             self.xyd,
                                             self.wafer_info,
                                             data_type=self.data_type,
                                             high_color=self.high_color,
                                             low_color=self.low_color,
                                             plot_range=self.plot_range,
                                             )

        self.frame.Show()
        self.app.MainLoop()


def main():
    """ Main Code """
#    raise RuntimeError("This module is not meant to be run by itself.")
    wafer_info, xyd = gen_fake_data.generate_fake_data(die_x=5.4,
                                                       die_y=3.6,
                                                       dia=150,
                                                       edge_excl=5,
                                                       flat_excl=5,
                                                       x_offset=0.5,
                                                       y_offset=0.5,
                                                       )

    import random
    num_discrete_values = random.randint(2, 10)
#    num_discrete_values = 3
    discrete_xyd = [(grid_x, grid_y, random.randint(1, num_discrete_values))
                    for grid_x, grid_y, _
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
                )


if __name__ == "__main__":
    main()
