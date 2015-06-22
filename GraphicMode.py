#from wx.lib.agw.buttonpanel import BoxSizer
from ganttchart import GanttChart
from Device import Device, DeviceState

__author__ = 'Marina'

import wx
#import wx.lib.inspection


class GraphicModeFrame(wx.Frame):
    device_counter = 0
    devices = {}
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title)
        self.parent = parent
        self.SetMinSize((300, 300))
        self.SetPosition((300,200))
        self.create_menu()

        self.create_check_box_panel()


        self.chart = GanttChart(self, wx.ID_ANY)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.check_box_panel, 0, wx.ALL, border=8)
        box.Add(self.chart, 1, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()

    def create_check_box_panel(self):
        size = self.GetSize()
        screenSize = self.GetSize()
        screenWidth = screenSize[0]
        screenHeight = screenSize[1]

        #self.check_box_panel = wx.Panel(self)  # Create panel with devices checkboxes
        #self.check_box_panel.SetMinSize((200, -1))

        self.check_box_panel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(200,1000), pos=(0,28), style=wx.SIMPLE_BORDER)
        self.check_box_panel.SetAutoLayout(1)
        self.check_box_panel.SetupScrolling()


        box = wx.StaticBox(self.check_box_panel, wx.ID_ANY, "Devices")  # Static box with sexy borders
        self.check_box_panel_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)  # Sizer
        self.check_box_panel.SetSizer(self.check_box_panel_sizer)

        self.check_box_panel_sizer.Fit(self.check_box_panel)

    def create_menu(self):
        self.fileMenu = wx.Menu()
        
        fqitem = wx.MenuItem(self.fileMenu, 0, '&Quit\tCtrl+Q')
        #fqitem.SetBitmap(wx.Bitmap('exit.png'))
        self.fileMenu.AppendItem(fqitem)
        self.fileMenu.AppendSeparator()
        fsitem = wx.MenuItem(self.fileMenu, 5, '&Stop\tCtrl+T')
        self.fileMenu.AppendItem(fsitem)

        fbitem = wx.MenuItem(self.fileMenu, 6, '&Start\tCtrl+B')
        self.fileMenu.AppendItem(fbitem)
        
        fmitem = wx.Menu()
        
        mode_1_item = wx.Menu()
        fmitem.AppendMenu(wx.ID_ANY, '&Mode1', mode_1_item)

        mode_2_item = wx.MenuItem(fmitem, 2, '&Mode2')
        fmitem.AppendItem(mode_2_item)

        self.fileMenu.AppendMenu(wx.ID_ANY, 'Mode', fmitem)

        mode_1_item_scale_min = wx.MenuItem(mode_1_item, 1, '&ScaleMin')
        mode_1_item_scale_norm = wx.MenuItem(mode_1_item, 4, '&ScaleNorm')
        mode_1_item_scale_max = wx.MenuItem(mode_1_item, 3, '&ScaleMax')

        mode_1_item.AppendItem(mode_1_item_scale_max)
        mode_1_item.AppendItem(mode_1_item_scale_norm)
        mode_1_item.AppendItem(mode_1_item_scale_min)

        
        self.menu_bar = wx.MenuBar()  
        self.menu_bar.Append(self.fileMenu, 'File')
        self.SetMenuBar(self.menu_bar)
        
        self.Bind(wx.EVT_MENU, self.parent.OnQuit, fqitem)
        self.Bind(wx.EVT_CLOSE, self.parent.OnQuit)
        self.Bind(wx.EVT_MENU, self.parent.OnMode_1_max, mode_1_item_scale_max)
        self.Bind(wx.EVT_MENU, self.parent.OnMode_1_min, mode_1_item_scale_min)
        self.Bind(wx.EVT_MENU, self.parent.OnMode_1_norm, mode_1_item_scale_norm)
        self.Bind(wx.EVT_MENU, self.parent.OnMode_2, mode_2_item)
        self.Bind(wx.EVT_MENU, self.parent.OnStop, fsitem)
        self.Bind(wx.EVT_MENU, self.parent.OnStart, fbitem)
                
    def DeviceChecked(self, evt):
        device = self.devices[evt.GetEventObject().GetId()]
        if evt.GetEventObject().GetValue():
            self.chart.add_device(device)
        else:
            self.chart.RemoveDevice(device)


    def AddDevice(self, device):
        if not isinstance(device, Device):  # Check that received object is Device
            raise TypeError("Device must be type of class Device")
        device.order = self.device_counter
        self.device_counter += 1
        device_check_box = wx.CheckBox(self.check_box_panel, wx.ID_ANY, label=device.name, size=((100,38)))
        device_check_box.SetValue(False)
        device_check_box.Bind(wx.EVT_CHECKBOX, self.DeviceChecked)
        self.devices[device_check_box.GetId()] = device

        # device_check_box.SetV

        self.check_box_panel_sizer.Add(device_check_box, 0, wx.ALL, 2)

        self.check_box_panel_sizer.Fit(self.check_box_panel)



