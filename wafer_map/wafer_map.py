# -*- coding: utf-8 -*-
"""
@name:          wafer_map.py
@vers:          0.1.0
@author:        dthor
@created:       Tue Nov 11 15:08:43 2014
@descr:         A new file

Usage:
    wafer_map.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.

Changelog:
    2014-11-25: 0.1.0   Removed code used for testing - was moved to
                        example.py.
"""

from __future__ import print_function, division, absolute_import
#from __future__ import unicode_literals
import math
import numpy as np
import wx
import wx.lib.mixins.inspection
from wx.lib.floatcanvas import FloatCanvas

# Library Constants
# Defined by SEMI M1-0302
FLAT_LENGTHS = {50: 15.88, 75: 22.22, 100: 32.5, 125: 42.5, 150: 57.5}

__author__ = "Douglas Thor"
__version__ = "v0.1.0"


def rescale(x, (original_min, original_max), (new_min, new_max)=(0, 1)):
    """
    Rescales x (which was part of scale original_min to original_max)
    to run over a range new_min to new_max such
    that the value x maintains position on the new scale new_min to new_max.
    If x is outside of xRange, then y will be outside of yRange.

    Default new scale range is 0 to 1 inclusive.

    Examples:
    rescale(5, (10, 20), (0, 1)) = -0.5
    rescale(27, (0, 200), (0, 5)) = 0.675
    rescale(1.5, (0, 1), (0, 10)) = 15.0
    """
    part_a = x * (new_max - new_min)
    part_b = original_min * new_max - original_max * new_min
    denominator = original_max - original_min
    result = (part_a - part_b)/denominator
    return result


class WaferMap(wx.Panel):
    """
    The Canvas that the wafer map resides on
    """
    def __init__(self, parent, rcd, wafer_info=None):
        wx.Panel.__init__(self, parent)
        self.rcd = rcd
        self.wafer_info = wafer_info
        self.drag = False

        # timer to give a delay when moving so that buffers aren't
        # re-built too many times.
        self.move_timer = wx.PyTimer(self.on_move_timer)
        self.init_ui()

    def init_ui(self):
        """
        Creates the UI Elements for the wafer map and binds various events
        such as mouse wheel change (zoom) and left-click+drag (pan).
        """
        # Create items to add to our layout
        self.canvas = FloatCanvas.FloatCanvas(self,
#                                              ProjectionFun=YDownProjection,
                                              BackgroundColor="BLACK",
                                              )

        # Create layout manager and add items
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        self.vbox.Add(self.canvas, 4, wx.EXPAND | wx.ALL)
#        self.vbox.Add(self.MsgWindow, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.vbox)

        self.coord = (0, 0)
        self.size = (30, 30)

        # Work on the canvas
        self.canvas.InitAll()       # Needs to come before adding items!

        # Add the die
        # TODO: Change rcd to instance var
        color_dict = {0: (255, 0, 0),
                      1: (0, 255, 0),
                      2: (0, 0, 255),
                      }
        color_dict = None

        for die in self.rcd:
            if color_dict is None:
                color1 = max(50, min(rescale(die[2],
                                             (0, (self.wafer_info.dia / 2)**2),
                                             (0, 255)
                                             ),
                                     255)
                             )
                # black to yellow
                color = (color1, color1, 0)
            else:
                color = color_dict[die[2]]
            self.canvas.AddRectangle((die[0], die[1]),
                                     # TODO: Change die_size to instance var
                                     self.wafer_info.die_size,
                                     LineWidth=1,
                                     FillColor=color,
                                     )

        # Add the wafer outline
        wafer_outline = draw_wafer_outline(self.wafer_info.dia,
                                           self.wafer_info.edge_excl,
                                           self.wafer_info.flat_excl)
        self.canvas.AddObject(wafer_outline)

        # Bind events to the canvas
        self.canvas.Bind(FloatCanvas.EVT_MOTION, self.mouse_move)
        self.canvas.Bind(FloatCanvas.EVT_MOUSEWHEEL, self.mouse_wheel)
        self.canvas.Bind(FloatCanvas.EVT_MIDDLE_DOWN, self.mouse_middle_down)
        self.canvas.Bind(FloatCanvas.EVT_MIDDLE_UP, self.mouse_middle_up)
        self.canvas.Bind(wx.EVT_LEFT_DOWN, self.mouse_left_down)
        self.canvas.Bind(wx.EVT_LEFT_UP, self.mouse_left_up)
        self.canvas.Bind(wx.EVT_KEY_DOWN, self.key_down)

        # Zoom to the entire image by default
        # TODO: Figure out why this isn't working on init.
        self.zoom_fill()

    def mouse_wheel(self, event):
        """ Mouse wheel event for Zooming """
        # Get the event position and how far the wheel moved
#        point = event.Position
        speed = event.GetWheelRotation()

        # calculate a zoom factor based on the wheel movement
        #   Allows for zoom acceleration: fast wheel move = large zoom.
        #   factor < 0: zoom out. factor > 0: zoom in
        sign = abs(speed) / speed
        factor = (abs(speed) * 1.1 / 120)**sign
#        print("MouseMove! {}: {}".format(event.GetWheelRotation(), factor))

        self.canvas.Zoom(factor,
                         center=event.Position,
                         centerCoords="pixel",
                         keepPointInPlace=True,
                         )

    def on_move_timer(self, event=None):
        """
        Redraw the canvas whenever the move_timer is triggered. Is needed to
        prevent buffers from being rebuilt too often
        """
#        print("3s later?")
#        self.canvas.MoveImage(self.diff_loc, 'Pixel', ReDraw=True)
        self.canvas.Draw()

    def mouse_move(self, event):
        """
        Updates the status bar with the world coordinates
        """
        # display the mouse coords on the Frame StatusBar
        parent = wx.GetTopLevelParent(self)
        # TODO: Change die_size to instance var
        die_coord_x = int(event.Coords[0] // self.wafer_info.die_size[0]) + 24
        # Since FloatCanvas uses Lower-Left as origin, we need to
        # adjust y-coords. Nuts.
        # TODO: Change die_size to instance var
        # TODO: Adjust displayed coord to account for the fact that the
        #   die center is the origin of the die. Right now, if you're on the
        #   left of the die you get X=23 and the right gives X=24
        die_coord_y = 20 - int(event.Coords[1] // self.wafer_info.die_size[1])
        status_str = "{x:0.3f}, {y:0.3f} :: x{die_x:03d}, y{die_y:03d}"
        parent.SetStatusText(status_str.format(x=event.Coords[0],
                                               y=event.Coords[1],
                                               die_x=die_coord_x,
                                               die_y=die_coord_y))

        # If we're dragging, actually move the image.
        if self.drag:
            self.end_move_loc = np.array(event.GetPosition())
#            self.MoveImage(event)
            self.diff_loc = self.mid_move_loc - self.end_move_loc
            self.canvas.MoveImage(self.diff_loc, 'Pixel', ReDraw=True)
#            self.MoveImageDoug()
            self.mid_move_loc = self.end_move_loc

            # doesn't appear to do anything...
            self.move_timer.Start(30, oneShot=True)

    def mouse_middle_down(self, event):
        self.drag = True

        # Update various positions
        self.start_move_loc = np.array(event.GetPosition())
        self.mid_move_loc = self.start_move_loc
        self.prev_move_loc = (0, 0)
        self.end_move_loc = None

        # Change the cursor to a drag cursor
        self.SetCursor(wx.StockCursor(wx.CURSOR_SIZING))

    def mouse_middle_up(self, event):
        self.drag = False

        # update various positions
        if self.start_move_loc is not None:
            self.end_move_loc = np.array(event.GetPosition())
            self.diff_loc = self.mid_move_loc - self.end_move_loc
            self.canvas.MoveImage(self.diff_loc, 'Pixel', ReDraw=True)

        # change the cursor back to normal
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))

    def key_down(self, event):
        """
        Event Handler for Keyboard Shortcuts:
            HOME:   Zoom to fill window
            other keys:    none yet
        """
        key = event.GetKeyCode()
        if key == wx.WXK_HOME:
            print("home pressed!")
            self.zoom_fill()

    def zoom_fill(self):
        self.canvas.ZoomToBB()

    def mouse_left_down(self, event):
        """
        Start making the zoom-to-box box.
        """
        pass

    def mouse_left_up(self, event):
        """
        End making the zoom-to-box box and execute the zoom.
        """
        pass

#    def mouse_right_down(self, event):
#        """
#        Start making the zoom-out box.
#        """
#        pass
#
#    def mouse_right_up(self, event):
#        """
#        Stop making the zoom-out box and execute the zoom
#        """
#        pass

    def MoveImageDoug(self):
        """ actually move the image? """
        self.move_timer.Start(300, oneShot=True)
#        self.canvas.MoveImage(self.diff_loc, 'Pixel', ReDraw=True)

    def MoveImage(self, event):
        """
        This is taken from the FloatCanvas.GUIMode module
        and is *supposed* to reduce flicker, but doesn't seem to. Perhpas I
        have something else wrong.
        """
        #xy1 = N.array( event.GetPosition() )
        xy1 = self.end_move_loc
        wh = self.canvas.PanelSize
        xy_tl = xy1 - self.start_move_loc
        dc = wx.ClientDC(self.canvas)
        dc.BeginDrawing()
        x1, y1 = self.prev_move_loc
        x2, y2 = xy_tl
        w, h = self.canvas.PanelSize
        ##fixme: This sure could be cleaner!
        ##   This is all to fill in the background with the background color
        ##   without flashing as the image moves.
        if x2 > x1 and y2 > y1:
            xa = xb = x1
            ya = yb = y1
            wa = w
            ha = y2 - y1
            wb = x2 - x1
            hb = h
        elif x2 > x1 and y2 <= y1:
            xa = x1
            ya = y1
            wa = x2 - x1
            ha = h
            xb = x1
            yb = y2 + h
            wb = w
            hb = y1 - y2
        elif x2 <= x1 and y2 > y1:
            xa = x1
            ya = y1
            wa = w
            ha = y2 - y1
            xb = x2 + w
            yb = y1
            wb = x1 - x2
            hb = h - y2 + y1
        elif x2 <= x1 and y2 <= y1:
            xa = x2 + w
            ya = y1
            wa = x1 - x2
            ha = h
            xb = x1
            yb = y2 + h
            wb = w
            hb = y1 - y2

        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(self.canvas.BackgroundBrush)
        dc.DrawRectangle(xa, ya, wa, ha)
        dc.DrawRectangle(xb, yb, wb, hb)
        self.prev_move_loc = xy_tl
        if self.canvas._ForeDrawList:
            dc.DrawBitmapPoint(self.canvas._ForegroundBuffer, xy_tl)
        else:
            dc.DrawBitmapPoint(self.canvas._Buffer, xy_tl)
        dc.EndDrawing()
        #self.Canvas.Update()


class WaferInfo(object):
    """
    Contains the wafer info:
    Die Size
    Center XY
    Wafer Diameter
    Edge Exclusion
    Flat Exclusion
    """
    def __init__(self, die_size, center_xy, dia=150, edge_excl=5, flat_excl=5):
        self.die_size = die_size
        self.center_xy = center_xy
        self.dia = dia
        self.edge_excl = edge_excl
        self.flat_excl = flat_excl

    def __str__(self):
        string = "{}mm wafer with {}mm edge exclusion. Die Size = {}"
        return string.format(self.dia, self.edge_excl, self.die_size)


def draw_wafer_outline(dia=150, excl=5, flat=5):
    """
    Draws a wafer outline for a given radius, including any edge exclusion
    lines.

    Returns a FloatCanvas.Group object that can be added to any
    FloatCanvas.FloatCanvas instance.

    :dia:   Wafer diameter in mm
    :excl:  Wafer edge exclusion in mm. Defaults to None (no edge excl.)
    :flat:  Flat edge exclusion. Defaults to the same as excl.
    """
    # Defined by SEMI M1-0302
    FLAT_LENGTHS = {50: 15.88, 75: 22.22, 100: 32.5, 125: 42.5, 150: 57.5}

    rad = float(dia)/2.0

    if flat == 0:
        flat = excl

    # TODO: There's a lot of duplicate code here. I should try and change that.
    if dia in FLAT_LENGTHS:
        # A flat is defined, so we draw it.
        flat_size = FLAT_LENGTHS[dia]
        x = flat_size/2
        y = -math.sqrt(rad**2 - x**2)

        arc = FloatCanvas.Arc((x, y),
                              (-x, y),
                              (0, 0),
                              LineColor=wx.RED,
                              LineWidth=3,
                              )

        # actually a wafer flat, but called notch
        notch = draw_wafer_flat(rad, FLAT_LENGTHS[dia])
    else:
        # Flat not defined, so use a notch to denote wafer orientation.
        ang = 2.5
        ang_rad = ang * math.pi / 180

        start_xy = (rad * math.sin(ang_rad), -rad * math.cos(ang_rad))
        end_xy = (-rad * math.sin(ang_rad), -rad * math.cos(ang_rad))

        arc = FloatCanvas.Arc(start_xy,
                              end_xy,
                              (0, 0),
                              LineColor=wx.RED,
                              LineWidth=3,
                              )

        notch = draw_wafer_notch(rad)

    # Group the outline arc and the orientation (flat / notch) together
    group = FloatCanvas.Group([arc, notch])

    if excl != 0:
        exclRad = 0.5 * (dia - 2.0 * excl)

        if dia in FLAT_LENGTHS:
            # Define the arc angle based on the flat exclusion, not the edge
            # exclusion. Find the flat exclusion X and Y coords.
            FSSflatY = y + flat
            FSSflatX = math.sqrt(exclRad**2 - FSSflatY**2)

            # Define the wafer arc
            excl_arc = FloatCanvas.Arc((FSSflatX, FSSflatY),
                                       (-FSSflatX, FSSflatY),
                                       (0, 0),
                                       LineColor=wx.RED,
                                       LineWidth=3,
                                       )

            excl_notch = draw_wafer_flat(exclRad, FSSflatX * 2)

        else:
            # Flat not defined, so use a notch to denote wafer orientation.
            ang = 2.5
            ang_rad = ang * math.pi / 180

            start_xy = (exclRad * math.sin(ang_rad),
                        -exclRad * math.cos(ang_rad))
            end_xy = (-exclRad * math.sin(ang_rad),
                      -exclRad * math.cos(ang_rad))

            excl_arc = FloatCanvas.Arc(start_xy,
                                       end_xy,
                                       (0, 0),
                                       LineColor=wx.RED,
                                       LineWidth=3,
                                       )

            excl_notch = draw_wafer_notch(exclRad)
        group = FloatCanvas.Group([arc, notch, excl_arc, excl_notch])

    # Add dot for center of wafer
    # replaced by crosshairs
#    circ = FloatCanvas.Circle((0, 0),
#                              2.5,
#                              FillColor=wx.RED,
#                              )

    # Add crosshairs
    xline = FloatCanvas.Line([(rad * 1.05, 0), (-rad * 1.05, 0)],
                             LineColor=wx.CYAN,
                             )
    yline = FloatCanvas.Line([(0, rad * 1.05), (0, -rad * 1.05)],
                             LineColor=wx.CYAN,
                             )

    return FloatCanvas.Group([group, xline, yline])


def draw_wafer_flat(rad, flat_length):
    """ Draws a wafer flat for a given radius and flat length """
    x = flat_length/2
    y = -math.sqrt(rad**2 - x**2)

    flat = FloatCanvas.Line([(-x, y), (x, y)],
                            LineColor=wx.RED,
                            LineWidth=3,
                            )
    return flat


def draw_excl_flat(rad, flat_y, line_width=1, line_color='black'):
    """ Draws a wafer flat for a given radius and flat length """
    flat_x = math.sqrt(rad**2 - flat_y**2)

    flat = FloatCanvas.Line([(-flat_x, flat_y), (flat_x, flat_y)],
                            LineColor=wx.RED,
                            LineWidth=3,
                            )
    return flat


def draw_wafer_notch(rad):
    """ Draws a wafer notch for a given wafer radius"""
    ang = 2.5
    ang_rad = ang * math.pi / 180

    # Define the Notch as a series of 3 (x, y) points
    xy_points = [(-rad * math.sin(ang_rad), -rad * math.cos(ang_rad)),
                 (0, -rad*0.95),
                 (rad * math.sin(ang_rad), -rad * math.cos(ang_rad))]

    notch = FloatCanvas.Line(xy_points,
                             LineColor=wx.RED,
                             LineWidth=2,
                             )
    return notch


def plot_wafer_map_wx(rcd, **kwargs):
                   #wafer=(150, 5, 4.5),
                   #die_xy=(2.43, 3.3),
                   #center_rc=(24, 31.5),
                   #plot_range=(10, 20)),
                   #wafer_outline=True,
                   #exclusion_outline=True,
                   #color_dict={0: (0, 0, 0),
                   #            1: (0, 0, 0),
                   #            2: (0, 0, 0)}
    """
    Plots a wafer map with outline and edge exclusion, with die color defined
    by the die data value.

    Same as plot_wafer_map but uses wxPython.

    Req'd Inputs:
    rcd: list of tuples of (row_coord, col_coord, value)

    Optional Inputs (must be named):
    wafer: tuple of wafer info: (diameter, edge_exclusion, flat_exclusion)
    die_xy: tuple of (die_x, die_y) sizes
    center_rc: tuple of (center_row, center_col)
    plot_range: tuple of (min, max) plot values
    color_dict: dictionary of {value: color} that overrides default plot colors
    """

    DEFAULT_KWARGS = {'wafer': (150, 5, 4.5),
                      'die_xy': (2.43, 3.3),
                      'center_rc': (24, 31.5),
                      'plot_range': (0, 1),
                      'draw_wfr': True,
                      'draw_excl': True,
                      'color_dict': None}

    # parse the keyword arguements, asigning defaults if not found.
    for key in DEFAULT_KWARGS:
        if key not in kwargs:
            kwargs[key] = DEFAULT_KWARGS[key]

    wafer = kwargs['wafer']
    die_xy = kwargs['die_xy']
    center_rc = kwargs['center_rc']
    plot_range = kwargs['plot_range']
    draw_wfr = kwargs['draw_wfr']
    draw_excl = kwargs['draw_excl']
    color_dict = kwargs['color_dict']

    if color_dict is None:
        # use black to yellow
        color1 = max(0, min(rescale(data[2], (plot_range), (0, 1)), 1))
        color = (color1, color1, 0)
    else:
        color = color_dict[data[2]]


def main():
    """ Main Code """
    pass


if __name__ == "__main__":
    main()
