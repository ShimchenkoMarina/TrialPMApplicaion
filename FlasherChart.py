import wx
from Device import Device


class FlasherChart(wx.Panel):
    devices = []

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id, size=(parent.GetSize()))
        self.parent = parent
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def AddDevice(self, device, x, y, width, height):
        self.devices.append((device, x, y, width, height))

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        for device in self.devices:
            dc.SetBrush(wx.Brush(device[0].states[-1].color, wx.SOLID))
            dc.DrawRectangle(device[1], device[2], device[3], device[4])

        self.Layout()


