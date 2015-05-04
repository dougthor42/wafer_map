# -*- coding: utf-8 -*-
"""
@name:          wafer_map.py
@vers:          1.0.0
@author:        dthor
@created:       Tue Nov 11 15:08:43 2014
@descr:         A new file

Usage:
    wafer_map.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.

Changelog
=========

See README.rst

"""

from __future__ import print_function, division#, absolute_import
#from __future__ import unicode_literals
import math
import numpy as np
import wx
from wx.lib.floatcanvas import FloatCanvas
import wx.lib.colourselect as csel

import wafer_map.wm_legend as wm_legend
import wafer_map.wm_utils as wm_utils
import wafer_map.wm_constants as wm_const

# Module-level TODO list.
# TODO: make variables "private" (prepend underscore)
# TODO: Add function to update wafer map with new die size and the like.


class WaferMapPanel(wx.Panel):
    """
    The Canvas that the wafer map resides on.

    Usage: WaferMap(parent, xyd, wafer_info)
        xyd :: List of (x_coord, y_coord, data) tuples

        wafer_info :: instance of the WaferInfo class
    """
    def __init__(self,
                 parent,
                 xyd,
                 wafer_info,
                 data_type='continuous',
                 coord_type='absolute',
                 high_color=wm_const.wm_HIGH_COLOR,
                 low_color=wm_const.wm_LOW_COLOR,
                 plot_range=None,
                 plot_die_centers=False,
                 discrete_legend_values=None,
                 ):
        """
        __init__(self,
                 parent_panel,
                 [(x, y, data), ...] xyd,
                 WaferInfo wafer_info,
                 string data_type='continuous',
                 string coord_type='absolute',
                 ) -> wx.Panel
        """
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.xyd = xyd
        self.xyd_dict = self.xyd_to_dict(self.xyd)      # data duplication!
        self.wafer_info = wafer_info
        self.grid_center = self.wafer_info.center_xy
        self.die_size = self.wafer_info.die_size

        self.drag = False
        self.wfr_outline_bool = True
        self.crosshairs_bool = True
        self.legend_bool = True
        self.data_type = data_type
        self.coord_type = coord_type
        self.high_color = high_color
        self.low_color = low_color
        self.plot_range = plot_range
        self.plot_die_centers = plot_die_centers
        self.discrete_legend_values = discrete_legend_values

        # timer to give a delay when moving so that buffers aren't
        # re-built too many times.
        # TODO: Convert PyTimer to Timer and wx.EVT_TIMER. See wxPytho demo.
        self.move_timer = wx.PyTimer(self.on_move_timer)
        self.init_ui()

    def xyd_to_dict(self, xyd_list):
        """ Converts the xyd list to a dict of xNNyNN key-value pairs """
        return {"x{}y{}".format(_x, _y): _d for _x, _y, _d in xyd_list}

    def init_ui(self):
        """
        Creates the UI Elements for the wafer map and binds various events
        such as mouse wheel change (zoom) and left-click+drag (pan).
        """
        # Create items to add to our layout
        self.canvas = FloatCanvas.FloatCanvas(self,
                                              BackgroundColor="BLACK",
                                              )

        # Initialize the FloatCanvas. Needs to come before adding items!
        self.canvas.InitAll()

        # Create the legend
        self._create_legend()

        # Draw the die and wafer objects (outline, crosshairs) on the canvas
        self.draw_die()
        if self.plot_die_centers:
            self.draw_die_center()
        self.draw_wafer_objects()

        # Bind events to the canvas
        self._bind_events()

        # Create layout manager and add items
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.hbox.Add(self.legend, 0, wx.EXPAND)
        self.hbox.Add(self.canvas, 1, wx.EXPAND)

        self.SetSizer(self.hbox)

    def _bind_events(self):
        """
        Bind panel and canvas events.

        Note that key-down is bound again - this allws hotkeys to work
        even if the main Frame, which defines hotkeys in menus, is not
        present. wx sents the EVT_KEY_DOWN up the chain and, if the Frame
        and hotkeys are present, executes those instead.
        At least I think that's how that works...
        See http://wxpython.org/Phoenix/docs/html/events_overview.html
        for more info.
        """
        # Canvas Events
        self.canvas.Bind(FloatCanvas.EVT_MOTION, self.mouse_move)
        self.canvas.Bind(FloatCanvas.EVT_MOUSEWHEEL, self.mouse_wheel)
        self.canvas.Bind(FloatCanvas.EVT_MIDDLE_DOWN, self.mouse_middle_down)
        self.canvas.Bind(FloatCanvas.EVT_MIDDLE_UP, self.mouse_middle_up)
        self.canvas.Bind(wx.EVT_PAINT, self.on_first_paint)
        # XXX: Binding the EVT_LEFT_DOWN seems to cause Issue #24.
        #      What seems to happen is: If I bind EVT_LEFT_DOWN, then the
        #      parent panel or application can't set focus to this
        #      panel, which prevents the EVT_MOUSEWHEEL event from firing
        #      properly.
#        self.canvas.Bind(wx.EVT_LEFT_DOWN, self.mouse_left_down)
        self.canvas.Bind(wx.EVT_LEFT_UP, self.mouse_left_up)
        self.canvas.Bind(wx.EVT_KEY_DOWN, self.key_down)

        # Panel Events
        self.Bind(csel.EVT_COLOURSELECT, self.on_color_change)

    def _create_legend(self):
        """
        Create the legend.

        For Continuous data, uses min(data) and max(data) for plot range.

        Might change to 5th percentile and 95th percentile.
        """
        if self.data_type == "discrete":
            if self.discrete_legend_values is None:
                unique_items = list({_die[2] for _die in self.xyd})
            else:
                unique_items = self.discrete_legend_values
            self.legend = wm_legend.DiscreteLegend(self,
                                                   labels=unique_items,
                                                   colors=None,
                                                   )
        else:
            if self.plot_range is None:
                p_98 = float(wm_utils.nanpercentile([_i[2]
                                                    for _i
                                                    in self.xyd], 98))
                p_02 = float(wm_utils.nanpercentile([_i[2]
                                                    for _i
                                                    in self.xyd], 2))

                data_min = min([die[2] for die in self.xyd])
                data_max = max([die[2] for die in self.xyd])
                self.plot_range = (data_min, data_max)
                self.plot_range = (p_02, p_98)

            self.legend = wm_legend.ContinuousLegend(self,
                                                     self.plot_range,
                                                     self.high_color,
                                                     self.low_color,
                                                     )

    def draw_die(self):
        """ Draws and add the die on the canvas """
        color_dict = None
        for die in self.xyd:
            # define the die color
            if self.data_type == 'discrete':
                color_dict = self.legend.color_dict
                color = color_dict[die[2]]
            else:
                color = self.legend.get_color(die[2])

            # Determine the die's lower-left coordinate
            lower_left_coord = wm_utils.grid_to_rect_coord(die[:2],
                                                           self.die_size,
                                                           self.grid_center)

            # Draw the die on the canvas
            self.canvas.AddRectangle(lower_left_coord,
                                     self.die_size,
                                     LineWidth=1,
                                     FillColor=color,
                                     )

    def draw_die_center(self):
        """ Plots the die centers as a small dot """
        for die in self.xyd:
            # Determine the die's lower-left coordinate
            lower_left_coord = wm_utils.grid_to_rect_coord(die[:2],
                                                           self.die_size,
                                                           self.grid_center)

            # then adjust back to the die center
            lower_left_coord = (lower_left_coord[0] + self.die_size[0] / 2,
                                lower_left_coord[1] + self.die_size[1] / 2)

            circ = FloatCanvas.Circle(lower_left_coord,
                                      0.5,
                                      FillColor=wx.RED,
                                      )
            self.canvas.AddObject(circ)

    def draw_wafer_objects(self):
        """
        Draw and Add the various wafer objects
        """
        self.wafer_outline = draw_wafer_outline(self.wafer_info.dia,
                                                self.wafer_info.edge_excl,
                                                self.wafer_info.flat_excl)
        self.canvas.AddObject(self.wafer_outline)
        self.crosshairs = draw_crosshairs(self.wafer_info.dia, dot=False)
        self.canvas.AddObject(self.crosshairs)

    def _clear_canvas(self):
        """ Clears the canvas """
        self.canvas.ClearAll(ResetBB=False)

    def on_color_change(self, event):
        """ Update the wafer map canvas with the new color """
        self._clear_canvas()
        if self.data_type == "continuous":
            # call the continuous legend on_color_change() code
            self.legend.on_color_change(event)
        self.draw_die()
        if self.plot_die_centers:
            self.draw_die_center()
        self.draw_wafer_objects()
        self.canvas.Draw(True)
#        self.canvas.Unbind(FloatCanvas.EVT_MOUSEWHEEL)
#        self.canvas.Bind(FloatCanvas.EVT_MOUSEWHEEL, self.mouse_wheel)

    def on_first_paint(self, event):
        """ Zoom to fill on the first paint event """
        # disable the handler for future paint events
        self.canvas.Bind(wx.EVT_PAINT, None)

        #TODO: Fix a flicker-type event that occurs on this call
        self.zoom_fill()

    def mouse_wheel(self, event):
        """ Mouse wheel event for Zooming """
        speed = event.GetWheelRotation()
        pos = event.GetPosition()
        x, y, w, h = self.canvas.GetClientRect()

        # If the mouse is outside the FloatCanvas area, do nothing
        if pos[0] < 0 or pos[1] < 0 or pos[0] > x + w or pos[1] > y + h:
            return

        # calculate a zoom factor based on the wheel movement
        #   Allows for zoom acceleration: fast wheel move = large zoom.
        #   factor < 0: zoom out. factor > 0: zoom in
        sign = abs(speed) / speed
        factor = (abs(speed) * wm_const.wm_ZOOM_FACTOR)**sign

        self.canvas.Zoom(factor,
                         center=pos,
                         centerCoords="pixel",
#                         center=event.GetCoords(),
#                         centerCoords="world",
                         keepPointInPlace=True,
                         )

    def on_move_timer(self, event=None):
        """
        Redraw the canvas whenever the move_timer is triggered. Is needed to
        prevent buffers from being rebuilt too often
        """
#        self.canvas.MoveImage(self.diff_loc, 'Pixel', ReDraw=True)
        self.canvas.Draw()

    def mouse_move(self, event):
        """
        Updates the status bar with the world coordinates
        """
        # display the mouse coords on the Frame StatusBar
        parent = wx.GetTopLevelParent(self)

        die_coord_x, die_coord_y = wm_utils.coord_to_grid(event.Coords,
                                                          self.die_size,
                                                          self.grid_center,
                                                          )

        # lookup the die value
        die_coord = "x{}y{}".format(die_coord_x, die_coord_y)
        try:
            die_val = self.xyd_dict[die_coord]
        except KeyError:
            die_val = "N/A"

        # create the status bar string
        coord_str = "{x:0.3f}, {y:0.3f}".format(x=event.Coords[0],
                                                y=event.Coords[1],
                                                )
        value_str = "{}".format(die_val)
        status_str = "{coord} :: {loc} :: {val}".format(coord=coord_str,
                                                        loc=die_coord,
                                                        val=value_str,
                                                        )
        try:
            parent.SetStatusText(status_str)
        except:
            pass

        # If we're dragging, actually move the image.
        if self.drag:
            self.end_move_loc = np.array(event.GetPosition())
            self.diff_loc = self.mid_move_loc - self.end_move_loc
            self.canvas.MoveImage(self.diff_loc, 'Pixel', ReDraw=True)
            self.mid_move_loc = self.end_move_loc

            # doesn't appear to do anything...
            self.move_timer.Start(30, oneShot=True)

    def mouse_middle_down(self, event):
        """ Start the drag """
        self.drag = True

        # Update various positions
        self.start_move_loc = np.array(event.GetPosition())
        self.mid_move_loc = self.start_move_loc
        self.prev_move_loc = (0, 0)
        self.end_move_loc = None

        # Change the cursor to a drag cursor
        self.SetCursor(wx.StockCursor(wx.CURSOR_SIZING))

    def mouse_middle_up(self, event):
        """ End the drag """
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
        Event Handler for Keyboard Shortcuts. This is used when the panel
        is integrated into a Frame and the Frame does not define the KB
        Shortcuts already.

        If inside a frame, the wx.EVT_KEY_DOWN event is sent to the toplevel
        Frame which handles the event (if defined).

        At least I think that's how that works...
        See http://wxpython.org/Phoenix/docs/html/events_overview.html
        for more info.

        Shortcuts:
            HOME:   Zoom to fill window
            O:      Toggle wafer outline
            C:      Toggle wafer crosshairs
            L:      Toggle the legend
        """
        # TODO: Decide if I want to move this to a class attribute
        keycodes = {wx.WXK_HOME: self.zoom_fill,      # "Home
                    79: self.toggle_outline,          # "O"
                    67: self.toggle_crosshairs,       # "C"
                    76: self.toggle_legend,           # "L"
                    }

        print("panel event!")
        key = event.GetKeyCode()

        if key in keycodes.keys():
            keycodes[key]()
        else:
            print("KeyCode: {}".format(key))

    def zoom_fill(self):
        """ Zoom so that everything is displayed """
        self.canvas.ZoomToBB()

    def toggle_outline(self):
        """ Toggles the wafer outline and edge exclusion on and off """
        if self.wfr_outline_bool:
            self.canvas.RemoveObject(self.wafer_outline)
            self.wfr_outline_bool = False
        else:
            self.canvas.AddObject(self.wafer_outline)
            self.wfr_outline_bool = True
        self.canvas.Draw()

    def toggle_crosshairs(self):
        """ Toggles the center crosshairs on and off """
        if self.crosshairs_bool:
            self.canvas.RemoveObject(self.crosshairs)
            self.crosshairs_bool = False
        else:
            self.canvas.AddObject(self.crosshairs)
            self.crosshairs_bool = True
        self.canvas.Draw()

    def toggle_legend(self):
        """ Toggles the legend on and off """
        if self.legend_bool:
            self.hbox.RemovePos(0)
            self.Layout()       # forces update of layout
            self.legend_bool = False
        else:
            self.hbox.Insert(0, self.legend, 0)
            self.Layout()
            self.legend_bool = True
        self.canvas.Draw(Force=True)

    def mouse_left_down(self, event):
        """
        Start making the zoom-to-box box.
        """
        print("Left mouse down!")
        # TODO: Look into what I was doing here. Why no 'self' on parent?
        parent = wx.GetTopLevelParent(self)
        wx.PostEvent(self.parent, event)

    def mouse_left_up(self, event):
        """
        End making the zoom-to-box box and execute the zoom.
        """
        print("Left mouse up!")

    def mouse_right_down(self, event):
        """
        Start making the zoom-out box.
        """
        print("Right mouse down!")

    def mouse_right_up(self, event):
        """
        Stop making the zoom-out box and execute the zoom
        """
        print("Right mouse up!")


def draw_wafer_outline(dia=150, excl=5, flat=None):
    """
    Draws a wafer outline for a given radius, including any edge exclusion
    lines.

    Returns a FloatCanvas.Group object that can be added to any
    FloatCanvas.FloatCanvas instance.

    :dia:   Wafer diameter in mm
    :excl:  Wafer edge exclusion in mm. Defaults to None (no edge excl.)
    :flat:  Flat edge exclusion. Defaults to the same as excl.
    """

    rad = float(dia)/2.0
    if flat is None:
        flat = excl

    # Full wafer outline circle
    circ = FloatCanvas.Circle((0, 0),
                              dia,
                              LineColor=wx.YELLOW,
                              LineWidth=1,
                              )

    # Calculate the exclusion Radius
    exclRad = 0.5 * (dia - 2.0 * excl)

    if dia in wm_const.wm_FLAT_LENGTHS:
        # A flat is defined, so we draw it.
        flat_size = wm_const.wm_FLAT_LENGTHS[dia]
        x = flat_size/2
        y = -math.sqrt(rad**2 - x**2)       # Wfr Flat's Y Location

        arc = FloatCanvas.Arc((x, y),
                              (-x, y),
                              (0, 0),
                              LineColor=wx.RED,
                              LineWidth=3,
                              )

        # actually a wafer flat, but called notch
        notch = draw_wafer_flat(rad, wm_const.wm_FLAT_LENGTHS[dia])
        # Define the arc angle based on the flat exclusion, not the edge
        # exclusion. Find the flat exclusion X and Y coords.
        FSSflatY = y + flat
        if exclRad < abs(FSSflatY):
            # Then draw a circle with no flat
            excl_arc = FloatCanvas.Circle((0, 0),
                                          exclRad * 2,
                                          LineColor=wx.RED,
                                          LineWidth=3,
                                          )
            excl_group = FloatCanvas.Group([excl_arc])
        else:
            FSSflatX = math.sqrt(exclRad**2 - FSSflatY**2)

            # Define the wafer arc
            excl_arc = FloatCanvas.Arc((FSSflatX, FSSflatY),
                                       (-FSSflatX, FSSflatY),
                                       (0, 0),
                                       LineColor=wx.RED,
                                       LineWidth=3,
                                       )

            excl_notch = draw_wafer_flat(exclRad, FSSflatX * 2)
            excl_group = FloatCanvas.Group([excl_arc, excl_notch])
    else:
        # Flat not defined, so use a notch to denote wafer orientation.
        ang = 2.5
        start_xy, end_xy = calc_flat_coords(rad, ang)

        arc = FloatCanvas.Arc(start_xy,
                              end_xy,
                              (0, 0),
                              LineColor=wx.RED,
                              LineWidth=3,
                              )

        notch = draw_wafer_notch(rad)
        # Flat not defined, so use a notch to denote wafer orientation.
        start_xy, end_xy = calc_flat_coords(exclRad, ang)

        excl_arc = FloatCanvas.Arc(start_xy,
                                   end_xy,
                                   (0, 0),
                                   LineColor=wx.RED,
                                   LineWidth=3,
                                   )

        excl_notch = draw_wafer_notch(exclRad)
        excl_group = FloatCanvas.Group([excl_arc, excl_notch])

    # Group the outline arc and the orientation (flat / notch) together
    group = FloatCanvas.Group([circ, arc, notch, excl_group])
    return group


def calc_flat_coords(radius, angle):
    """
    Calculates the starting and ending XY coordinates for a horizontal line
    below the y axis that interects a circle of radius ``radius`` and
    makes an angle ``angle`` at the center of the circle.

    This line is below the y axis.

    Parameters:
    -----------
    radius : float
        The radius of the circle that the line intersects.
    angle : float
        The angle, in degrees, that the line spans.

    Returns:
    --------
    (start_xy, end_xy) : tuple of coord pairs
        The starting and ending XY coordinates of the line.
        (start_x, start_y), (end_x, end_y))

    Notes:
    ------
    What follows is a poor-mans schematic. I hope.

    ::

        1-------------------------------------------------------1
        1                                                       1
        1                                                       1
        1                           +                           1
        1                          . .                          1
        1                         .   .                         1
        1                        .     . Radius                 1
         1                      .       .                      1
         1                     .         .                     1
         1                    .           .                    1
          1                  .             .                  1
          1                 .  <--angle-->  .                 1
           1               .                 .               1
            1             .                   .             1
            1            .                     .            1
             1          .                       .          1
              1        .                         .        1
                1     .                           .     1
                 1   .                             .   1
                  1 .                               . 1
                    1-------------line--------------1
                      1                           1
                        1                       1
                           1                  1
                               111111111111
    """
    ang_rad = angle * math.pi / 180
    start_xy = (radius * math.sin(ang_rad), -radius * math.cos(ang_rad))
    end_xy = (-radius * math.sin(ang_rad), -radius * math.cos(ang_rad))
    return (start_xy, end_xy)


def draw_crosshairs(dia=150, dot=False):
    """ Draws the crosshairs or center dot """
    if dot:
        circ = FloatCanvas.Circle((0, 0),
                                  2.5,
                                  FillColor=wx.RED,
                                  )

        return FloatCanvas.Group([circ])
    else:
        # Default: use crosshairs
        rad = dia / 2
        xline = FloatCanvas.Line([(rad * 1.05, 0), (-rad * 1.05, 0)],
                                 LineColor=wx.CYAN,
                                 )
        yline = FloatCanvas.Line([(0, rad * 1.05), (0, -rad * 1.05)],
                                 LineColor=wx.CYAN,
                                 )

        return FloatCanvas.Group([xline, yline])


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


def main():
    """ Main Code """
    raise RuntimeError("This module is not meant to be run by itself.")


if __name__ == "__main__":
    main()
