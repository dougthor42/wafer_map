# -*- coding: utf-8 -*-
"""
@name:          wafer_map.py
@vers:          0.2.0
@author:        dthor
@created:       Tue Nov 11 15:08:43 2014
@descr:         A new file

Usage:
    wafer_map.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.

Changelog:

* 2014-12-01: 0.3.0   Added kb shortcuts and menu items for display toggle
                      of wafer outline and crosshairs. Added placeholder
                      for legend and kb shortcut for display toggle.
                      Added option for plotting discrete data.
* 2014-11-26: 0.2.0   Made it so a wafer map can be plotted with a single
                      command. Updated example.py to demo this.
* 2014-11-25: 0.1.0   First working code. Added example file.
* 2014-11-25: 0.0.1   Project Creation
"""

from __future__ import print_function, division, absolute_import
#from __future__ import unicode_literals
import math
import numpy as np
import wx
from wx.lib.floatcanvas import FloatCanvas


# Module-level TODO list.
# TODO: make variables "private" (prepend underscore)
# TODO: Add legend to Panel - should not be included in bounding box.


# Library Constants
# Defined by SEMI M1-0302
FLAT_LENGTHS = {50: 15.88, 75: 22.22, 100: 32.5, 125: 42.5, 150: 57.5}

__author__ = "Douglas Thor"
__version__ = "v0.3.0"


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


# TODO: Move this to a separate module?
class WaferMapApp(object):
    """
    A self-contained Window for a Wafer Map.
    """
    def __init__(self,
                 xyd,
                 die_size,
                 center_xy=(0, 0),
                 dia=150,
                 edge_excl=5,
                 flat_excl=5,
                 ):
        app = wx.App()
        self.wafer_info = WaferInfo(die_size,
                                    (0, 0),
                                    dia,
                                    edge_excl,
                                    flat_excl,
                                    )
        self.xyd = xyd
        frame = WaferMapWindow("Wafer Map", self.xyd, self.wafer_info)
        frame.Show()
        app.MainLoop()


# TODO: Move this to a separate module?
class WaferMapWindow(wx.Frame):
    """
    This is the main window of the application. It contains the WaferMapPanel
    and the MenuBar.

    Although technically I don't need to have only 1 panel in the MainWindow,
    I can have multiple panels. But I think I'll stick with this for now.
    """
    def __init__(self,
                 title,
                 xyd,
                 wafer_info,
                 size=(800, 800),
                 ):
        wx.Frame.__init__(self,
                          None,
                          wx.ID_ANY,
                          title=title,
                          size=size,
                          )
        self.xyd = xyd
        self.wafer_info = wafer_info
        self.init_ui()

    def init_ui(self):
     
        
        # Create menu bar
        self.menu_bar = wx.MenuBar()

        self._create_menus()
        self._create_menu_items()
        self._add_menu_items()
        self._add_menus()
        self._bind_events()
        
        # Initialize default states
        self.mv_outline.Check()
        self.mv_crosshairs.Check()
        self.mv_legend.Check()

        # Set the MenuBar and create a status bar (easy thanks to wx.Frame)
        self.SetMenuBar(self.menu_bar)
        self.CreateStatusBar()

        self.panel = WaferMapPanel(self,
                                   self.xyd,
                                   self.wafer_info)   

    # TODO: There's gotta be a more scalable way to make menu items
    #       and bind events... I'll run out of names if I have too many items.
    #       If I use numbers, as displayed in wxPython Demo, then things
    #       become confusing if I want to reorder things.
    def _create_menus(self):
        """ Create each menu for the menu bar """
        self.mfile = wx.Menu()
        self.medit = wx.Menu()
        self.mview = wx.Menu()
        self.mopts = wx.Menu()

    def _create_menu_items(self):
        """ Create each item for each menu """
#        self.mf_new = wx.MenuItem(self.mfile, wx.ID_ANY, "&New\tCtrl+N", "TestItem")
#        self.mf_open = wx.MenuItem(self.mfile, wx.ID_ANY, "&Open\tCtrl+O", "TestItem")
        self.mf_close = wx.MenuItem(self.mfile, wx.ID_ANY, "&Close\tCtrl+Q", "TestItem")

        self.me_redraw = wx.MenuItem(self.medit, wx.ID_ANY, "&Redraw", "Force Redraw")
#        self.me_test1 = wx.MenuItem(self.medit, wx.ID_ANY, "&Test1", "Test Menu1")
#        self.me_test2 = wx.MenuItem(self.medit, wx.ID_ANY, "&Test2", "Test Menu2")

        self.mv_zoomfit = wx.MenuItem(self.mview, wx.ID_ANY, "Zoom &Fit\tHome", "Zoom to fit")
        self.mv_crosshairs = wx.MenuItem(self.mview, wx.ID_ANY, "Crosshairs\tC", "Show or hide the crosshairs", wx.ITEM_CHECK)
        self.mv_outline = wx.MenuItem(self.mview, wx.ID_ANY, "Wafer Outline\tO", "Show or hide the wafer outline", wx.ITEM_CHECK)
        self.mv_legend = wx.MenuItem(self.mview, wx.ID_ANY, "Legend\tL", "Show or hide the legend", wx.ITEM_CHECK)

        self.mo_test = wx.MenuItem(self.mopts, wx.ID_ANY, "&Test", "Nothing")

    def _add_menu_items(self):
        """ Appends MenuItems to each menu """
#        self.mfile.AppendItem(self.mf_new)
#        self.mfile.AppendItem(self.mf_open)
        self.mfile.AppendItem(self.mf_close)

        self.medit.AppendItem(self.me_redraw)
#        self.medit.AppendItem(self.me_test1)
#        self.medit.AppendItem(self.me_test2)

        self.mview.AppendItem(self.mv_zoomfit)
        self.mview.AppendItem(self.mv_crosshairs)
        self.mview.AppendItem(self.mv_outline)
        self.mview.AppendItem(self.mv_legend)

        self.mopts.AppendItem(self.mo_test)

    def _add_menus(self):
        """ Appends each menu to the menu bar """
        self.menu_bar.Append(self.mfile, "&File")
        self.menu_bar.Append(self.medit, "&Edit")
        self.menu_bar.Append(self.mview, "&View")
        self.menu_bar.Append(self.mopts, "&Options")

    def _bind_events(self):
        """ Binds events to varoius MenuItems """
        self.Bind(wx.EVT_MENU, self.on_quit, self.mf_close)
        self.Bind(wx.EVT_MENU, self.zoom_fit, self.mv_zoomfit)
        self.Bind(wx.EVT_MENU, self.toggle_crosshairs, self.mv_crosshairs)
        self.Bind(wx.EVT_MENU, self.toggle_outline, self.mv_outline)
        self.Bind(wx.EVT_MENU, self.toggle_legend, self.mv_legend)

        # If I define an ID to the menu item, then I can use that instead of
        #   and event source:
        #self.mo_test = wx.MenuItem(self.mopts, 402, "&Test", "Nothing")
        #self.Bind(wx.EVT_MENU, self.zoom_fit, id=402)

    def on_quit(self, event):
        self.Close(True)

    # TODO: I don't think I need a separate method for this
    def zoom_fit(self, event):
        print("Frame Event!")
        self.panel.zoom_fill()

    # TODO: I don't think I need a separate method for this
    def toggle_crosshairs(self, event):
        self.panel.toggle_crosshairs()

    # TODO: I don't think I need a separate method for this
    def toggle_outline(self, event):
        self.panel.toggle_outline()

    # TODO: I don't think I need a separate method for this
    #       However if I don't use these then I have to 
    #           1) instance self.panel at the start of __init__
    #           2) make it so that self.panel.toggle_legend accepts the event arg
    def toggle_legend(self, event):
        self.panel.toggle_legend()


# TODO: figure out how to handle discrete data vs continuous data
# TODO: figure out how to handle row-col coords data vs absolute xy coords
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
        self.xyd = xyd
        self.wafer_info = wafer_info
        self.drag = False
        self.wfr_outline_bool = True
        self.crosshairs_bool = True
        self.legend_bool = True
        self.data_type = data_type
        self.coord_type = coord_type

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
        color_dict = None
        # if discrete data, generate a list of colors
        # TODO: I'm sure there's a lib for this already...
        if self.data_type == 'discrete':
            unique_items = {_die[2] for _die in self.xyd}
            color_dict = {_i: (255*_n/len(unique_items), 0, 0)
                          for _n, _i
                          in enumerate(unique_items)}

        for die in self.xyd:
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
                                     self.wafer_info.die_size,
                                     LineWidth=1,
                                     FillColor=color,
                                     )

        # Add the wafer outline and crosshairs (or center dot)
        self.wafer_outline = draw_wafer_outline(self.wafer_info.dia,
                                                self.wafer_info.edge_excl,
                                                self.wafer_info.flat_excl)
        self.canvas.AddObject(self.wafer_outline)
        self.crosshairs = draw_crosshairs(self.wafer_info.dia)
        self.canvas.AddObject(self.crosshairs)

        self.legend = Legend("Legend Placeholder",
                             (20, 20),
                             Size=18,
                             Color="Black",
                             BackgroundColor='Pink',
                             )
                                      
        self.canvas.GridOver = self.legend

        # Bind events to the canvas
        # TODO: Move event binding to method
        self.canvas.Bind(FloatCanvas.EVT_MOTION, self.mouse_move)
        self.canvas.Bind(FloatCanvas.EVT_MOUSEWHEEL, self.mouse_wheel)
        self.canvas.Bind(FloatCanvas.EVT_MIDDLE_DOWN, self.mouse_middle_down)
        self.canvas.Bind(FloatCanvas.EVT_MIDDLE_UP, self.mouse_middle_up)
        self.canvas.Bind(wx.EVT_LEFT_DOWN, self.mouse_left_down)
        self.canvas.Bind(wx.EVT_LEFT_UP, self.mouse_left_up)
        # note that key-down is bound again - this allows hotkeys to work
        # even if the main Frame, which defines hotkeys in menus, is not
        # present. wx sents the EVT_KEY_DOWN up the chain and, if the Frame
        # and hotkeys are present, executes those instead.
        # At least I think that's how that works...
        # See http://wxpython.org/Phoenix/docs/html/events_overview.html
        # for more info.
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
        die_coord_x = int(event.Coords[0] // self.wafer_info.die_size[0]) + 24
        # Since FloatCanvas uses Lower-Left as origin, we need to
        # adjust y-coords. Nuts.
        # TODO: Adjust displayed coord to account for the fact that the
        #   die center is the origin of the die. Right now, if you're on the
        #   left of the die you get X=23 and the right gives X=24
        die_coord_y = 20 - int(event.Coords[1] // self.wafer_info.die_size[1])
        status_str = "{x:0.3f}, {y:0.3f} :: x{die_x:03d}, y{die_y:03d}"
        try:
            parent.SetStatusText(status_str.format(x=event.Coords[0],
                                                   y=event.Coords[1],
                                                   die_x=die_coord_x,
                                                   die_y=die_coord_y))
        except:
            pass

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
        """
#        pass
        print("panel event!")
        key = event.GetKeyCode()
        print("KeyCode: {}".format(key))
        if key == wx.WXK_HOME:
            self.zoom_fill()
        if key == 79:               # "O"
            self.toggle_outline()
        if key == 67:               # "C"
            self.toggle_crosshairs()
        if key == 76:               # "L"
            self.toggle_legend()

    def zoom_fill(self):
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
            self.canvas.GridOver = None
            self.legend_bool = False
        else:
            self.canvas.GridOver = self.legend
            self.legend_bool = True
        self.canvas.Draw()

    def mouse_left_down(self, event):
        """
        Start making the zoom-to-box box.
        """
        print("Left mouse down!")

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
        string = """{}mm wafer with {}mm edge exclusion and \
{}mm flat exclusion. Die Size = {}"""
        return string.format(self.dia,
                             self.edge_excl,
                             self.flat_excl,
                             self.die_size)


class Legend(FloatCanvas.Text):
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

    # if an exclusion is defined: create it and add to group
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
    return group


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


# TODO: Finish this function
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
