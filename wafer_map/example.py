# -*- coding: utf-8 -*-
"""
@name:          example.py
@vers:          0.4.0
@author:        dthor
@created:       Tue Nov 25 13:13:33 2014
@descr:         Provides examples on how to call wafer_map.py

Usage:
    example.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.

Description:
    Provides an example on how to use the wafer_map module.
"""

from __future__ import print_function, division#, absolute_import
#from __future__ import unicode_literals
import wx

import wafer_map.gen_fake_data as gen_fake_data
import wafer_map.wm_core as wm_core
import wafer_map.wm_app as wm_app

__author__ = "Douglas Thor"
__version__ = "v0.4.0"


def standalone_app(xyd, wafer_info):
    """
    Example of running wafer_map as a standalone application.

    All you need to do once you have your data in the correct

      ``[(grid_x_1, grid_y_1, data_1), (grid_x_2, grid_y_2, data_2), ..., ]``

    format, is to call ``wm_app.WaferMapApp`` with your keyword arguments
    which define the wafer and die parameters such as die size, the wafer
    diameter, and the edge exclusion.
    """
    wm_app.WaferMapApp(xyd,
                       wafer_info.die_size,
                       wafer_info.center_xy,
                       wafer_info.dia,
                       wafer_info.edge_excl,
                       wafer_info.flat_excl,
                       )


def add_to_existing_app(xyd, wafer_info):
    """
    Example of adding the wafer map to your existing wxPython application.

    To add a wafer map to an existing application, instance the
    ``wm_core.WaferMapPanel()`` class with your data and wafer info. The
    wafer info must be a ``wm_info.WaferInfo`` object.
    """
    app = wx.App()

    class ExampleFrame(wx.Frame):
        """ Base Frame """
        def __init__(self, title, xyd, wafer_info):
            wx.Frame.__init__(self,
                              None,                         # Window Parent
                              wx.ID_ANY,                    # id
                              title=title,                  # Window Title
                              size=(600 + 16, 500 + 38),    # Size in px
                              )
            self.xyd = xyd
            self.wafer_info = wafer_info

            # Add a status bar if you want to
            self.CreateStatusBar()

            # Bind events
            self.Bind(wx.EVT_CLOSE, self.OnQuit)

            # Create some other dummy stuff for the example
            self.listbox = wx.ListBox(self,
                                      wx.ID_ANY,
                                      choices=['A', 'B', 'C', 'D'],
                                      )
            self.button = wx.Button(self, wx.ID_ANY, label="Big Button!")

            # Create the wafer map
            self.panel = wm_core.WaferMapPanel(self,
                                               self.xyd,
                                               self.wafer_info)

            # set our layout
            self.hbox = wx.BoxSizer(wx.HORIZONTAL)
            self.vbox = wx.BoxSizer(wx.VERTICAL)

            self.vbox.Add(self.panel, 1, wx.EXPAND)
            self.vbox.Add(self.button, 1, wx.EXPAND)
            self.hbox.Add(self.listbox, 1, wx.EXPAND)
            self.hbox.Add(self.vbox, 1, wx.EXPAND)
            self.SetSizer(self.hbox)

        def OnQuit(self, event):
            self.Destroy()

    frame = ExampleFrame("Called as a panel in your own app!", xyd, wafer_info)
    frame.Show()
    app.MainLoop()


def discrete_data_example(xyd, wafer_info):
    """
    Example of plotting discrete data using the standalone app version.

    Plotting discrete data is the same as continuous data, but you need to
    add the ``data_type`` arguement to the class initialization.
    """
    import random
    bins = ["Bin1", "Bin1", "Bin1", "Bin2", "Dragons", "Bin1", "Bin2"]
    discrete_xyd = [(_x, _y, random.choice(bins))
                    for _x, _y, _
                    in xyd]

    wm_app.WaferMapApp(discrete_xyd,
                       wafer_info.die_size,
                       wafer_info.center_xy,
                       wafer_info.dia,
                       wafer_info.edge_excl,
                       wafer_info.flat_excl,
                       data_type="discrete",
                       )


def main():
    """ Main Code """
    # Generate some fake data
    wafer_info, xyd = gen_fake_data.generate_fake_data()

    standalone_app(xyd, wafer_info)
    add_to_existing_app(xyd, wafer_info)
    discrete_data_example(xyd, wafer_info)

if __name__ == "__main__":
    main()
