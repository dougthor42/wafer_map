# -*- coding: utf-8 -*-
"""
Test file that hopefully demonstrates the issue wherein the
colourselect.EVT_COLOURSELECT event messes with the
FloatCanvas.EVT_MOUSEWHEEL event.

See http://stackoverflow.com/questions/27413232/wx-lib-evt-colourselect-interfering-with-wx-lib-floatcanvas-evt-mousewheel
"""

from __future__ import print_function, division, absolute_import
#from __future__ import unicode_literals
#from docopt import docopt
import wx
from wx.lib.floatcanvas import FloatCanvas
import random
from wafer_map import wm_core, wm_info


class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title='test')

        self.menu_bar = wx.MenuBar()
        self.mfile = wx.Menu()
        self.mf_close = wx.MenuItem(self.mfile,
                                    wx.ID_ANY,
                                    "&Close\tCtrl+Q",
                                    "TestItem",
                                    )
        self.mfile.AppendItem(self.mf_close)
        self.menu_bar.Append(self.mfile, "&File")
        self.SetMenuBar(self.menu_bar)

        self.CreateStatusBar()

        self.listbox = wx.ListBox(self,
                                  wx.ID_ANY,
                                  choices=['A', 'B', 'C', 'D'],
                                  )
        self.button = wx.Button(self, wx.ID_ANY, label="Big Button!")

        self.panel = MainPanel(self)
        self.Bind(wx.EVT_MENU, self.on_quit, self.mf_close)
        self.Bind(wx.EVT_CLOSE, self.on_quit)

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.panel, 1, wx.EXPAND)
        self.hbox.Add(self.listbox, 1, wx.EXPAND)
        self.hbox.Add(self.button, 1, wx.EXPAND)
        self.hbox.Add(self.vbox, 3, wx.EXPAND)
        self.SetSizer(self.hbox)

    def on_quit(self, event):
        print("quitting!")
        self.Destroy()


class Legend(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox.Add(wx.StaticText(self, label="Placeholder"))
        self.hbox.Add((100, 100))
        self.SetSizer(self.hbox)


class MainPanel(wx.Panel):
    """ Emulates wm_panel.WaferMapPanel """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

#        data = [(1, 2, 3), (1, 3, 4), (2, 2, 1), (2, 4, 5)]
#        wfr_info = wm_info.WaferInfo((2, 2), center_xy=(1, 1))
#        self.canvas = wm_core.WaferMapPanel(self, data, wfr_info)
        self.canvas = FloatCanvas.FloatCanvas(self,
                                              BackgroundColor="BLUE")
        self.canvas.InitAll()

        self.legend = Legend(self)

        self.canvas.Bind(FloatCanvas.EVT_MOUSEWHEEL, self.mouse_wheel)
        self.canvas.Bind(wx.EVT_KEY_DOWN, self.key_down)
#        self.Bind(FloatCanvas.EVT_LEFT_DOWN, self.on_click)

        # set our layout
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox.Add(self.legend, 0, wx.EXPAND)
        self.hbox.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(self.hbox)

    def mouse_wheel(self, event):
        print("mousewheel {}".format(event.GetWheelRotation()))
        self.on_click(event)

    def key_down(self, event):
        key = event.GetKeyCode()
        print("KeyCode: {}".format(key))

    def on_click(self, event):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = wx.Colour(r, g, b, 255)
        self.canvas.SetBackgroundColour(color)
        self.canvas.ClearBackground()


print("test.py loaded")


def main():
    """ Main Code """
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
