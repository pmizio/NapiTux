# *-* coding: utf-8 *-*

'''
Created on 21-12-2012

@author: miziak
'''

import wx, sys, os
from Paths import *

class InfoBalloon(wx.Frame):
    def __init__(self, parent, info, status = True):
        wx.Frame.__init__(self, wx.GetApp().TopWindow, -1, "Shaped Window", style = wx.FRAME_SHAPED | wx.SIMPLE_BORDER | wx.FRAME_NO_TASKBAR)
        self.hasShape = False
        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        image = wx.Image(getDir() + "/bg.png", wx.BITMAP_TYPE_PNG)
        image.ConvertAlphaToMask()
        self.bmp = image.ConvertToBitmap()
        self.SetClientSize((self.bmp.GetWidth(), self.bmp.GetHeight()))
        dc = wx.ClientDC(self)
        dc.DrawBitmap(self.bmp, 0,0, True)
        self.panel = wx.Panel(self, wx.ID_ANY, size = (self.bmp.GetWidth(), self.bmp.GetHeight()))
        self.panel.Bind(wx.EVT_RIGHT_UP, self.OnExit)
        self.panel.Bind(wx.EVT_LEFT_UP, self.OnExit)
        cover = wx.ImageFromStream(info["cover"]).ConvertToBitmap()
        bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, cover, (13, 5))
        bitmap.Bind(wx.EVT_RIGHT_UP, self.OnExit)
        bitmap.Bind(wx.EVT_LEFT_UP, self.OnExit)
        self.textinfo = u"""Status: {7}
Tytuł:
    {0}

Gatunek: {1}
Kraj i rok: {2}, {3}
Czas trawania: {4}
Rozmiar pliku: {5}
Rozdzielczość: {6}



Link do filmweb.pl:""".format(info["title"], info["genre"], info["country"],
                             info["year"], info["duration"][:info["duration"].rfind(".")],
                             info["size"], info["resolution"], "Pobrano!" if status else "Nie pobrano!")
        #title = wx.StaticText(self.panel, label="\n"+textinfo, pos=(170, 5))
        #title.SetForegroundColour((0xFF, 0xFF, 0xFF))
        #title.SetFont(font)
        #title.Bind(wx.EVT_RIGHT_UP, self.OnExit)
        #title.Bind(wx.EVT_LEFT_UP, self.OnExit)
            
        hyperlink = wx.HyperlinkCtrl(self.panel, wx.NewId(), u""+info["title"]+" na filmweb.pl", info["filmweb"], (175, 175))
        hyperlink.Bind(wx.EVT_HYPERLINK, self.Hyperlink)
    
        self.panel.Bind(wx.EVT_PAINT, self.OnPaint)
		
        if(sys.platform != "win32"):
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetWindowShape)
        else:
		    self.SetWindowShape()
		
        #self.SetPosition((1516, 36))
        wx.Frame.SetTransparent(self, 220)
        self.Centre()
        self.Move((wx.GetDisplaySize()[0]-self.GetSize()[0]-5, 5))
        print(self.GetPosition())
        
    def Hyperlink(self, evt):
        wx.LaunchDefaultBrowser(evt.GetURL())
        self.Close()

    def SetWindowShape(self, evt=None):
        r = wx.RegionFromBitmap(self.bmp)
        self.hasShape = self.SetShape(r)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self.panel)
        dc.DrawBitmap(self.bmp, 0,0, True)
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        dc.SetFont(font) 
        dc.SetTextForeground(wx.Color(0xFF, 0xFF, 0xFF))
        lines = self.textinfo.split('\n')
        lines = [line.strip() for line in lines]
        print(lines)
        for i, t in enumerate(lines, start=1):
			dc.DrawText(t, 170, 5+(12*i))

    def OnExit(self, evt):
        self.Close()