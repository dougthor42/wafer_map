# -*- coding: utf-8 -*-
"""
Test file that hopefully demonstrates the issue wherein the
colourselect.EVT_COLOURSELECT event messes with the
FloatCanvas.EVT_MOUSEWHEEL event.

See http://stackoverflow.com/questions/27413232/wx-lib-evt-colourselect-interfering-with-wx-lib-floatcanvas-evt-mousewheel
"""

from __future__ import print_function, division, absolute_import
#from __future__ import unicode_literals
#from docopt import docopt
import wx
from wx.lib.floatcanvas import FloatCanvas
import wx.lib.colourselect as csel


class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title='test')
        self.panel = MainPanel(self)
        self.Bind(wx.EVT_CLOSE, self.on_quit)

    def on_quit(self, event):
        self.Destroy()


class Legend(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        for _i in xrange(6):
            self.colorbox = csel.ColourSelect(self,
                                              _i,
                                              "",
                                              (0, 0, 0),
                                              style=wx.NO_BORDER,
                                              size=(20, 20),
                                              )

            self.Bind(csel.EVT_COLOURSELECT, self.on_color_pick, id=_i)
            self.vbox.Add(self.colorbox)
        self.SetSizer(self.vbox)

    def on_color_pick(self, event):
        event_id = event.GetId()
        print("A color was picked for box #{}!".format(event_id))
        wx.PostEvent(self.parent, event)


class MainPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.legend = Legend(self)

        self.canvas = FloatCanvas.FloatCanvas(self,
                                              BackgroundColor="BLUE")
        self.canvas.InitAll()

        self.Bind(FloatCanvas.EVT_MOUSEWHEEL, self.mouse_wheel)
        self.Bind(csel.EVT_COLOURSELECT, self.on_color_change)

        # Create layout manager and add items
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.hbox.Add(self.legend, 0)
        self.hbox.Add(self.canvas, 1, wx.EXPAND)

        self.SetSizer(self.hbox)

    def mouse_wheel(self, event):
        print("mousewheel {}".format(event.GetWheelRotation()))

    def _clear_canvas(self):
        """ Clears the canvas """
        self.canvas.ClearAll(ResetBB=False)

    def on_color_change(self, event):
        print("color change event")
        self._clear_canvas()
#        self.draw_die()
#        self.draw_wafer_objects()
        self.canvas.Draw(True)


def main():
    """ Main Code """
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
