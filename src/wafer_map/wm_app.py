# -*- coding: utf-8 -*-
"""
A self-contained Window for a Wafer Map.
"""
# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
from __future__ import absolute_import, division, print_function, unicode_literals

# Third-Party
import wx

# Package / Application
from . import wm_frame
from . import wm_info
from . import gen_fake_data
from . import wm_constants as wm_const


class WaferMapApp(object):
    """
    A self-contained Window for a Wafer Map.

    Parameters
    ----------
    xyd : list of 3-tuples
        The data to plot.
    die_size : tuple
        The die size in mm as a ``(width, height)`` tuple.
    center_xy : tuple, optional
        The center grid coordinate as a ``(x_grid, y_grid)`` tuple.
    dia : float, optional
        The wafer diameter in mm. Defaults to `150`.
    edge_excl : float, optional
        The distance in mm from the edge of the wafer that should be
        considered bad die. Defaults to 5mm.
    flat_excl : float, optional
        The distance in mm from the wafer flat that should be
        considered bad die. Defaults to 5mm.
    data_type : wm_constants.DataType or str, optional
        The type of data to plot. Must be one of `continuous` or `discrete`.
    high_color : :class:`wx.Colour`, optional
        The color to display if a value is above the plot range. Defaults
        to `wm_constants.wm_HIGH_COLOR`.
    low_color : :class:`wx.Colour`, optional
        The color to display if a value is below the plot range. Defaults
        to `wm_constants.wm_LOW_COLOR`.
    plot_range : tuple, optional
        The plot range to display. If ``None``, then auto-ranges. Defaults
        to auto-ranging.
    plot_die_centers : bool, optional
        If ``True``, display small red circles denoting the die centers.
        Defaults to ``False``.
    show_die_gridlines : bool, optional
        If ``True``, displayes gridlines along the die edges. Defaults to
        ``True``.
    """

    def __init__(self,
                 xyd,
                 die_size,
                 center_xy=(0, 0),
                 dia=150,
                 edge_excl=5,
                 flat_excl=5,
                 data_type=wm_const.DataType.CONTINUOUS,
                 high_color=wm_const.wm_HIGH_COLOR,
                 low_color=wm_const.wm_LOW_COLOR,
                 plot_range=None,
                 plot_die_centers=False,
                 show_die_gridlines=True,
                 ):
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
        self.show_die_gridlines=show_die_gridlines

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
                                             show_die_gridlines=self.show_die_gridlines,
                                             )

        self.frame.Show()
        self.app.MainLoop()


def main():
    """Run when called as a module."""
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
    dtype = wm_const.DataType.CONTINUOUS

#    discrete = True         # uncomment this line to use discrete data
    if discrete:
        xyd = discrete_xyd
        dtype = wm_const.DataType.DISCRETE

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
