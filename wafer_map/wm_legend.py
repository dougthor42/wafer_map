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
import wx
from wx.lib.floatcanvas import FloatCanvas
import wx.lib.colourselect as csel
import colorsys

# check to see if we can import from the dev folder, otherwise import
# from the standard install folder, site-packages
if 'site-packages' in __file__:
    from wafer_map import wm_utils
    from wafer_map.wm_constants import *
else:
    print("Running wm_legend from Development Location")
    import wm_utils
    from wm_constants import *

# TODO: Update to Bezier Curves for colors. See http://bsou.io/p/3


class Legend(object):
    """
    Base class for both discrete and continuous legends.

    Not currently used. Not even sure if I will use it.
    """
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
    def __init__(self,
                 parent,
                 plot_range,
                 high_color=wm_HIGH_COLOR,
                 low_color=wm_LOW_COLOR,
                 num_ticks=wm_TICK_COUNT,
                 oor_high_color=wm_OOR_HIGH_COLOR,
                 oor_low_color=wm_OOR_LOW_COLOR,
                 ):
        """
        __init__(self,
                 wx.Panel parent,
                 tuple plot_range,
                 color tuple high_color=(255, 255, 255),
                 color tuple low_color=(0, 0, 0),
                 int num_ticks=11,
                 ) -> wx.Panel
        """
        wx.Panel.__init__(self, parent)

        ###==================================================================
        ### Inputs
        ###==================================================================
        self.parent = parent
        self.plot_range = plot_range
        self.high_color = high_color
        self.low_color = low_color
        self.num_ticks = num_ticks
        self.oor_high_color = oor_high_color
        self.oor_low_color = oor_low_color
        self.invalid_color = wm_INVALID_COLOR

        ###==================================================================
        ### Initialize Size Attributes
        ###==================================================================
        # These get set in set_sizes(), but are here to remind me that
        # the instance attribute exists and what they are.
        # Values are in px.
        self.text_h = None          # text height
        self.text_w = None          # Length of longest tick label
        self.grad_w = None          # gradient width
        self.grad_h = None          # gradient height
        self.spacer = None          # spacer speration between items
        self.grad_start_y = None    # top of gradient pixel coord
        self.grad_end_y = None      # bottom of gradient pixel coord
        self.grad_start_x = None    # gradient left pixel coord
        self.grad_end_x = None      # gradient right pixel coord
        self.tick_w = None          # tick mark length
        self.tick_start_x = None    # tick label left pixel coord
        self.dc_w = None            # total bitmap width
        self.dc_h = None            # total bitmap height

        ###==================================================================
        ### Other Instance Attributes
        ###==================================================================
        self.ticks = None
        self.gradient = wm_utils.LinearGradient(self.low_color,
                                                self.high_color)

        ###==================================================================
        ### Remainder of __init__
        ###==================================================================
        # Create the MemoryDC now - we'll add the bitmap later.
        self.mdc = wx.MemoryDC()
        self.mdc.SetFont(wx.Font(9,
                                 wx.FONTFAMILY_SWISS,
                                 wx.FONTSTYLE_NORMAL,
                                 wx.FONTWEIGHT_NORMAL,
                                 ))

        self.set_sizes()

        # Create EmptyBitmap in our MemoryDC where we'll do all our drawing.
        self.mdc.SelectObject(wx.EmptyBitmap(self.dc_w, self.dc_h))

        # Draw the entire thing
        self.draw_scale()

        # Bind various events
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
#        self.Bind(wx.EVT_MOTION, self.mouse_move)
        self.Bind(wx.EVT_LEFT_DOWN, self.left_click)
        self.Bind(wx.EVT_RIGHT_DOWN, self.right_click)

        self.init_ui()

    def init_ui(self):
        """
        Add a Sizer that is the same size as the MemoryDC
        """
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox.Add((self.dc_w, self.dc_h))
        self.SetSizer(self.hbox)

    def on_size(self, event):
        """ Redraw everything with the new sizes. """
        # TODO: Also reduce number of ticks when text starts to overlap
        #       or add ticks when there's extra space.
        self.set_sizes()
        self.hbox.Remove(0)
        self.hbox.Add((self.dc_w, self.dc_h))
        self.mdc.SelectObject(wx.EmptyBitmap(self.dc_w, self.dc_h))
        self.draw_scale()
        self.Refresh()

    def on_paint(self, event):
        """ Push the MemoryDC bitmap to the displayed PaintDC """
        dc = wx.PaintDC(self)
        dc.Blit(0, 0, self.dc_w, self.dc_h, self.mdc, 0, 0)

    def mouse_move(self, event):
        """ Used for debugging """
        pt = self.mdc.GetPixelPoint(event.GetPosition())
        print(pt)

    def left_click(self, event):
        """ Used for debugging """
        print("Left-click - color from self.mdc.GetPixelPoint.")
        pos = event.GetPosition()
        w, h = self.mdc.GetSize()       # change to gradient area
        if pos[0] < w and pos[1] < h:
            val = wm_utils.rescale(pos[1],
                                   (self.grad_start_y, self.grad_end_y - 1),
                                   reversed(self.plot_range))
            a = self.mdc.GetPixelPoint(event.GetPosition())
            print("{}\t{}\t{}".format(pos, a, val))

    def right_click(self, event):
        """ Used for debugging """
        print("Right-click - color from get_color()")
        pos = event.GetPosition()
        w, h = self.mdc.GetSize()       # change to gradient area
        if pos[0] < w and pos[1] < h:
            val = wm_utils.rescale(pos[1],
                                   (self.grad_start_y, self.grad_end_y - 1),
                                   reversed(self.plot_range))
            a = self.get_color(val)
            print("{}\t{}\t{}".format(pos, a, val))

    def mouse_wheel(self, event):
        print("mouse wheel!")
#        self.left_click(event)

    def on_color_change(self, event):
        """
        Change the plot colors by updating self.gradient and by calling
        self.draw_scale()
        """
        if event['low'] is not None:
            self.low_color = event['low']
        if event['high'] is not None:
            self.high_color = event['high']
        self.gradient = wm_utils.LinearGradient(self.low_color,
                                                self.high_color)

#        self._clear_scale()
        self.hbox.Remove(0)
        self.hbox.Add((self.dc_w, self.dc_h))
        self.mdc.SelectObject(wx.EmptyBitmap(self.dc_w, self.dc_h))

        self.draw_scale()

    def get_color(self, value):
        """
        Gets a color from the gradient.
        """
        # TODO: determine how wxPython's GradientFillLinear works and use that
        # instead of grabbing the color from the gradient.
        if value > self.plot_range[1]:
            color = self.oor_high_color
        elif value < self.plot_range[0]:
            color = self.oor_low_color
        else:
            try:
#                pxl = int(wm_utils.rescale(value,
#                                           self.plot_range,
#                                           (self.grad_end_y - 1,
#                                            self.grad_start_y)))
#
#                x_pt = self.grad_w // 2 + self.grad_start_x
#                point = (x_pt, pxl)
#                color = self.mdc.GetPixelPoint(point)
            
                # New Method
                pxl = wm_utils.rescale(value,
                                       self.plot_range,
                                       (0, 1))
                color = self.gradient.get_color(pxl)
#                color = wm_utils.linear_gradient(self.low_color,
#                                                 self.high_color,
#                                                 pxl)
                color = wx.Colour(*color)
            except ValueError:
                color = self.invalid_color
        return color

    def calc_ticks(self):
        """
        Calculates the tick marks' display string, value, and pixel value.

        High values are at the top of the scale, low at the bottom.
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
            value = tick
            # `grad_end_y - 1` so that the bottom tick is aligned correctly.
            pixel = wm_utils.rescale(tick,
                                     self.plot_range,
                                     (self.grad_end_y - 1, self.grad_start_y))
            # Putting gradient_end_y as the "low" for rescale makes the
            # high value be at the north end and the low value at the south.
            ticks.append((string, value, pixel))

        return ticks

    def draw_ticks(self, ticks):
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

    def set_sizes(self):
        """
        Sets various instance attributes for item sizes and locations.
        """
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
#        self.grad_h = 500           # total gradient height (px)
        self.grad_h = self.parent.GetClientSize()[1] - self.text_h
        self.tick_w = 20            # tick mark length
        self.spacer = 5             # spacer speration between items
        self.grad_start_y = self.text_h / 2
        self.grad_end_y = self.grad_start_y + self.grad_h

        # Now that the widths are defined, I can calculate some other things
        self.ticks = self.calc_ticks()
        self.text_w = self.get_max_text_w(self.ticks)

        # Note: I'm intentionally listing every spacer manually rather than
        #       multiplying by how many there are. This makes it easier
        #       to see where I'm placing them.
        self.tick_start_x = self.spacer + self.text_w + self.spacer
        self.grad_start_x = self.tick_start_x + self.tick_w + self.spacer
        self.grad_end_x = self.grad_start_x + self.grad_w
        self.dc_w = self.grad_end_x + self.spacer   # total bitmap width
        self.dc_h = self.grad_h + self.text_h       # total bitmap height

    def draw_background(self):
        """
        Draws the background box. If I don't do this, then the background is
        black.

        Could I change wx.EmptyBitmap() so that it defaults to white rather
        than black?
        """
        # TODO: change the bitmap background to be transparent
        c = wx.Colour(200, 230, 230, 0)
        c = wx.Colour(255, 255, 255, 0)
        pen = wx.Pen(c)
        brush = wx.Brush(c)
        self.mdc.SetPen(pen)
        self.mdc.SetBrush(brush)
        self.mdc.DrawRectangle(0, 0, self.dc_w, self.dc_h)

    def draw_scale(self):
        """
        Draws the entire scale area: background, gradient, OOR colors,
        ticks, and labels.
        """
        self.draw_background()

        # Draw the Gradient on a portion of the MemoryDC
        self.draw_gradient()

        # Draw the out-of-range high and low rectangles
        c = self.oor_high_color
        pen = wx.Pen(c)
        brush = wx.Brush(c)
        self.mdc.SetPen(pen)
        self.mdc.SetBrush(brush)
        self.mdc.DrawRectangle(self.grad_start_x,
                               2,
                               self.grad_w,
                               self.grad_start_y - 2)

        c = self.oor_low_color
        pen = wx.Pen(c)
        brush = wx.Brush(c)
        self.mdc.SetPen(pen)
        self.mdc.SetBrush(brush)
        self.mdc.DrawRectangle(self.grad_start_x,
                               self.grad_end_y,
                               self.grad_w,
                               self.dc_h - self.grad_end_y - 2)



        # Calculate and draw the tickmarks.
        self.draw_ticks(self.ticks)

    def draw_gradient(self):
        """ Draws the Gradient, painted from North (high) to South (low) """
#        self.mdc.GradientFillLinear((self.grad_start_x, self.grad_start_y,
#                                     self.grad_w, self.grad_h),
#                                    self.high_color,
#                                    self.low_color,
#                                    wx.SOUTH,
#                                    )

        # Remake of the wx.DC.GradientFillLinear wx core function, but uses
        # my own algorithm for determining the colors.
        # Doing so ensures that both the gradient and the die colors match.

        # Save the old pen colors
        old_pen = self.mdc.GetPen()
        old_brush = self.mdc.GetBrush()
        delta = self.grad_h / 255           # height of one shade box
        if delta < 1:
            delta = 1       # max of 255 pts - fractional colors not defined.

        y = self.grad_start_y
        while y <= self.grad_end_y:
            val = wm_utils.rescale(y,
                                   (self.grad_start_y, self.grad_end_y),
                                   (1, 0))
            color = self.gradient.get_color(val)
#            color = wm_utils.linear_gradient(self.low_color,
#                                             self.high_color,
#                                             val)
            self.mdc.SetPen(wx.Pen(color))
            self.mdc.SetBrush(wx.Brush(color))
            self.mdc.DrawRectangle(self.grad_start_x,
                                   y,
                                   self.grad_w, delta + 1)
            y += delta

        # Set the pen and brush back to what they were
        self.mdc.SetPen(old_pen)
        self.mdc.SetBrush(old_brush)

    def get_max_text_w(self, ticks):
        """ Get the maximum label sizes. There's probably a better way... """
        return max([self.mdc.GetTextExtent(i[0])[0] for i in ticks])


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
                 colors=None,
                 ):
        """
        __init__(self, wx.Panel parent, list labels, list colors) -> wx.Panel
        """
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.labels = labels
        self.n_items = len(self.labels)
        if colors is None:
            self.colors = self.create_colors(self.n_items)
        else:
            self.colors = colors
        self.create_color_dict()

        self.init_ui()

    def init_ui(self):

        # Add layout management
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.fgs = wx.FlexGridSizer(rows=self.n_items, cols=2, vgap=0, hgap=2)

        # Create items to add
        for _i, (key, value) in enumerate(zip(self.labels, self.colors)):
            self.label = wx.StaticText(self,
                                       label=str(key),
                                       style=wx.ALIGN_LEFT,
                                       )

            self.colorbox = csel.ColourSelect(self,
                                              _i,
                                              "",
                                              tuple(value),
                                              style=wx.NO_BORDER,
                                              size=(20, 20))

            self.Bind(csel.EVT_COLOURSELECT, self.on_color_pick, id=_i)

            self.fgs.Add(self.label, flag=wx.ALIGN_CENTER_VERTICAL)
            self.fgs.Add(self.colorbox)

        # Add our items to the layout manager and set the sizer.
        self.hbox.Add(self.fgs)
        self.SetSizer(self.hbox)

    def create_colors(self, n):
        """
        Create the colors based on how many legend items there are (n).

        The idea is to start off with one color, assign it to the 1st legend
        value, then find that color's complement and assign it to the 2nd
        legend value. Then, move around the color wheel by some degree,
        probably like so:

          <insert math>

        We are limited to only using 1/2 of the circle
        because we use the other half for the complements.

        1.  Split the circle into n parts.
        2.  reorganize into alternations
            1 2 3 4 5 6 7 8  -->
            1 3 5 7 2 4 6 8
        """
        spacing = 360 / n
        colors = []
        for val in wm_utils.frange(0, 360, spacing):
            hsl = (val/360, 1, 0.75)
            colors.append(colorsys.hsv_to_rgb(*hsl))

        # convert from 0-1 to 0-255 and return
        colors = [tuple(int(i*255) for i in color) for color in colors]

        # Alternate colors across the circle
        colors = colors[::2] + colors[1::2]
        return colors

    def create_color_dict(self):
        """
        Takes the value and color lists and creates a dict from them.

        This may eventually become a public function with two inputs:
        lables, colors.
        """
        # TODO: Determine if I want this to be a public callable method
        self.color_dict = dict(zip(self.labels, self.colors))
        return self.color_dict

    def on_color_pick(self, event):
        """
        Recreate the label: color dictionary and send the event to the
        parent panel.
        """
        print(event.GetId())
        self.colors[event.GetId()] = event.GetValue().Get()
        self.create_color_dict()
        # Send the event to the parent:
        wx.PostEvent(self.parent, event)


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
#    legend_labels = [str(_i) for _i in range(10)]

    legend_colors = None

    continuous_range = (10, 50)

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
            self.c_legend = ContinuousLegend(self, continuous_range)

            self.hbox.Add(self.d_legend, 0)
            self.hbox.Add(self.c_legend, 0)
            self.SetSizer(self.hbox)

        def OnQuit(self, event):
            self.Destroy()

    app = wx.App()
    frame = ExampleFrame("Legend Example")
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
