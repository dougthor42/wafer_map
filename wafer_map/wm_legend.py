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
import numpy as np
from wx.lib.floatcanvas import FloatCanvas
import wx.lib.colourselect as csel
import wx.lib.colourchooser.pycolourslider as cs
from colour import Color
import colorsys

# check to see if we can import local, otherwise import absolute
print(__file__)
if 'site-packages' in __file__:
    print("we're being run from site-pkg")
    from wafer_map import wm_utils
else:
    print("running in dev mode")
    import wm_utils

__author__ = "Douglas Thor"
__version__ = "v0.1.0"


# TODO: Update to Bezier Curves for colors. See http://bsou.io/p/3


class Legend(object):
    """ Base class for both discrete and continuous legends """
    pass


class ContinuousLegend(wx.Panel):
    """
    Legend for continuous values.

    This is a color gradient with a few select labels. At minumum, the high
    and low values will be labeled. I plan on allowing the user to set
    the number of labels.

    Initially, it will be fixed to 3 labels: high, mid, low.

    Here's the logic:

    1.  Upon Init of the Legend, create an instance attribute MemoryDC
        to store the gradient.
    2.  Create the gradient using the convienent GradientFillLinear method.
    3.  We now have a buffer that we can access to pull the color values from
    4.  To actually paint the item, we have to access the paint event.

        a.  Inside the on_paint method, we create a new temporary PaintDC.
        b.  Get the size of the instance MemoryDC
        c.  Copy the instance MemoryDC to the temporary PaintDC
        d.  Exiting out of the on_paint event destroys the PaintDC which
            actually draws it on the screen.

    5.  We can now access our instance MemoryDC with the GetPixelPoint method.

    For now, I'm leaving on_size disabled. This may change in the future.
    """
    def __init__(self, parent, plot_range):
        """
        __init__(self, wx.Panel parent, tuple plot_range) -> wx.Panel
        """
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.plot_range = plot_range

        self.w = 20
        self.h = 500

        self.mdc = wx.MemoryDC(wx.EmptyBitmap(self.w, self.h))
        self.mdc.GradientFillLinear((0, 0, self.w, self.h),
                                    wx.GREEN,
                                    wx.RED,
                                    wx.NORTH,
                                    )

        print(self.mdc.GetPixelPoint((2, self.h/4)))
#
        self.Bind(wx.EVT_PAINT, self.on_paint)
#        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOTION, self.mouse_move)
        self.Bind(wx.EVT_LEFT_DOWN, self.left_click)

    def init_ui(self):
        """
        build the ui.
        """
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.hbox)

#    def on_size(self, event):
#        w, h = self.GetClientSize()
#        self.mdc = wx.MemoryDC(wx.EmptyBitmap(w, h))
#        self.mdc.GradientFillLinear((0, 0, w, h),
#                                    wx.GREEN,
#                                    wx.RED,
#                                    wx.NORTH,
#                                    )
#        self.Refresh()

    def on_paint(self, event):
        """ Draw the gradient """
        dc = wx.PaintDC(self)
        w, h = self.mdc.GetSize()
        dc.Blit(0, 0, w, h, self.mdc, 0, 0)

    def mouse_move(self, event):
        """ Used for debugging """
        pass
#        pos = event.GetPosition()
#        # only display colors if we're inside the gradient
#        w, h = self.mdc.GetSize()
#        if pos[0] < w and pos[1] < h:
#            a = self.mdc.GetPixelPoint(event.GetPosition())
#            print(pos, a)

    def left_click(self, event):
        """ Used for debugging """
        pos = event.GetPosition()
        w, h = self.mdc.GetSize()
        if pos[0] < w and pos[1] < h:
            val = wm_utils.rescale(pos[1], (0, self.h - 1), self.plot_range)
            a = self.mdc.GetPixelPoint(event.GetPosition())
            print("{}\t{}\t{}".format(pos, a, val))

    def get_color(self, value):
        """
        Gets a color from the gradient
        """
        pxl = int(wm_utils.rescale(value, self.plot_range, (0, self.h - 1)))
        point = (0, pxl)
        color = self.mdc.GetPixelPoint(point)
        return color


# DON'T TOUCH! It's kinda working...
# but not entirely. So screw it.
class ContinuousLegend_old(wx.Panel):
    """
    Legend for continuous values.

    This is a color gradient with a few select labels. At minumum, the high
    and low values will be labeled. I plan on allowing the user to set
    the number of labels.

    Initially, it will be fixed to 3 labels: high, mid, low.
    """
    def __init__(self, parent, plot_range):
        """
        __init__(self, wx.Panel parent, tuple plot_range) -> wx.Panel
        """
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.plot_range = plot_range
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        self.width = 20
        self.height = 500

#        self.dc = wx.ClientDC(self)
#        self.dc.GradientFillLinear((0, 0, self.width, self.height),
#                                   wx.GREEN,
#                                   wx.RED,
#                                   wx.NORTH,
#                                   )

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOTION, self.mouse_move)

    def init_ui(self):
        """
        build the ui.
        """
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.hbox)

    def on_size(self, event):
        event.Skip()
        self.Refresh()

    def on_paint(self, event):
        """ Draw the gradient """
        self.w, self.h = w, h = self.GetClientSize()
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
#        dc.DrawLine(0, 0, w, h)
#        dc.SetPen(wx.Pen(wx.BLACK, 5))
#        dc.DrawCircle(w / 2, h / 2, 100)
        dc.GradientFillLinear((0, 0, w, h),
                              wx.GREEN,
                              wx.RED,
                              wx.NORTH,
                              )
        self.mdc = wx.MemoryDC(dc.GetAsBitmap())

    def mouse_move(self, event):
        pos = event.GetPosition()
        # only display colors if we're inside the gradient
        if pos[0] < self.w and pos[1] < self.h:
            a = self.mdc.GetPixelPoint(event.GetPosition())
            print(pos, a)

    def get_color(self, value):
        """
        Gets a color from the gradient
        """
#        pxl = int(wm_utils.rescale(value, self.plot_range, (0, self.height - 1)))
#        pxl = value
#        point = (0, pxl)
#        color = self.mdc.GetPixelPoint(point)
#        return color
#        pass


class DiscreteLegend(wx.Panel):
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
                              size=(200 + 16, 550 + 38),    # Size in px
                              )

            self.Bind(wx.EVT_CLOSE, self.OnQuit)

            # Here's where we call the WaferMapPanel
            self.hbox = wx.BoxSizer(wx.HORIZONTAL)

            self.d_legend = DiscreteLegend(self, legend_labels, legend_colors)
            self.c_legend = ContinuousLegend(self, (0, 1))

            self.hbox.Add(self.d_legend, 1, wx.EXPAND)
            self.hbox.Add(self.c_legend, 1, wx.EXPAND)
            self.SetSizer(self.hbox)

        def OnQuit(self, event):
            self.Destroy()

    app = wx.App()
    frame = ExampleFrame("Legend Example")
    frame.Show()
    for _i in [0, 0.5, 0.75, 1]:
        print(_i, frame.c_legend.get_color(_i))
    app.MainLoop()


if __name__ == "__main__":
    main()
