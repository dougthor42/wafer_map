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
# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
import os.path as osp

# Third-Party
import wx

# Package / Application
if "github" in osp.abspath(__file__):
    import sys
#    [print(_p) for _p in sys.path]
#    print("running {} from the dev dir".format(osp.split(__file__)[1]))
    sys.path.append(osp.dirname(osp.dirname(osp.abspath(__file__))))
else:
#    print("importing from site-packages")
    pass

try:
    # Imports used for unittests
    from . import wm_frame as wm_frame
    from . import wm_info as wm_info
    from . import gen_fake_data as gen_fake_data
    from . import wm_constants as wm_const
#    from . import (__project_name__,
#                   __version__,
#                   )
#    logging.debug("Imports for UnitTests")
except SystemError:
    try:
        # Imports used by Spyder
        import wm_frame as wm_frame
        import wm_info as wm_info
        import gen_fake_data as gen_fake_data
        import wm_constants as wm_const
#        from __init__ import (__project_name__,
#                              __version__,
#                              )
#        logging.debug("Imports for Spyder IDE")
    except ImportError:
         # Imports used by cx_freeze
        from wafer_map import wm_frame as wm_frame
        from wafer_map import wm_info as wm_info
        from wafer_map import gen_fake_data as gen_fake_data
        from wafer_map import wm_constants as wm_const
#        from pybank import (__project_name__,
#                            __version__,
#                            )
#        logging.debug("imports for Executable")

#print("Imports for WM_APP:")
#print("wm_app:\t\t{}".format(__file__))
#print("wm_frame:\t\t{}".format(wm_frame.__file__))
#print("wm_info:\t\t{}".format(wm_info.__file__))
#print("gen_fake_data:\t{}".format(gen_fake_data.__file__))
#print("wm_const:\t\t{}".format(wm_const.__file__))


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

        self.frame = wm_frame.WaferMapWindow("Wafer Map Phoenix",
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
    wafer_info, xyd = gen_fake_data.generate_fake_data(die_x=5.43,
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
#    pass
