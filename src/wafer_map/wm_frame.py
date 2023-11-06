# -*- coding: utf-8 -*-
# pylint: disable=E1101
#   E1101 = Module X has no Y member
"""
This is the main window of the Wafer Map application.
"""
# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
from __future__ import absolute_import, division, print_function, unicode_literals

# Third-Party
import wx

# Package / Application
from . import wm_core
from . import wm_constants as wm_const


class WaferMapWindow(wx.Frame):
    """
    This is the main window of the application.

    It contains the WaferMapPanel and the MenuBar.

    Although technically I don't need to have only 1 panel in the MainWindow,
    I can have multiple panels. But I think I'll stick with this for now.

    Parameters
    ----------
    title : str
        The title to display.
    xyd : list of 3-tuples
        The data to plot.
    wafer_info : :class:`wx_info.WaferInfo`
        The wafer information.
    size : tuple, optional
        The windows size in ``(width, height)``. Values must be ``int``s.
        Defaults to ``(800, 600)``.
    data_type : wm_constants.DataType or string, optional
        The type of data to plot. Must be one of `continuous` or `discrete`.
        Defaults to `continuous`.
    high_color : :class:`wx.Colour`, optional
        The color to display if a value is above the plot range. Defaults
        to `wm_constants.wm_HIGH_COLOR`.
    low_color : :class:`wx.Colour`, optional
        The color to display if a value is below the plot range. Defaults
        to `wm_constants.wm_LOW_COLOR`.
    plot_range : tuple, optional
        The plot range to display. If ``None``, then auto-ranges. Defaults
        to auto-ranging.
    plot_die_centers : bool, optional
        If ``True``, display small red circles denoting the die centers.
        Defaults to ``False``.
    show_die_gridlines : bool, optional
        If ``True``, displayes gridlines along the die edges. Defaults to
        ``True``.
    """

    def __init__(self,
                 title,
                 xyd,
                 wafer_info,
                 size=(800, 600),
                 data_type=wm_const.DataType.CONTINUOUS,
                 high_color=wm_const.wm_HIGH_COLOR,
                 low_color=wm_const.wm_LOW_COLOR,
                 plot_range=None,
                 plot_die_centers=False,
                 show_die_gridlines=True,
                 ):
        wx.Frame.__init__(self,
                          None,
                          wx.ID_ANY,
                          title=title,
                          size=size,
                          )
        self.xyd = xyd
        self.wafer_info = wafer_info
        # backwards compatability
        if isinstance(data_type, str):
            data_type = wm_const.DataType(data_type)
        self.data_type = data_type
        self.high_color = high_color
        self.low_color = low_color
        self.plot_range = plot_range
        self.plot_die_centers = plot_die_centers
        self.show_die_gridlines = show_die_gridlines
        self._init_ui()

    def _init_ui(self):
        """Init the UI components."""
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
        self.mv_diecenters.Check(self.plot_die_centers)
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
                                               show_die_gridlines=self.show_die_gridlines,
                                               )

    # TODO: There's gotta be a more scalable way to make menu items
    #       and bind events... I'll run out of names if I have too many items.
    #       If I use numbers, as displayed in wxPython Demo, then things
    #       become confusing if I want to reorder things.
    def _create_menus(self):
        """Create each menu for the menu bar."""
        self.mfile = wx.Menu()
        self.medit = wx.Menu()
        self.mview = wx.Menu()
        self.mopts = wx.Menu()

    def _create_menu_items(self):
        """Create each item for each menu."""
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
        self.mv_diecenters = wx.MenuItem(self.mview,
                                      wx.ID_ANY,
                                      "Die Centers\tD",
                                      "Show or hide the die centers",
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
        """Append MenuItems to each menu."""
#        self.mfile.Append(self.mf_new)
#        self.mfile.Append(self.mf_open)
        self.mfile.Append(self.mf_close)

        self.medit.Append(self.me_redraw)
#        self.medit.Append(self.me_test1)
#        self.medit.Append(self.me_test2)

        self.mview.Append(self.mv_zoomfit)
        self.mview.AppendSeparator()
        self.mview.Append(self.mv_crosshairs)
        self.mview.Append(self.mv_outline)
        self.mview.Append(self.mv_diecenters)
        self.mview.Append(self.mv_legend)

        self.mopts.Append(self.mo_test)
        self.mopts.Append(self.mo_high_color)
        self.mopts.Append(self.mo_low_color)

    def _add_menus(self):
        """Append each menu to the menu bar."""
        self.menu_bar.Append(self.mfile, "&File")
        self.menu_bar.Append(self.medit, "&Edit")
        self.menu_bar.Append(self.mview, "&View")
        self.menu_bar.Append(self.mopts, "&Options")

    def _bind_events(self):
        """Bind events to varoius MenuItems."""
        self.Bind(wx.EVT_MENU, self.on_quit, self.mf_close)
        self.Bind(wx.EVT_MENU, self.on_zoom_fit, self.mv_zoomfit)
        self.Bind(wx.EVT_MENU, self.on_toggle_crosshairs, self.mv_crosshairs)
        self.Bind(wx.EVT_MENU, self.on_toggle_diecenters, self.mv_diecenters)
        self.Bind(wx.EVT_MENU, self.on_toggle_outline, self.mv_outline)
        self.Bind(wx.EVT_MENU, self.on_toggle_legend, self.mv_legend)
        self.Bind(wx.EVT_MENU, self.on_change_high_color, self.mo_high_color)
        self.Bind(wx.EVT_MENU, self.on_change_low_color, self.mo_low_color)

        # If I define an ID to the menu item, then I can use that instead of
        #   and event source:
        #self.mo_test = wx.MenuItem(self.mopts, 402, "&Test", "Nothing")
        #self.Bind(wx.EVT_MENU, self.on_zoom_fit, id=402)

    def on_quit(self, event):
        """Action for the quit event."""
        self.Close(True)

    # TODO: I don't think I need a separate method for this
    def on_zoom_fit(self, event):
        """Call :meth:`wafer_map.wm_core.WaferMapPanel.zoom_fill()`."""
        print("Frame Event!")
        self.panel.zoom_fill()

    # TODO: I don't think I need a separate method for this
    def on_toggle_crosshairs(self, event):
        """Call :meth:`wafer_map.wm_core.WaferMapPanel.toggle_crosshairs()`."""
        self.panel.toggle_crosshairs()

    # TODO: I don't think I need a separate method for this
    def on_toggle_diecenters(self, event):
        """Call :meth:`wafer_map.wm_core.WaferMapPanel.toggle_crosshairs()`."""
        self.panel.toggle_die_centers()

    # TODO: I don't think I need a separate method for this
    def on_toggle_outline(self, event):
        """Call the WaferMapPanel.toggle_outline() method."""
        self.panel.toggle_outline()

    # TODO: I don't think I need a separate method for this
    #       However if I don't use these then I have to
    #           1) instance self.panel at the start of __init__
    #           2) make it so that self.panel.toggle_legend accepts arg: event
    def on_toggle_legend(self, event):
        """Call the WaferMapPanel.toggle_legend() method."""
        self.panel.toggle_legend()

    # TODO: See the 'and' in the docstring? Means I need a separate method!
    def on_change_high_color(self, event):
        """Change the high color and refresh display."""
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

    # TODO: See the 'and' in the docstring? Means I need a separate method!
    def on_change_low_color(self, event):
        """Change the low color and refresh display."""
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
    """Run when called as a module."""
    app = wx.App()
    frame = WaferMapWindow("Testing", [], None)
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
