# -*- coding: utf-8 -*-

import re, datetime
from Subtitles import *

class SubRip(Subtitles):
    """docstring for SubRip"""
    def __init__(self, data, info = None, fps = None):
        super(SubRip, self).__init__(data, info)
        
        print self.type

        if(self.type != SubTypesEnum.TYPE_SUBRIP):
            if(info != None):
                self.convert(float(info["fps"]))
            else:
                self.convert(fps)

    def convertToTime(self, _str, fps):
        """docstring for framesToTime"""
        if(self.type == SubTypesEnum.TYPE_MPL2):
            _str = str(int((int(_str)*0.1)*fps))
        
        sec = int(int(_str)/fps)

        if(sec != 0):
            tmp = str(datetime.timedelta(seconds=sec)) 
            
            if(":" in tmp[:2]):
                tmp = "0" + tmp[:1] + tmp[1:]

            return tmp + "," + str((int(_str)/fps)%sec)[2:5]
        else:
            return "00:00:00,000"
    
    def convert(self, fps=None):
        """docstring for convert"""
       
        tmp = ""
        if(self.type == SubTypesEnum.TYPE_MICRODVD):
            for i,v in enumerate(self.data.splitlines(), start=1):
                m = re.match(".*\{(\d+)\}\{(\d+)\}(.*)[\r\n]*", v)
                if(m):
                    tmp += str(i) + "\r\n" + self.convertToTime(m.group(1), fps) + " --> " + self.convertToTime(m.group(2), fps) + "\r\n" + m.group(3).replace("|", "\r\n") + "\r\n\r\n"
                #print self.framateToTime(m.group(1), fps)
            #print tmp
        elif(self.type == SubTypesEnum.TYPE_MPL2):
            for i,v in enumerate(self.data.splitlines(), start=1):
                m = re.match(".*\[(\d+)\]\[(\d+)\](.*)[\r\n]*", v)
                if(m):
                    tmp += str(i) + "\r\n" + self.convertToTime(m.group(1), fps) + " --> " + self.convertToTime(m.group(2), fps) + "\r\n" + m.group(3).replace("|", "\r\n") + "\r\n\r\n"
            
        self.type = SubTypesEnum.TYPE_SUBRIP
        self.data = tmp
