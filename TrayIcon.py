# *-* coding: utf-8 *-*

'''
Created on 13-12-2012

@author: miziak
'''

import wx, types
from InfoBalloon import *
from NapiProjekt import *
from DownloadFrame import *
from Paths import *
from threading import Thread

EVT_TYPE_DOWNLOAD = wx.NewEventType()
EVT_DOWNLOAD = wx.PyEventBinder(EVT_TYPE_DOWNLOAD, 1)

class DownloadEvent(wx.PyCommandEvent):
    def __init__(self, etype, eid, value=None):
        wx.PyCommandEvent.__init__(self, etype, eid)
        self.value = value

    def GetValue(self):
        return self.value

class DownloadThread(Thread):
    def __init__(self, parent, list, lang):
        Thread.__init__(self)
        self.parent = parent
        self.list = list
        self.lang = lang

    def run(self):
        if(len(self.list) != 1):
            for i, path in enumerate(self.list, start=1):
                napi = NapiProjekt(path)

                if(napi.downloadSubtitles(self.lang)):
                    downloaded = True
                else:
                    downloaded = False
            
                wx.PostEvent(self.parent, DownloadEvent(EVT_TYPE_DOWNLOAD, -1, (downloaded, i)))
        else:
            napi = NapiProjekt(self.list[0])
            if(napi.downloadSubtitles(self.lang)):
                downloaded = True
            else:
                downloaded = False
            
            napi.getMoreInfo()
            wx.PostEvent(self.parent, DownloadEvent(EVT_TYPE_DOWNLOAD, -1, (downloaded, napi.info)))

wildcard = "Matroska video file (*.mkv)|*.mkv|MPEG4 video file (*.mp4)|*.mp4|Audio Video Interleave video file (*.avi)|*.avi|All files (*.*)|*.avi;*.mp4;*.mkv"

class TrayIcon(wx.TaskBarIcon):
    def __init__(self, parent, icon):
        super(TrayIcon, self).__init__()
        self.worker = None
        self.parent = parent
        self.SetIcon(wx.Icon(icon, wx.BITMAP_TYPE_PNG), "NapiTux")
        
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.ShowMenu)
        
        self.menu=wx.Menu()
        self.dwnldPl = wx.NewId()
        self.menu.Append(self.dwnldPl, u"Pobierz napisy(pl)")
        self.dwnldEn = wx.NewId()
        self.menu.Append(self.dwnldEn, u"Pobierz napisy(en)")
        self.menu.Append(wx.ID_EXIT, u"Wyłącz")
        
        self.Bind(wx.EVT_MENU, self.ClickEvents, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.ClickEvents, id=self.dwnldPl)
        self.Bind(wx.EVT_MENU, self.ClickEvents, id=self.dwnldEn)
        self.Bind(EVT_DOWNLOAD, self.Update)

    def ShowMenu(self, event):
        self.PopupMenu(self.menu)
        
    def Update(self, e):
        if(type(e.GetValue()[1]) == types.IntType):
            if(self.frame):
                self.frame.Update(e.GetValue()[1], e.GetValue()[0])
        else:
            InfoBalloon(self.parent, e.GetValue()[1], e.GetValue()[0]).Show()
        
    def ClickEvents(self, event):
        if(event.GetId() == wx.ID_EXIT):
            if(self.worker):
                self.worker.join()
                for frame in self.parent.GetChildren():
                    frame.Destroy()
            
            self.parent.Destroy()
            self.Destroy()
        elif(event.GetId() == self.dwnldPl or event.GetId() == self.dwnldEn):
            dlg = wx.FileDialog(None, message=u"Wybierz filmy do których chcesz pobrać napisy!", defaultDir="",  defaultFile="", wildcard=wildcard, style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)
            
            if(dlg.ShowModal() == wx.ID_OK):
                paths = dlg.GetPaths()
                dlg.Destroy()
                if(len(paths) != 1):
                    self.frame = DownloadFrame(self.parent, u"Pobieranie napisów...", (350, 250), getDir() + "/ico.png", paths)
                
                self.worker = DownloadThread(self, paths, True if event.GetId() == self.dwnldEn else False)
                self.worker.start()
                
class MainWindow(wx.Frame):
    def __init__(self):
        super(MainWindow, self).__init__(None)
        self.Show(False)
        TrayIcon(self, getDir() + "/ico.png")
        