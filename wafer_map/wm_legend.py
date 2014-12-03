# -*- coding: utf-8 -*-
"""
@name:          wm_legend.py
@vers:          0.1.0
@author:        dthor
@created:       Tue Dec 02 16:39:58 2014
@descr:         Draws the wafer map legend

Usage:
    wm_legend.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.
"""

from __future__ import print_function, division, absolute_import
#from __future__ import unicode_literals
#from docopt import docopt
import wx
from wx.lib.floatcanvas import FloatCanvas
import wx.lib.colourselect as csel

__author__ = "Douglas Thor"
__version__ = "v0.1.0"


class Legend(wx.Panel):
    """
    Legend for discrete values

    Is basically a 2D table of label-color rows. The colors are actually
    buttons that can be clicked on - a color picker appears. However, as of
    2014-12-03, changing the color does not do anything.
    """
    def __init__(self,
                 parent,
                 labels,
                 colors,
                 ):
        """
        __init__(self, wx.Panel parent, list labels, list colors) -> wx.Panel
        """
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.labels = labels
        self.colors = colors
        self.n_items = len(self.labels)

        self.init_ui()

    def init_ui(self):

        # Add layout management
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.fgs = wx.FlexGridSizer(rows=self.n_items, cols=2, vgap=2, hgap=2)

        # Create items to add
        for key, value in zip(self.labels, self.colors):
            self.label = wx.StaticText(self,
                                       label=key,
                                       style=wx.ALIGN_LEFT | wx.SIMPLE_BORDER,
                                       )

            # I can use the csel.ColourSelect built-in with ease...
            #   This takes care of the colorbox stuff automaticlaly.
            self.colorbox = csel.ColourSelect(self,
                                              wx.ID_ANY,
                                              "",
                                              value,
                                              style=wx.NO_BORDER,
                                              size=(20, 20))

            self.fgs.Add(self.label, flag=wx.ALIGN_CENTER_VERTICAL)
            self.fgs.Add(self.colorbox)

        # Add our items to the layout manager and set the sizer.
        self.hbox.Add(self.fgs)
        self.SetSizer(self.hbox)


class LegendOverlay(FloatCanvas.Text):
    """ Demo of drawing overlay - to be used for legend """
    def __init__(self,
                 String,
                 xy,
                 Size=24,
                 Color="Black",
                 BackgroundColor=None,
                 Family=wx.MODERN,
                 Style=wx.NORMAL,
                 Weight=wx.NORMAL,
                 Underlined=False,
                 Font=None):
        FloatCanvas.Text.__init__(self,
                                  String,
                                  xy,
                                  Size=Size,
                                  Color=Color,
                                  BackgroundColor=BackgroundColor,
                                  Family=Family,
                                  Style=Style,
                                  Weight=Weight,
                                  Underlined=Underlined,
                                  Font=Font)

    # TODO: Change this so that it creates the custom legend
    def _Draw(self, dc, Canvas):
        """
        _Draw method for Overlay
         note: this is a differeent signarture than the DrawObject Draw
        """
        dc.SetFont(self.Font)
        dc.SetTextForeground(self.Color)
        if self.BackgroundColor:
            dc.SetBackgroundMode(wx.SOLID)
            dc.SetTextBackground(self.BackgroundColor)
        else:
            dc.SetBackgroundMode(wx.TRANSPARENT)
        dc.DrawTextPoint(self.String, self.XY)


def main():
    """ Display the Legend when module is run directly """

    legend_labels = ["A", "Banana!", "C", "Donut", "E"]

    legend_colors = [(0, 128, 0),
                     (0, 0, 255),
                     (255, 0, 0),
                     (128, 0, 128),
                     (0, 128, 128),
                     ]

    class ExampleFrame(wx.Frame):
        """ Base Frame """
        def __init__(self, title):
            wx.Frame.__init__(self,
                              None,                         # Window Parent
                              wx.ID_ANY,                    # id
                              title=title,                  # Window Title
                              size=(800 + 16, 600 + 38),    # Size in px
                              )

            self.Bind(wx.EVT_CLOSE, self.OnQuit)

            # Here's where we call the WaferMapPanel
            self.panel = Legend(self, legend_labels, legend_colors)

        def OnQuit(self, event):
            self.Destroy()

    app = wx.App()
    frame = ExampleFrame("Legend Example")
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
