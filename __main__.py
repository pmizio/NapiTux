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
from Subtitles import *

def main():
    parser = CmdParser("NapiTux", "", "0.1beta")
    parser.addOpt("console", "c", "console", "exist", "change application mode to console", False)
    parser.addOpt("target", "t", "target", "var", "set downloading target may be directory or file", "")
    parser.addOpt("language", "l", "lang", "var", "set languago of subtitles(PL or ENG, default PL)", "PL")
    parser.addOpt("info", "i", "info", "var", "get informations about video", "")
    parser.addOpt("sub", "s", "subinfo", "var", "get informations about subtitles file", "")
    parser.addOpt("conv", "o", "convert", "var", "soon", "")

    try:
        parser.praseCmd()
    except Exception as e:
        print e

    opt = parser.values_dict
    
    for i,v in opt.iteritems():
        if(type(opt[i]) is str and "~" in opt[i]):
            opt[i] = os.path.expanduser(opt[i])
    #elif("~" in opt["info"]):
    #    opt["info"] = os.path.expanduser(opt["info"])
    

    if(opt["console"]):
        if(opt["info"] != ""): 
            napi = NapiProjekt(opt["info"])
            napi.getMoreInfo()
            print napi.info
        elif(opt["sub"] != ""):
            sub = Subtitles(opt["sub"])
            print sub.getType()
        elif(opt["conv"] != ""):
            sub = Subtitles(opt["conv"])
            sub.convert(SubTypesEnum.TYPE_SUBRIP, 23.976)
            sub.save()
        elif(os.path.isfile(opt["target"])):
            napi = NapiProjekt(opt["target"])
            if(napi.downloadSubtitles(opt["language"] == "ENG")):
                print("Pobrano napisy do: " + os.path.basename(opt["target"]) + "!")
            else:
                print("Nie znaleziono napisów do: " + os.path.basename(opt["target"]) + "!")
        elif(os.path.isdir(opt["target"])):
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
