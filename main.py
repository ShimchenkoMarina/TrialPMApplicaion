#!/usr/bin/env python

import threading
import wx
import time
import wx.lib.inspection
from GraphicMode import GraphicModeFrame
from Device import Device, DeviceState
from FlasherChart import FlasherChart

class HelpBox(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, size=(400,400))
        self.parent = parent
        self.SetMinSize((400,400))
        self.SetMaxSize((400,400))
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        self.panel = wx.Panel(self, -1)


        '''self.spSizer0 = wx.BoxSizer(wx.VERTICAL)
        self.spSizer1 = wx.BoxSizer(wx.VERTICAL)
        self.spSizer2 = wx.BoxSizer(wx.HORIZONTAL)'''

        self.panel.Bind(wx.EVT_PAINT, self.OnPaint)

        #self.panel.SetSizer(self.spSizer0)
        self.Centre()

    def OnPaint(self, event):
        dc = wx.PaintDC(self.panel)
        #dc.SetPen(wx.Pen('#4c4c4c', 1, wx.SHORT_DASH))
        dc.SetBrush(wx.Brush(self.parent.cpuC0.color))
        dc.DrawRectangle(1,1, 20, 20)
        dc.DrawText('C0',30,1)
        dc.SetBrush(wx.Brush(self.parent.cpuC1.color))
        dc.DrawRectangle(1,25, 20, 20)
        dc.DrawText('C1', 30,25)
        #self.spSizer0.Add(dc)

    def OnQuit(self, e):
        self.Destroy()

class MessageBox(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, size=(400,400))
        self.parent = parent
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        total_tr = self.parent.cpu0.flag_change + self.parent.cpu1.flag_change

        #self.scroll = wx.ScrolledWindow( self, -1 )

        panel = wx.lib.scrolledpanel.ScrolledPanel(self, -1, size=(300,200), pos=(0,28), style=wx.SIMPLE_BORDER)
        panel.SetAutoLayout(1)
        panel.SetupScrolling()
        self.spSizer0 = wx.BoxSizer(wx.VERTICAL)
        self.spSizer1 = wx.BoxSizer(wx.VERTICAL)
        self.spSizer2 = wx.BoxSizer(wx.VERTICAL)
        self.spSizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.spSizer4 = wx.BoxSizer(wx.VERTICAL)
        self.spSizer5 = wx.BoxSizer(wx.VERTICAL)

        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        heading = wx.StaticText(panel, -1, 'Total:', (90, 15))
        self.spSizer0.Add(heading, 1, wx.EXPAND | wx.TOP , 20)
        heading.SetFont(font)

        self.spSizer0.Add(wx.StaticLine(panel, -1, (25, 50), (300,1)))
        self.spSizer1.Add(wx.StaticText(panel, -1, 'Slovakia', (25, 80)))
        self.spSizer1.Add(wx.StaticText(panel, -1, 'Hungary', (25, 100)))
        self.spSizer1.Add(wx.StaticText(panel, -1, 'Poland', (25, 120)))
        self.spSizer1.Add(wx.StaticText(panel, -1, 'Czech Republic', (25, 140)))
        self.spSizer1.Add(wx.StaticText(panel, -1, 'Germany', (25, 160)))
        self.spSizer1.Add(wx.StaticText(panel, -1, 'Slovenia', (25, 180)))
        self.spSizer1.Add(wx.StaticText(panel, -1, 'Austria', (25, 200)))
        self.spSizer1.Add(wx.StaticText(panel, -1, 'Switzerland', (25, 220)))

        self.spSizer2.Add(wx.StaticText(panel, -1, '5 379 000'),wx.ALIGN_LEFT)
        self.spSizer2.Add(wx.StaticText(panel, -1, '10 084 000', (250, 100)))
        self.spSizer2.Add(wx.StaticText(panel, -1, '38 635 000', (250, 120)))
        self.spSizer2.Add(wx.StaticText(panel, -1, '10 240 000', (250, 140)))
        self.spSizer2.Add(wx.StaticText(panel, -1, '82 443 000', (250, 160)))
        self.spSizer2.Add(wx.StaticText(panel, -1, '2 001 000', (250, 180)))
        self.spSizer2.Add(wx.StaticText(panel, -1, '8 032 000', (250, 200)))
        self.spSizer2.Add(wx.StaticText(panel, -1, '7 288 000', (250, 220)))

        self.spSizer4.Add(wx.StaticLine(panel, -1, (25, 260), (300,1)))

        sum = wx.StaticText(panel, -1, str(total_tr), (240, 280))
        sum_font = sum.GetFont()
        sum_font.SetWeight(wx.BOLD)
        sum.SetFont(sum_font)
        self.spSizer4.Add(sum, 1,wx.LEFT, 200)

        self.spSizer4.Add(wx.Button(panel, 1, 'Ok', (140, 310), (60, 30)),1, wx.LEFT, 150)
        self.Bind(wx.EVT_BUTTON, self.OnQuit)
        self.spSizer3.Add(self.spSizer1, proportion=1, flag=wx.RIGHT,
            border=100)
        self.spSizer3.Add(self.spSizer2, proportion=1, flag=wx.RIGHT,
            border=10)

        self.spSizer5.Add(self.spSizer0)
        self.spSizer5.Add(self.spSizer3, 1, wx.LEFT, 30)
        self.spSizer5.Add(self.spSizer4)

        panel.SetSizer(self.spSizer5)
        self.Centre()

    def OnQuit(self, e):
        self.Destroy()



class Me(wx.Frame):
    def __init__(self, _stop_event):
        super(Me, self).__init__(None)
        self.pause = 0
        self.stop_event = _stop_event
        self.SetSize = (1000, 1000)
        self.col = wx.Colour(0,190,255)
        self.SetBackgroundColour(self.col)
        self.cpu0 = Device("CORE0")
        self.cpu1 = Device("CORE1")
        self.dev1 = Device("dev1")
        self.dev2 = Device("dev2")
        self.dev3 = Device("dev3")
        self.dev4 = Device("dev4")
        self.dev5 = Device("dev5")
        self.dev6 = Device("dev6")
        self.cpuC0 = DeviceState(0, "green", "C0")
        self.cpuC1 = DeviceState(1, "yellow", "C1")
        self.cpuC2 = DeviceState(2, "red", "C2")

        self.create_menu()
        self.SetMinSize((1100, 800))
        self.SetPosition((100,100))
        self.set_title("PM analyzer")

        self.gpf = GraphicModeFrame(self, -1, "Sizer Test")
        self.mode1_constructor()



        '''for i in range(0, 100, 2):
            cpu1.add_state(i, cpuC1)
            cpu1.add_state(i+1, cpuC2)
        cpu1.add_state(100, cpuC0)'''
        self.gpf.AddDevice(self.cpu1)
        self.gpf.AddDevice(self.cpu0)
        self.gpf.AddDevice(self.dev1)
        self.gpf.AddDevice(self.dev2)
        self.gpf.AddDevice(self.dev3)
        self.gpf.AddDevice(self.dev4)
        self.gpf.AddDevice(self.dev5)
        self.gpf.AddDevice(self.dev6)

    def GetPMValues(self, tick):
        if self.pause is 0:
            if tick % 2 == 0:
                self.cpu0.add_state(tick, self.cpuC0)
                self.cpu1.add_state(tick, self.cpuC1)
                self.dev1.add_state(tick, self.cpuC0)
                self.dev2.add_state(tick, self.cpuC1)
                self.dev3.add_state(tick, self.cpuC2)
                self.dev4.add_state(tick, self.cpuC0)
                self.dev5.add_state(tick, self.cpuC1)
                self.dev6.add_state(tick, self.cpuC2)
            else:
                self.cpu0.add_state(tick, self.cpuC1)
                self.cpu1.add_state(tick, self.cpuC2)
                self.dev1.add_state(tick, self.cpuC1)
                self.dev2.add_state(tick, self.cpuC2)
                self.dev3.add_state(tick, self.cpuC0)
                self.dev4.add_state(tick, self.cpuC1)
                self.dev5.add_state(tick, self.cpuC2)
                self.dev6.add_state(tick, self.cpuC0)
            self.gpf.Refresh()
            self.panel.Refresh()
        #self.Refresh()

    def mode1_constructor(self):
        self.vbox1 = wx.BoxSizer(wx.VERTICAL)
        self.panel = FlasherChart(self, -1)
        self.panel.SetBackgroundColour(wx.Colour(245,222,179)) 
        self.panel.Bind(wx.EVT_PAINT, self.OnPaint)
        self.vbox1.Add(self.panel, proportion=1, flag=wx.EXPAND)

        #Addind device
        self.panel.AddDevice(self.cpu0, 10, 15, 60, 40)

    def OnPaint(self, event):
        self.panel.OnPaint(None)
        #Experiment
        dc = wx.PaintDC(self.panel)

        #Define pens and brushes
        pen_basic = wx.Pen(wx.Colour(23,128,109), 2, wx.SOLID)
        brush_basic = wx.Brush(wx.Colour(48,186,143))
        pen_service = wx.Pen(wx.Colour(78,87,84), 2, wx.SOLID)
        brush_service = wx.Brush('#C8A696')
        pen_bus = wx.Pen('#FF2B2B', 6, wx.SOLID)
        brush_bus = wx.Brush('#FD5E53')
        pen_csme = wx.Pen('#FF9218', 2, wx.SOLID)
        brush_csme = wx.Brush('#F8D568')
        pen_hw = wx.Pen('#131313', 2, wx.SOLID)
        brush_hw = wx.Brush('#F8F8FF')

        #Contur
        dc.SetPen(wx.Pen('#4c4c4c', 1, wx.SHORT_DASH))
        dc.SetBrush(wx.Brush('#C9C0BB'))
        dc.DrawRectangle(550, 305, 500, 220)
        dc.SetBrush(wx.Brush('#D7D7D7'))
        dc.DrawRectangle(565, 395, 330, 110)

        #Basic pen and brush for periferal devices == green
        pen_basic.SetJoin(wx.JOIN_ROUND)
        dc.SetPen(pen_basic)
        dc.SetBrush(brush_basic)
        #dc.DrawRectangle(10, 15, 60, 40)
        dc.DrawRectangle(72, 15, 60, 40)
        dc.DrawRectangle(10, 57, 122, 40)

        dc.DrawRectangle(102, 205, 60,40)
        dc.DrawRectangle(182, 205, 60, 40)
        dc.DrawRectangle(142, 255, 60, 40)
        
        dc.DrawRectangle(265, 405, 60, 40)
        dc.DrawRectangle(335, 405, 60, 40)
        dc.DrawRectangle(405, 405, 60, 40)
        dc.DrawRectangle(300, 458, 60, 40)
        dc.DrawRectangle(375, 458, 60, 40)
        dc.DrawRectangle(445, 458, 60, 40)
        dc.DrawRectangle(65, 405, 30, 40)
        dc.DrawRectangle(134, 405, 60, 40)
        dc.DrawRectangle(200, 405, 60, 40)
        
        dc.DrawRectangle(10, 610, 30, 40)
        dc.DrawRectangle(80, 610, 30, 40)
        dc.DrawRectangle(150, 610, 30, 40)
        dc.DrawRectangle(220, 610, 60, 40)
        dc.DrawRectangle(290, 610, 60, 40)
        dc.DrawRectangle(360, 610, 60, 40)
        
        dc.DrawRectangle(45, 670, 30, 40)
        dc.DrawRectangle(115, 670, 60, 40)
        dc.DrawRectangle(185, 670, 60, 40)
        
        dc.DrawRectangle(812, 450, 30, 40)
        dc.DrawRectangle(777, 400, 30, 40)
        dc.DrawRectangle(905, 400, 30, 40)
        
        dc.DrawRectangle(697, 660, 20, 15)
        
        #HW -#-#-#- for hw block == white
        pen_csme.SetJoin(wx.JOIN_ROUND)
        dc.SetPen(pen_hw)
        dc.SetBrush(brush_hw)
        dc.DrawRectangle(100, 458, 60, 40)
        dc.DrawRectangle(168, 458, 60, 40)
        dc.DrawRectangle(255, 670, 60, 40)
        dc.DrawCircle(500, 630, 30)
        dc.DrawRectangle(540, 610, 60, 40)
        dc.DrawRectangle(480, 540, 60, 40)
        dc.DrawRectangle(480, 680, 60, 40)
        
        dc.DrawRectangle(697, 620, 20, 15)
        
        #Csme -#-#-#- for csme root space == yellow
        pen_csme.SetJoin(wx.JOIN_ROUND)
        dc.SetPen(pen_csme)
        dc.SetBrush(brush_csme)
        dc.DrawRectangle(95, 405, 30, 40)
        dc.DrawRectangle(40, 610, 30, 40)
        dc.DrawRectangle(110, 610, 30, 40)
        dc.DrawRectangle(180, 610, 30, 40)
        dc.DrawRectangle(75, 670, 30, 40)
        dc.DrawRectangle(567, 400, 60, 40)
        dc.DrawRectangle(637, 400, 60, 40)
        dc.DrawRectangle(707, 400, 60, 40)
        dc.DrawRectangle(807, 400, 30, 40)
        dc.DrawRectangle(935, 400, 30, 40)
        dc.DrawRectangle(602, 450, 60, 40)
        dc.DrawRectangle(672, 450, 60, 40)
        dc.DrawRectangle(742, 450, 60, 40)
        dc.DrawRectangle(842, 450, 30, 40)
        
        dc.DrawRectangle(697, 680, 20, 15)
        
        #Bus -#-#-#- for buses
        pen_service.SetJoin(wx.JOIN_MITER)
        dc.SetPen(pen_bus)
        dc.SetBrush(brush_bus)
        dc.DrawRectangle(10, 115, 650, 70)
        dc.DrawRectangle(10, 315, 250, 70)
        dc.DrawRectangle(10, 315, 250, 70)
        dc.DrawRectangle(270, 315, 205, 70)
        dc.DrawRectangle(10, 520, 430, 70)
        
        dc.DrawRectangle(700, 640, 15, 15)
        
        #Service -#-#-#- for conection elements
        dc.SetPen(pen_service)
        dc.SetBrush(brush_service)
        dc.DrawLine(60, 97, 60, 115)
        dc.DrawLine(60, 185, 60, 315)
        dc.DrawLine(60, 385, 60, 520)
        dc.DrawLine(280, 185, 280, 315)
        dc.DrawLine(600, 185, 600, 315)
        dc.DrawLine(132, 185, 132, 205)
        dc.DrawLine(212, 185, 212, 205)
        dc.DrawLine(172, 185, 172, 255)
        dc.DrawLine(295, 385, 295, 405)
        dc.DrawLine(365, 385, 365, 405)
        dc.DrawLine(435, 385, 435, 405)
        dc.DrawLine(330, 385, 330, 458)
        dc.DrawLine(400, 385, 400, 458)
        dc.DrawLine(130, 385, 130, 458)
        dc.DrawLine(198, 385, 198, 458)
        dc.DrawLine(95, 385, 95, 405)
        dc.DrawLine(165, 385, 165, 405)
        dc.DrawLine(230, 385, 230, 405)
        dc.DrawLine(467, 385, 467, 458)
        
        dc.DrawLine(40, 590, 40, 610)
        dc.DrawLine(110, 590, 110, 610)
        dc.DrawLine(180, 590, 180, 610)
        dc.DrawLine(250, 590, 250, 610)
        dc.DrawLine(320, 590, 320, 610)
        dc.DrawLine(390, 590, 390, 610)
        
        dc.DrawLine(75, 590, 75, 670)
        dc.DrawLine(145, 590, 145, 670)
        dc.DrawLine(215, 590, 215, 670)
        dc.DrawLine(285, 590, 285, 670)
        
        dc.DrawLine(420, 630, 470, 630)
        dc.DrawLine(500, 580, 500, 600)
        dc.DrawLine(500, 660, 500, 680)
        dc.DrawLine(530, 630, 540, 630)
        
        dc.DrawRectangle(560, 315, 405, 70)
        
        
        dc.DrawLine(597, 385, 597, 400)
        dc.DrawLine(667, 385, 667, 400)
        dc.DrawLine(737, 385, 737, 400)
        dc.DrawLine(807, 385, 807, 400)
        dc.DrawLine(935, 385, 935, 400)
        
        dc.DrawLine(632, 385, 632, 450)
        dc.DrawLine(702, 385, 702, 450)
        dc.DrawLine(772, 385, 772, 450)
        dc.DrawLine(842, 385, 842, 450)
        
        #Write text
        #Legend
        dc.DrawText('Legend:', 700, 600)
        dc.DrawText('HW Block', 720, 620)
        dc.DrawText('PCH Backbone Components', 720, 640)
        dc.DrawText('Host Root Space', 720, 660)
        dc.DrawText('CSME Root Space', 720, 680)
        
        dc.DrawText('PCIe', 20, 18)
        dc.DrawText('LL/PL', 16, 33)
        dc.DrawText('OPI', 90, 18)
        dc.DrawText('LL/PL', 85, 33)
        dc.DrawText('DMI TL', 50, 67)
        
        dc.DrawText('CSME IOSF Fabric(64b, 200MHZ) Bus 0', 690, 330)
        dc.DrawText('KVMcc', 575, 410)
        dc.DrawText('ME', 655, 405)
        dc.DrawText('SMT x3', 643, 417)
        dc.DrawText('SST /', 720, 405)
        dc.DrawText('PECI', 720, 417)
        dc.DrawText('PMI', 795, 410)
        dc.DrawText('CSE', 925, 410)
        dc.DrawText('CSE', 550, 287)
        dc.DrawText('CM', 570, 485)
        
        dc.DrawText('USB-R', 609, 460)
        dc.DrawText('South', 682, 453)
        dc.DrawText('Clink', 682, 465)
        dc.DrawText('Perf Prof', 744, 452)
        dc.DrawText('/ODLA', 750, 467)
        dc.DrawText('PTIO', 826, 455)
        
        dc.DrawText('PSF #1(128b, 250MHZ) Bus 0', 420, 120)
        dc.DrawText('PCIe 3', 108, 210)
        dc.DrawText('x4', 127, 220)
        dc.DrawText('PCIe 3', 188, 210)
        dc.DrawText('x4', 205, 220)
        dc.DrawText('PCIe 3', 148, 260)
        dc.DrawText('x4', 165, 270)
        dc.DrawText('PSF #2(128b, 125MHZ) Bus 0', 55, 320)
        dc.DrawText('PSF #2(128b, 125MHZ) Bus 0', 278, 320)
        
        dc.DrawText('xHCI', 75, 412)
        dc.DrawText('Camera', 136, 410)
        dc.DrawText('Pipe', 143, 422)
        dc.DrawText('Thermal', 202, 410)
        dc.DrawText('SATA3', 269, 410)
        dc.DrawText('VR', 279, 422)
        dc.DrawText('SATA3', 339, 410)
        dc.DrawText('VS1', 349, 422)
        dc.DrawText('SATA3', 409, 410)
        dc.DrawText('VS3', 417, 422)
        dc.DrawText('SATA3', 303, 460)
        dc.DrawText('VS0', 310, 474)
        dc.DrawText('SATA3', 377, 460)
        dc.DrawText('VS2', 385, 474)
        dc.DrawText('NVM', 452, 467)
        
        #White blocks
        dc.DrawText('Exl', 116, 462)
        dc.DrawText('Bridge', 104, 475)
        dc.DrawText('ISH', 182, 467)
        dc.DrawText('NPK', 264, 678)
        dc.DrawText('PES', 491, 549)
        dc.DrawText('GPIO', 551, 620)
        dc.DrawText('HPET', 490, 690)
        dc.DrawText('IOSF-SB', 477, 612)
        dc.DrawText('Router', 480, 627)
        
        #Low layout
        dc.DrawText('PSF #3(64b, 125MHZ) Bus 0', 250, 527)
        dc.DrawText('HDA/', 19, 615)
        dc.DrawText('DSP', 22, 627)
        dc.DrawText('SPI, eSPI', 83, 617)
        dc.DrawText('PMS', 164, 617)
        dc.DrawText('LPC', 237, 617)
        dc.DrawText('TAM', 302, 617)
        dc.DrawText('IOSF P2S', 362, 615)
        dc.DrawText('Bridge', 366, 626)
        
        dc.DrawText('GBE', 62, 680)
        dc.DrawText('LPSS', 127, 680)
        dc.DrawText('Host', 193, 673)
        dc.DrawText('SMBus', 187, 685)

    def create_menu(self):
        self.fileMenu = wx.Menu()


        
        fqitem = wx.MenuItem(self.fileMenu, 0, '&Quit\tCtrl+Q')
        #fqitem.SetBitmap(wx.Bitmap('exit.png'))
        self.fileMenu.AppendItem(fqitem)
        self.fileMenu.AppendSeparator()

        fhitem = wx.MenuItem(self.fileMenu, 8, '&Help\tCtrl+H')
        self.fileMenu.AppendItem(fhitem)
        self.Bind(wx.EVT_MENU, self.OnHelp, fhitem)

        ftotitem = wx.MenuItem(self.fileMenu, 7, '&Total\tCtrl+T')
        self.fileMenu.AppendItem(ftotitem)
        self.fileMenu.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.OnTotal, ftotitem)

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
        
        self.Bind(wx.EVT_MENU, self.OnQuit, fqitem)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.Bind(wx.EVT_MENU, self.OnMode_1_max, mode_1_item_scale_max)
        self.Bind(wx.EVT_MENU, self.OnMode_1_min, mode_1_item_scale_min)
        self.Bind(wx.EVT_MENU, self.OnMode_1_norm, mode_1_item_scale_norm)
        self.Bind(wx.EVT_MENU, self.OnMode_2, mode_2_item)
        self.Bind(wx.EVT_MENU, self.OnStop, fsitem)
        self.Bind(wx.EVT_MENU, self.OnStart, fbitem)

    def OnHelp(self, e):
        HBox = HelpBox(self, -1, "Help")
        HBox.Show()

    def OnTotal(self, e):
        MasBox = MessageBox(self, -1, "Info of total transitions")
        MasBox.Show()

    def OnStop(self, e):
        print("Stop")
        self.pause = 1

    def OnStart(self, e):
        self.pause = 0

    def OnQuit(self, e):
        dial = wx.MessageDialog(None, 'Are you sure to quit?', 'Question',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            
        ret = dial.ShowModal()
        
        if ret == wx.ID_YES:
            self.stop_event.set()
            self.Destroy()
        else:
            e.Veto()
            
    def set_title(self, text): 
        print 'text = %s' % (text)
        super(Me, self).SetTitle(text)

    def OnMode_1_max(self, event):
        self.gpf.chart.set_scale(60)
        self.gpf.Show()
        self.Hide()
        pass

    def OnMode_1_min(self, event):
        self.gpf.chart.set_scale(35)
        self.gpf.Show()
        self.Hide()
        pass

    def OnMode_1_norm(self, event):
        self.gpf.chart.set_scale(50)
        self.gpf.Show()
        self.Hide()
        pass

    def OnMode_2(self, event):
        self.gpf.Hide()
        self.Show()
        pass



def MainFunction():
    #event for stop
    stop_event = threading.Event()

    #InitialThread
    try:
        initial_th = InitialThread(stop_event)

        #start it here
        initial_th.start()
    except:
        print("Main thread failed")
        return
    #end or wait
    initial_th.join()
    print("Exiting main thread.")

class MyWindow:

  def __init__(self, _stop_event):
    self.stop_event = _stop_event

  def Show(self):
    time.sleep(10)
    self.OnQuit()

  def OnQuit(self):
    print("Hello, I'm a window!")
    input("close me: ")
    self.stop_event.set()

class InitialThread(threading.Thread):

  def __init__(self, _stop_event):
    threading.Thread.__init__(self)
    self.stop_event = _stop_event

  def run(self):

    #create a window
    app = wx.App(False)
    me = Me(self.stop_event)
    me.Show()


    try:
        #launch the computer
        computer = Computer(me, self.stop_event)
        computer.start()
    except:
        print("Computer failed")
        return

    #wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
    computer.join()


    print("Terminating the initial thread.")

class Computer(threading.Thread):

  def __init__(self, win_object, _stop_event):
    threading.Thread.__init__(self)
    self.stop_event = _stop_event
    self.main_window = win_object#Object of created windows

  def run(self):
    tock = 0
    while not self.stop_event.is_set():

      #calculation process
      self.main_window.GetPMValues(tock)
      tock = tock + 1
      time.sleep(1)

    print("Terminating the computer.")


if __name__ == '__main__':
    MainFunction()

