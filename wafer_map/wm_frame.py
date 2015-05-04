# -*- coding: utf-8 -*-
"""
@name:          wm_frame.py
@vers:          0.1.0
@author:        dthor
@created:       Tue Dec 02 09:30:21 2014
@descr:         This is the main window of the Wafer Map application.

Usage:
    wm_frame.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.
"""

from __future__ import print_function, division#, absolute_import
#from __future__ import unicode_literals
import wx

import wafer_map.wm_core as wm_core
import wafer_map.wm_constants as wm_const


__author__ = "Douglas Thor"
__version__ = "v0.1.0"


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
                 size=(800, 600),
                 data_type='continuous',
                 high_color=wm_const.wm_HIGH_COLOR,
                 low_color=wm_const.wm_LOW_COLOR,
                 plot_range=None,
                 plot_die_centers=False,
                 ):
        """
        __init__(self,
                 string title,
                 list xyd,
                 WaferInfo wafer_info,
                 tuple size=(800, 800),
                 string data_type='continuous',
                 ) -> wx.Frame
        """
        wx.Frame.__init__(self,
                          None,
                          wx.ID_ANY,
                          title=title,
                          size=size,
                          )
        self.xyd = xyd
        self.wafer_info = wafer_info
        self.data_type = data_type
        self.high_color = high_color
        self.low_color = low_color
        self.plot_range = plot_range
        self.plot_die_centers = plot_die_centers
        self.init_ui()

    def init_ui(self):
        """
        Init the UI components.
        """

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

        # Allows this module to be run by itself if needed.
        if __name__ == "__main__":
            self.panel = None
        else:
            self.panel = wm_core.WaferMapPanel(self,
                                               self.xyd,
                                               self.wafer_info,
                                               data_type=self.data_type,
                                               high_color=self.high_color,
                                               low_color=self.low_color,
                                               plot_range=self.plot_range,
                                               plot_die_centers=self.plot_die_centers,
                                               )

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
        ### Menu: File (mf_) ###
#        self.mf_new = wx.MenuItem(self.mfile,
#                                  wx.ID_ANY,
#                                  "&New\tCtrl+N",
#                                  "TestItem")
#        self.mf_open = wx.MenuItem(self.mfile,
#                                   wx.ID_ANY,
#                                   "&Open\tCtrl+O",
#                                   "TestItem")
        self.mf_close = wx.MenuItem(self.mfile,
                                    wx.ID_ANY,
                                    "&Close\tCtrl+Q",
                                    "TestItem",
                                    )

        ### Menu: Edit (me_) ###
        self.me_redraw = wx.MenuItem(self.medit,
                                     wx.ID_ANY,
                                     "&Redraw",
                                     "Force Redraw",
                                     )

        ### Menu: View (mv_) ###
        self.mv_zoomfit = wx.MenuItem(self.mview,
                                      wx.ID_ANY,
                                      "Zoom &Fit\tHome",
                                      "Zoom to fit",
                                      )
        self.mv_crosshairs = wx.MenuItem(self.mview,
                                         wx.ID_ANY,
                                         "Crosshairs\tC",
                                         "Show or hide the crosshairs",
                                         wx.ITEM_CHECK,
                                         )
        self.mv_outline = wx.MenuItem(self.mview,
                                      wx.ID_ANY,
                                      "Wafer Outline\tO",
                                      "Show or hide the wafer outline",
                                      wx.ITEM_CHECK,
                                      )
        self.mv_legend = wx.MenuItem(self.mview,
                                     wx.ID_ANY,
                                     "Legend\tL",
                                     "Show or hide the legend",
                                     wx.ITEM_CHECK,
                                     )

        # Menu: Options (mo_) ###
        self.mo_test = wx.MenuItem(self.mopts,
                                   wx.ID_ANY,
                                   "&Test",
                                   "Nothing",
                                   )
        self.mo_high_color = wx.MenuItem(self.mopts,
                                         wx.ID_ANY,
                                         "Set &High Color",
                                         "Choose the color for high values",
                                         )
        self.mo_low_color = wx.MenuItem(self.mopts,
                                        wx.ID_ANY,
                                        "Set &Low Color",
                                        "Choose the color for low values",
                                        )

    def _add_menu_items(self):
        """ Appends MenuItems to each menu """
#        self.mfile.AppendItem(self.mf_new)
#        self.mfile.AppendItem(self.mf_open)
        self.mfile.AppendItem(self.mf_close)

        self.medit.AppendItem(self.me_redraw)
#        self.medit.AppendItem(self.me_test1)
#        self.medit.AppendItem(self.me_test2)

        self.mview.AppendItem(self.mv_zoomfit)
        self.mview.AppendSeparator()
        self.mview.AppendItem(self.mv_crosshairs)
        self.mview.AppendItem(self.mv_outline)
        self.mview.AppendItem(self.mv_legend)

        self.mopts.AppendItem(self.mo_test)
        self.mopts.AppendItem(self.mo_high_color)
        self.mopts.AppendItem(self.mo_low_color)

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
        self.Bind(wx.EVT_MENU, self.change_high_color, self.mo_high_color)
        self.Bind(wx.EVT_MENU, self.change_low_color, self.mo_low_color)

        # If I define an ID to the menu item, then I can use that instead of
        #   and event source:
        #self.mo_test = wx.MenuItem(self.mopts, 402, "&Test", "Nothing")
        #self.Bind(wx.EVT_MENU, self.zoom_fit, id=402)

    def on_quit(self, event):
        """ Actions for the quit event """
        self.Close(True)

    # TODO: I don't think I need a separate method for this
    def zoom_fit(self, event):
        """ Call the WaferMapPanel.zoom_fill() method """
        print("Frame Event!")
        self.panel.zoom_fill()

    # TODO: I don't think I need a separate method for this
    def toggle_crosshairs(self, event):
        """ Call the WaferMapPanel toggle_crosshairs() method """
        self.panel.toggle_crosshairs()

    # TODO: I don't think I need a separate method for this
    def toggle_outline(self, event):
        """ Call the WaferMapPanel.toggle_outline() method """
        self.panel.toggle_outline()

    # TODO: I don't think I need a separate method for this
    #       However if I don't use these then I have to
    #           1) instance self.panel at the start of __init__
    #           2) make it so that self.panel.toggle_legend accepts arg: event
    def toggle_legend(self, event):
        """ Call the WaferMapPanel.toggle_legend() method """
        self.panel.toggle_legend()

    def change_high_color(self, event):
        print("High color menu item clicked!")
        cd = wx.ColourDialog(self)
        cd.GetColourData().SetChooseFull(True)

        if cd.ShowModal() == wx.ID_OK:
            new_color = cd.GetColourData().Colour
            print("The color {} was chosen!".format(new_color))
            self.panel.on_color_change({'high': new_color, 'low': None})
            self.panel.Refresh()
        else:
            print("no color chosen :-(")
        cd.Destroy()

    def change_low_color(self, event):
        print("Low Color menu item clicked!")
        cd = wx.ColourDialog(self)
        cd.GetColourData().SetChooseFull(True)

        if cd.ShowModal() == wx.ID_OK:
            new_color = cd.GetColourData().Colour
            print("The color {} was chosen!".format(new_color))
            self.panel.on_color_change({'high': None, 'low': new_color})
            self.panel.Refresh()
        else:
            print("no color chosen :-(")
        cd.Destroy()


def main():
    """ Display just the window frame """
    app = wx.App()
    frame = WaferMapWindow("Testing", [], None)
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
