# *-* coding: utf-8 *-*

'''
Created on 13-12-2012

@author: miziak
'''

import wx, os, re
#from optparse import OptionParser
from TrayIcon import MainWindow
from NapiProjekt import NapiProjekt
#from AnimatedText import *
from CmdParser import CmdParser
from Paths import completePath

def main():
    parser = CmdParser("NapiTux", "", "0.1beta")
    parser.addOpt("console", "c", "console", "exist", "change application mode to console", False)
    parser.addOpt("target", "t", "target", "var", "set downloading target may be directory or file", "")
    parser.addOpt("language", "l", "lang", "var", "set languago of subtitles(PL or ENG, default PL)", "PL")

    try:
        parser.praseCmd()
    except Exception as e:
        print e

    opt = parser.values_dict

    if("~" in opt["target"]):
        opt["target"] = os.path.expanduser(opt["target"])

    if(opt["console"]):
        if(os.path.isfile(opt["target"])):
            napi = NapiProjekt(opt["target"])
            if(napi.downloadSubtitles(opt["language"] == "ENG")):
                print("Pobrano napisy do: " + os.path.basename(opt["target"]) + "!")
            else:
                print("Nie znaleziono napisów do: " + os.path.basename(opt["target"]) + "!")
        else:
            dir = completePath(opt["target"])
            for filename in os.listdir(dir):
                if(re.match(".+\.(avi|mp4|mkv)", filename)):
                    napi = NapiProjekt(dir + filename)
                    if(napi.downloadSubtitles(opt["language"] == "ENG")):
                        print("Pobrano napisy do: " + os.path.basename(filename) + "!")
                    else:
                        print("Nie znaleziono napisów do: " + os.path.basename(filename) + "!")
    else:   
        app = wx.App(redirect=False)
        MainWindow()    
        app.MainLoop()
    '''app = wx.App(redirect=False)
    frame = MyForm().Show()
    app.MainLoop()'''

if(__name__ == '__main__'):
    main()
