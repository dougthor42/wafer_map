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

        # Set some other instance attributes
        self.num_ticks = 11

        # We need to set some parameters before making the bitmap. How do?
        # Create the MemoryDC now - we'll add the bitmap later.
        self.mdc = wx.MemoryDC()
        self.mdc.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL,
                                 wx.FONTWEIGHT_NORMAL))

        # Set various sizes, some of which are based on things like the
        # text height:
        #       self.mdc.GetTextExtent("Longest String")
        # or the client size:
        #       self.GetClientSize().
        # We need to move the gradient down a bit so that the top and bottom
        # labels are not cut off.
        # TODO: Replace these contants with code that finds the sizes
        # These are in a specific order. Do not change!
        # First determine some fixed items
        self.text_h = self.mdc.GetTextExtent("A")[1]
        self.grad_w = 30            # total gradient width (px)
        self.grad_h = 500           # total gradient height (px)
        self.tick_w = 20            # tick mark length
        self.spacer = 5             # spacer speration between items
        self.grad_start_y = self.text_h / 2
        self.grad_end_y = self.grad_start_y + self.grad_h

        # Now that the widths are defined, I can calculate some other things
        self.ticks = self.calc_ticks()
        self.text_w = self.get_max_text_w(self.ticks)

        # back to sizes...
        # Note: I'm intentionally listing every spacer manually rather than
        #       multiplying by how many there are. This makes it easier
        #       to see where they are.
        self.tick_start_x = self.spacer + self.text_w + self.spacer
        self.grad_start_x = self.tick_start_x + self.tick_w + self.spacer
        self.grad_end_x = self.grad_start_x + self.grad_w
        self.dc_w = self.grad_end_x + self.spacer
        self.dc_h = self.grad_h + self.text_h   # total bitmap height

        self.init_ui()

        # Create the MemoryDC where we do all of the drawing.
#        self.mdc = wx.MemoryDC(wx.EmptyBitmap(self.w, self.h))
        self.mdc.SelectObject(wx.EmptyBitmap(self.dc_w, self.dc_h))

        # Draw a rectangle to make the background
        # TODO: change the bitmap background to be transparent
        c = wx.Colour(200, 230, 230)
        pen = wx.Pen(c)
        brush = wx.Brush(c)
        self.mdc.SetPen(pen)
        self.mdc.SetBrush(brush)
        self.mdc.DrawRectangle(0, 0, self.dc_w, self.dc_h)

        # Draw the Gradient on a portion of the MemoryDC
        self.draw_gradient()
#        self.mdc.GradientFillLinear((self.grad_start_x, self.grad_start_y,
#                                     self.grad_w, self.grad_h),
#                                    wx.BLACK,
#                                    wx.YELLOW,
#                                    wx.NORTH,
#                                    )

        # Calculate and draw the tickmarks.

        self.print_ticks(self.ticks)

        # Bind various events
        self.Bind(wx.EVT_PAINT, self.on_paint)
#        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOTION, self.mouse_move)
        self.Bind(wx.EVT_LEFT_DOWN, self.left_click)



    def init_ui(self):
        """
        Add a Sizer that is the same size as the MemoryDC
        """
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox.Add((self.dc_w, self.dc_h))
        self.SetSizer(self.hbox)

#    def on_size(self, event):
#        w, h = self.GetClientSize()
#        self.mdc = wx.MemoryDC(wx.EmptyBitmap(w, h))
#        self.draw_gradient()
#        self.Refresh()

    def on_paint(self, event):
        """ Draw the gradient """
        dc = wx.PaintDC(self)
#        w, h = self.mdc.GetSize()
        dc.Blit(0, 0, self.dc_w, self.dc_h, self.mdc, 0, 0)

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
            val = wm_utils.rescale(pos[1],
                                   (self.grad_start_y, self.grad_end_y - 1),
                                   self.plot_range)
            a = self.mdc.GetPixelPoint(event.GetPosition())
            print("{}\t{}\t{}".format(pos, a, val))

    def get_color(self, value):
        """
        Gets a color from the gradient
        """
        pxl = int(wm_utils.rescale(value,
                                   self.plot_range,
                                   (self.grad_start_y, self.grad_end_y - 1)))
        point = (0, pxl)
        color = self.mdc.GetPixelPoint(point)
        return color

    def calc_ticks(self):
        """
        Calculates the tick marks' display string, value, and pixel value.
        """
        # First we need to determine the values for the ticks.
        pr = self.plot_range[1] - self.plot_range[0]
        spacing = pr / (self.num_ticks - 1)

        tick_values = wm_utils.frange(self.plot_range[0],
                                      self.plot_range[1] + 1,
                                      spacing)

        ticks = []
        for tick in tick_values:
            string = "{:.3f}".format(tick)
            value = tick,
            pixel = wm_utils.rescale(tick,
                                     self.plot_range,
                                     (self.grad_start_y, self.grad_end_y - 1))
            ticks.append((string, value, pixel))

        return ticks

    def print_ticks(self, ticks):
        """
        prints the tickmarks. ticks is a list of (string, value, pixel) tuples
        """
        pen = wx.Pen(wx.BLACK)
        self.mdc.SetPen(pen)
        text_w = max([self.mdc.GetTextExtent(_i[0])[0] for _i in ticks])
        for tick in ticks:
            # Sorry, everything is measured from right to left...
            tick_end = self.grad_start_x - self.spacer
            tick_start = tick_end - self.tick_w
            self.mdc.DrawLine(tick_start, tick[2],
                              tick_end, tick[2])

            # Text origin is top left of bounding box.
            # Text is currently left-aligned. Maybe Change?
            text_x = tick_start - self.spacer - text_w
            text_y = tick[2] - self.text_h / 2
            self.mdc.DrawText(tick[0], text_x, text_y)

    def draw_gradient(self):
        """ Draws the Gradient """
        self.mdc.GradientFillLinear((self.grad_start_x, self.grad_start_y,
                                     self.grad_w, self.grad_h),
                                    wx.BLACK,
                                    wx.YELLOW,
                                    wx.SOUTH,
                                    )

    def get_max_text_w(self, ticks):
        """ Get the maximum label sizes. There's probably a better way... """
        return max([self.mdc.GetTextExtent(i[0])[0] for i in ticks])


# DON'T TOUCH! It's working.
class ContinuousLegend_save(wx.Panel):
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
        self.fgs = wx.FlexGridSizer(rows=self.n_items, cols=2, vgap=0, hgap=2)

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
                              size=(300 + 16, 550 + 38),    # Size in px
                              )

            self.Bind(wx.EVT_CLOSE, self.OnQuit)

            # Here's where we call the WaferMapPanel
            self.hbox = wx.BoxSizer(wx.HORIZONTAL)

            self.d_legend = DiscreteLegend(self, legend_labels, legend_colors)
            self.c_legend = ContinuousLegend(self, (10, 50))

            self.hbox.Add(self.d_legend, 0)
            self.hbox.Add(self.c_legend, 0)
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
