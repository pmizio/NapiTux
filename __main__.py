# *-* coding: utf-8 *-*

'''
Created on 13-12-2012

@author: miziak
'''

import wx, sys, os, re
from optparse import OptionParser
from TrayIcon import *
from NapiProjekt import *
from AnimatedText import *

def main():
    app = wx.App(redirect=False)
    
    parser = OptionParser(usage="usage: %prog [options] filename", version="%prog 0.1")
    parser.add_option("-c", "--console-mode", action="store_true", dest="console", default=False, help="run program only in console mode")
    parser.add_option("-w", "--without-gui", action="store_true", dest="gui", default=False, help="run program without GUI")
    parser.add_option("-d", "--directory",  action="store", dest="dir", default="", help="directory witch video files")
    parser.add_option("-l", "--language",  action="store", dest="lang", default="PL", help="language of subtitles(PL or ENG)")
    (options, args) = parser.parse_args()
    option_dict = vars(options)
    
    if(option_dict["console"]):
        napi = NapiProjekt(args[0])
        if(napi.downloadSubtitles(option_dict["lang"] == "ENG")):
            print("Pobrano napisy do: " + os.path.basename(args[0]) + "!")
            downloaded = True
        else:
            print("Nie znaleziono napisów do: " + os.path.basename(args[0]) + "!")
            downloaded = False
        
        if(not option_dict["gui"]):
            napi.getMoreInfo()
            InfoBalloon(None, napi.info, downloaded).Show()
    elif(option_dict["dir"]):
        dir = completePath(option_dict["dir"])
        for filename in os.listdir(dir):
            if(re.match(".+\.(avi|mp4|mkv)", filename)):
                napi = NapiProjekt(dir + filename)
                if(napi.downloadSubtitles()):
                    print("Pobrano napisy do: " + os.path.basename(filename) + "!")
                else:
                    print("Nie znaleziono napisów do: " + os.path.basename(filename) + "!")
    else:
        
        MainWindow()
        
    app.MainLoop()
    '''app = wx.App(redirect=False)
    frame = MyForm().Show()
    app.MainLoop()'''

if(__name__ == '__main__'):
    main()
