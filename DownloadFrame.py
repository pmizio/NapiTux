# *-* coding: utf-8 *-*

'''
Created on 07-01-2013

@author: miziak
'''

import wx, os
from InfoBalloon import *
from NapiProjekt import *
from Paths import *

class DownloadFrame(wx.Frame):
    def __init__(self, parent, name, _size, icon, paths):
        super(DownloadFrame, self).__init__(parent, title=name, size=_size, style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        panel = wx.Panel(self)
        vbox =wx.BoxSizer(wx.VERTICAL)
        self.parent = parent
        self.paths = paths
        self.index = None
        
        ico = wx.Icon(icon, wx.BITMAP_TYPE_PNG)
        self.SetIcon(ico)
        self.im_list = wx.ImageList(16, 16)
        self.im_list.Add(wx.Image(getDir() + "/blank.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.im_list.Add(wx.Image(getDir() + "/yes.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.im_list.Add(wx.Image(getDir() + "/no.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        
        
        #appname = wx.StaticText(panel, label="NapiTux", pos=(10, 10))
        #appname.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.DEFAULT, wx.FONTWEIGHT_NORMAL))
        #wx.StaticText(panel, label="", pos=(10, 10))
        
        #self.list_ctrl = wx.ListCtrl(panel, size=(_size[0]-15, _size[1]-90), pos=(5, 25), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        vbox.Add(self.list_ctrl, flag=wx.EXPAND|wx.ALL, border=3, proportion=1)
        self.list_ctrl.SetImageList(self.im_list, wx.IMAGE_LIST_SMALL)
        self.list_ctrl.InsertColumn(0, " ", width=20)
        self.list_ctrl.InsertColumn(1, u"Tytuł")
        
        for i, path in enumerate(paths, start=0):
            self.list_ctrl.InsertImageItem(i, 0)
            self.list_ctrl.SetStringItem(i, 1, os.path.basename(path))
        	
        self.list_ctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.list_ctrl.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.OnColDrag)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnActiveItem)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelectItem)
        
        #self.gauge = wx.Gauge(panel, 0, 100, size=(_size[0]-15, 25), pos=(5, _size[1]-60))
        #self.btn = wx.Button(panel, wx.ID_OK, label="OK", size=(80, 25), pos=(140, _size[1]-30))
        
        self.gauge = wx.Gauge(panel, 0, 100)
        vbox.Add(self.gauge, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=3)
        self.btn = wx.Button(panel, wx.ID_OK, label="OK", size=(80, 25))
        vbox.Add(self.btn, flag=wx.ALIGN_CENTER|wx.BOTTOM, border=3)
        
        
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.Bind(wx.EVT_BUTTON, self.OnClick, id=wx.ID_OK)

        panel.SetSizer(vbox)  
        self.Centre()
        self.Show()
        
    def Update(self, i, bool):
        self.gauge.SetValue(int(float(i)/len(self.paths)*100))
        self.list_ctrl.SetItemColumnImage(i-1, 0, 1 if bool else 2)
    
    def OnQuit(self, e):
        self.Destroy()
        
    def OnClick(self, e):
        if(self.index != None):
            napi = NapiProjekt(self.paths[self.index])
            napi.getMoreInfo()
            InfoBalloon(self.parent, napi.info, False).Show()
        
        self.Destroy()
    
    def OnColDrag(self, e):
        e.Veto()
        
    def OnActiveItem(self, e):
        self.index = e.GetIndex()
        napi = NapiProjekt(self.paths[self.index])
        napi.getMoreInfo()
        InfoBalloon(self.parent, napi.info, False).Show()
        
    def OnSelectItem(self, e):
        self.index = e.GetIndex()
