from Device import Device, DeviceState
import wx.lib.scrolledpanel as scrolled

import wx

class GanttChart(scrolled.ScrolledPanel):
    def __init__(self, parent, id):
        # create a panel

        scrolled.ScrolledPanel.__init__(self, parent, -1)#, size=(parent.GetSize()))
        self.Layout()
        self.SetupScrolling()
        self.set_scale(50)

        self.Bind(wx.EVT_SIZE, self.on_parent_resize)
        self.SetBackgroundColour("white")
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.devices = []


    def on_parent_resize(self, event):
            # self.SetSize(self.GetParent().GetSize())
            self.kvadratik_num = self.GetSize()[0] / self.chart_square_width
            self.Refresh()

    def set_scale(self, width):
        self.chart_square_width = width
        self.kvadratik_num = self.GetParent().GetSize()[0] / self.chart_square_width

    def add_device(self, device):
        if not isinstance(device, Device):
            raise TypeError("Argument must be Device")

        self.devices.append(device)
        self.devices = sorted(self.devices, key=lambda c_device: device.order)
        self.Layout()
        self.Refresh()


    def draw_device(self, device, device_id):
        dc = wx.PaintDC(self)
        dc.BeginDrawing()
        dc.SetPen(wx.Pen("black", style=wx.SOLID))
        if self.kvadratik_num < len(device.states):
            for i in range(len(device.states) - self.kvadratik_num, len(device.states)):
                dc.SetBrush(wx.Brush(device.states[i].color, wx.SOLID))
                dc.DrawRectangle(self.chart_square_width * (i - len(device.states) + self.kvadratik_num), self.chart_square_width * device_id, self.chart_square_width, self.chart_square_width)
        else:
            for i in range(0, len(device.states)):
                dc.SetBrush(wx.Brush(device.states[i].color, wx.SOLID))
                dc.DrawRectangle(self.chart_square_width * i, self.chart_square_width * device_id, self.chart_square_width, self.chart_square_width)

        dc.EndDrawing()
        del dc

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        self.DoPrepareDC(dc)
        dc.Clear()
        dc.EndDrawing()
        """set up the device context (DC) for painting"""
        MaxOrder = 0
        for device in self.devices:
            if device.order > MaxOrder:
                MaxOrder = device.order
            self.draw_device(device, device.order)
        self.SetVirtualSize((1000,self.chart_square_width * (MaxOrder + 1)))
        self.Layout()

    def RemoveDevice(self, device):
        if not isinstance(device, Device):
            raise TypeError("Argument must be Device")

        self.devices.remove(device)
        self.devices = sorted(self.devices, key=lambda c_device: device.order)
        self.Layout()
        self.Refresh()

# if __name__ == '__main__':
# app = wx.PySimpleApp()
# # create a window/frame, no parent, -1 is default ID
#     frame = wx.Frame(None, -1, "Drawing A Rectangle...", size=(800, 500))
#
# # call the derived class, -1 is default ID
#     cpu0 = Device("CORE0")
#     cpu1 = Device("CORE1")
#     cpuC0 = DeviceState(0, "green", "C0")
#     cpuC1 = DeviceState(1, "yellow", "C1")
#     cpuC2 = DeviceState(2, "red", "C2")
#
#     cpu0.add_device(0, cpuC0)
# #pu0.add_state(1, cpuC2)
# #pu0.add_state(2, cpuC2)
# #pu0.add_state(3, cpuC0)
#     for i in range(0, 15):
#         cpu1.add_state(i, cpuC1)
#         cpu1.add_state(i, cpuC2)
# #pu1.add_state(2, cpuC0)
# #pu1.add_state(3, cpuC0)
#
#     chart = GanttChart(frame, -1)
#     chart.add_device(cpu0)
#     chart.add_device(cpu1)
#
# # GanttChart(frame, -1, 1, 1)
# # show the frame
#     frame.Show(True)
# # start the event loop
#     app.MainLoop()
