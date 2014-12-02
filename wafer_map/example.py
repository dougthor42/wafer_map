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
    Provides an example on how to use the wafer_map.py module.
"""

from __future__ import print_function, division, absolute_import
#from __future__ import unicode_literals
#from docopt import docopt
import wx
import gen_fake_data

__author__ = "Douglas Thor"
__version__ = "v0.4.0"


def main():
    """ Main Code """
    # Generate some fake data
    import wafer_map
    wafer_info, xyd = gen_fake_data.generate_fake_data()

    # Example of calling the Standalone App:
    import wm_app
    wm_app.WaferMapApp(xyd,
                       wafer_info.die_size,
                       wafer_info.center_xy,
                       wafer_info.dia,
                       wafer_info.edge_excl,
                       wafer_info.flat_excl,
                       )

    # Example of adding the WaferMapPanel to an existing App:
    app = wx.App()

    class ExampleFrame(wx.Frame):
        """ Base Frame """
        def __init__(self, title, xyd, wafer_info):
            wx.Frame.__init__(self,
                              None,                         # Window Parent
                              wx.ID_ANY,                    # id
                              title=title,                  # Window Title
                              size=(800 + 16, 600 + 38),    # Size in px
                              )
            self.xyd = xyd
            self.wafer_info = wafer_info

            self.Bind(wx.EVT_CLOSE, self.OnQuit)

            # Here's where we call the WaferMapPanel
            self.panel = wafer_map.WaferMapPanel(self,
                                                 self.xyd,
                                                 self.wafer_info)

        def OnQuit(self, event):
            self.Destroy()

    frame = ExampleFrame("Called directly!", xyd, wafer_info)
    frame.Show()
    app.MainLoop()

    # Example showing how discrete data looks
    import random
    discrete_xyd = [(_x, _y, random.randint(1, 6))
                    for _x, _y, _
                    in xyd]

    class ExampleFrame(wx.Frame):
        """ Base Frame """
        def __init__(self, title, xyd, wafer_info, data_type):
            wx.Frame.__init__(self,
                              None,                         # Window Parent
                              wx.ID_ANY,                    # id
                              title=title,                  # Window Title
                              size=(800 + 16, 600 + 38),    # Size in px
                              )
            self.xyd = xyd
            self.wafer_info = wafer_info
            self.data_type = data_type

            self.Bind(wx.EVT_CLOSE, self.OnQuit)

            # Here's where we call the WaferMapPanel
            self.panel = wafer_map.WaferMapPanel(self,
                                                 self.xyd,
                                                 self.wafer_info,
                                                 self.data_type)

        def OnQuit(self, event):
            self.Destroy()

    frame = ExampleFrame("Called directly with Discrete Data",
                         discrete_xyd,
                         wafer_info,
                         data_type='discrete')
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
