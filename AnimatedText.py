# *-* coding: utf-8 *-*

'''
Created on 04-03-2013

@author: miziak
'''

import wx
import wx.lib.newevent

class AnimatedText(wx.Panel):
    def __init__(self, parent, text, point, size):
        super(AnimatedText, self).__init__(parent, wx.ID_ANY, point, size)
        self.text = text
        self.pos = 0
        self.way = True
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        dc.SetFont(font) 
        dc.SetTextForeground(wx.Color(0x00, 0x00, 0x00))
        dc.DrawText(self.text, 0-self.pos, 0)
        self.width, height = dc.GetTextExtent(self.text)
        if(self.Size[0] < self.width):
            self.timer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.update, self.timer)
            self.timer.Start(500)
        
    def update(self, event):
        if((self.Size[0] + self.pos == self.width and self.way) or (self.pos == 0 and not self.way)):
            self.way = not self.way
        else:
            if(self.way):
                self.pos += 5
            else:
                self.pos -= 5
            
            if(self.Size[0] + self.pos > self.width):
                self.pos = self.width-self.Size[0]
            elif(self.pos < 0):
                self.pos = 0
        
        self.Refresh()
        self.Update()
        
VoteBarEvent, EVT_VOTE_BAR = wx.lib.newevent.NewEvent()
        
class VoteBar(wx.Panel):
    def __init__(self, parent, point, count, cstar, gstar):
        self.pos = None
        self.count = count
        self.vote = None
        
        if(str(type(cstar)).find("Bitmap") == -1):
            self.cstar = wx.Bitmap(cstar)
            self.gstar = wx.Bitmap(gstar)
        else:
            self.cstar = cstar
            self.gstar = gstar
            
        super(VoteBar, self).__init__(parent, wx.ID_ANY, point, (count*self.cstar.GetWidth(), self.cstar.GetHeight()))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvent)
        self.Bind(wx.EVT_MOTION, self.OnMouseEvent)

    def OnMouseEvent(self, e):
        if(e.Moving()):
            self.pos = e.GetPosition()[0]
        elif e.LeftUp():
            self.pos = e.GetPosition()[0]
            wx.PostEvent(self, VoteBarEvent(value=self.vote+1))
        elif e.LeftDown():
            self.pos = e.GetPosition()[0]
        else:
            self.pos = None
            
        self.Refresh()
        self.Update()
        
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        prec = -1
        
        if(self.pos != None):
            prec = int((float(self.pos)/self.GetSize()[0])*100)
            self.vote = (self.count*prec)/100
            

        for i in range(self.count):
            if(i <= ((self.count*prec)/100) and prec != -1):
                dc.DrawBitmap(self.cstar, self.cstar.GetWidth()*i, 0)
            else:
                dc.DrawBitmap(self.gstar, self.gstar.GetWidth()*i, 0)
        
        
class MyForm(wx.Frame):
 
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Timer Tutorial 1", size=(500,500))
 
        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        AnimatedText(panel, "Paweł Mizio - Miziak 20 years old", (50, 50), (100, 20))
        vote = VoteBar(panel, (100, 100), 5, wx.Bitmap("star_color.png").ConvertToImage().Scale(20, 20, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap(), wx.Bitmap("star_grey.png").ConvertToImage().Scale(20, 20, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap())
        vote.Bind(EVT_VOTE_BAR, self.evth)
        
    def evth(self, evt):
        print evt.value