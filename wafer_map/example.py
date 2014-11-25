# -*- coding: utf-8 -*-
"""
@name:          example.py
@vers:          0.1.0
@author:        dthor
@created:       Tue Nov 25 13:13:33 2014
@descr:         A new file

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
import wafer_map
import math

__author__ = "Douglas Thor"
__version__ = "v0.1.0"


# Library Constants
# Defined by SEMI M1-0302
FLAT_LENGTHS = {50: 15.88, 75: 22.22, 100: 32.5, 125: 42.5, 150: 57.5}


class WaferMapApp(wx.App):
    """ Main App for WaferMap """
    def OnInit(self):
        frame = MainWindow("Wafer Map")
        frame.Show()
        self.SetTopWindow(frame)
        return True


class MainWindow(wx.Frame):
    """
    This is the main window of the application. It contains the MainPanel
    and the MenuBar.

    Although technically I don't need to have only 1 panel in the MainWindow,
    I can have multiple panels. But I think I'll stick with this for now.
    """
    def __init__(self, title, size=(800, 800)):
        wx.Frame.__init__(self,
                          None,
                          wx.ID_ANY,
                          title=title,
                          size=size,
                          )
        self.init_ui()

    def init_ui(self):
        # Create menu bar
        self.menu_bar = wx.MenuBar()

        # Create the menu items and bind the events
        self.file_menu = wx.Menu()

        self.menu_item = self.file_menu.Append(wx.ID_ANY,
                                               text="Redraw",
                                               help="Force Redraw",
                                               )
#        self.Bind(wx.EVT_MENU, self.redraw, self.menu_item)

        self.menu_item = self.file_menu.Append(wx.ID_ANY,
                                               text="&Close",
                                               help="Close this frame",
                                               )
        self.Bind(wx.EVT_MENU, self.on_quit, self.menu_item)

        # Add our menu items to the menu bar
        self.menu_bar.Append(self.file_menu, "&File")

        # Set the MenuBar and create a status bar (easy thanks to wx.Frame)
        self.SetMenuBar(self.menu_bar)
        self.CreateStatusBar()

        self.panel = MainPanel(self)
#        self.Show(True)

    def on_quit(self, event):
        self.Close(True)


class MainPanel(wx.Panel):
    """
    This is the main panel of the application. It contains all other panels
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.init_ui()

    def init_ui(self):
        """ Create the UI """
        # Add layout management
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)

        # Create Items
        self.wafer_map_panel = WaferMapPanel(self)

        # Add items to layout
        self.hbox.Add(self.wafer_map_panel, 1, wx.EXPAND)
        self.SetSizer(self.hbox)


class WaferMapPanel(wx.Panel):
    """
    Contains the wafer map
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.init_ui()

    def init_ui(self):
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.wafer_info, self.rcd = generate_fake_data()
        self.wafer_map = wafer_map.WaferMap(self, self.rcd, self.wafer_info)
        self.hbox.Add(self.wafer_map, 1, wx.EXPAND)
        self.SetSizer(self.hbox)


def max_dist_sqrd(center, size):
    """
    Calcualtes the largest distance from the origin for a rectangle of
    size (x, y), where the center of the rectangle's coordinates are known.
    If the rectangle's center is in the Q1, then the upper-right corner is
    the farthest away from the origin. If in Q2, then the upper-left corner
    is farthest away. Etc.
    Returns the magnitude of the largest distance squared.
    Does not include the Sqrt function for sake of speed.
    """
    half_x = size[0]/2.
    half_y = size[1]/2.
    if center[0] < 0:
        half_x = -half_x
    if center[1] < 0:
        half_y = -half_y
    dist = (center[0] + half_x)**2 + (center[1] + half_y)**2
    return dist


def generate_fake_data():
    """
    Generate a fake wafer map, where the die values are the die's
    radius squared.
    """
    # Generate random wafer attributes
    import random
    die_x = random.uniform(2, 10)
    die_y = random.uniform(2, 10)
    dia = random.choice([100, 150, 200, 210])
    die_size = (die_x, die_y)
    edge_excl = random.choice([0, 2.5, 5, 10])
    flat_excl = random.choice([0, 2.5, 5, 10])

    # put all the wafer info into the WaferInfo class.
    wafer_info = wafer_map.WaferInfo(die_size,      # Die Size in (X, Y)
                                     (0, 0),        # Center Coord (X, Y)
                                     dia,           # Wafer Diameter
                                     edge_excl,     # Edge Exclusion
                                     flat_excl,     # Flat Exclusion
                                     )
    print(wafer_info)

    xyd = []            # our list of (x_coord, x_coord, data) tuples

    # Create a temp wafer map for testing
    # Note that this assumes the center of the wafer lies in the die streets

    # Determine where our wafer edge is for the flat area
    flat_y = -dia/2     # assume wafer edge at first
    if dia in FLAT_LENGTHS:
        # A flat is defined by SEMI M1-0302, so we calcualte where it is
        flat_y = -math.sqrt((dia/2)**2 - (FLAT_LENGTHS[dia] * 0.5)**2)

    nX = int(math.ceil(dia/die_x))
    nY = int(math.ceil(dia/die_y))
    for i in xrange(nX):
        for j in xrange(nY):
            # die center coordinates
            x_coord = (i - nX//2) * die_x
            y_coord = (j - nY//2) * die_y
            max_dist = max_dist_sqrd((x_coord, y_coord), (die_size))

            # if we're off the wafer, don't add the die
            if max_dist > (dia/2)**2 or y_coord - die_y/2 < flat_y:
                continue
            else:
                r_squared = (x_coord**2 + y_coord**2)
                # wxPython and FloatCanvas use lower-left corner as
                # rectangle origin so we need to adjust
                xyd.append((x_coord - die_x / 2,
                            y_coord - die_y / 2,
                            r_squared))

    print("Number of Die Plotted: {}".format(len(xyd)))

    return (wafer_info, xyd)


def main():
    """ Main Code """
    app = WaferMapApp()
    app.MainLoop()

if __name__ == "__main__":
    main()
