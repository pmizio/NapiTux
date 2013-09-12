# -*- coding: utf-8 -*-

import os, re

class SubTypesEnum(object):
    """docstring for TypesEnum"""
    TYPE_NONE = 0
    TYPE_MICRODVD = 1
    TYPE_SUBRIP = 2
    TYPE_MPL2 = 3

class Subtitles(object):
    """docstring for Subtitles"""
    
    def __init__(self, data, info = None):
        self.info = info
        if(os.path.isfile(data)):
            f = open(data, "r")
            self.data = f.read()
            f.close()
        else:
            self.data = data

        self.type = self.getType()
        
    def getType(self):
        """docstring for getType"""
        #print repr(self.data)
        if(re.match(".*\d+\r?\n\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d.*", self.data)):
            return SubTypesEnum.TYPE_SUBRIP
        elif(re.match(".*\{\d+\}\{\d+\}.*", self.data)):
            return SubTypesEnum.TYPE_MICRODVD
        elif(re.match(".*\[\d+\]\[\d+\].*", self.data)):
            return SubTypesEnum.TYPE_MPL2
            
        return SubTypesEnum.TYPE_NONE

    def save(self):
        """docstring for save"""
        f = open("test.srt", "w")
        f.write(self.data)
        f.close()
"""
    def framateToTime(self, framate_str, fps):
        docstring for framesToTime
        sec = int(int(framate_str)/fps)
        if(sec != 0):
            tmp = str(datetime.timedelta(seconds=sec)) 
            
            if(":" in tmp[:2]):
                tmp = "0" + tmp[:1] + tmp[1:]

            return tmp + "," + str((int(framate_str)/fps)%sec)[2:5]
        else:
            return "00:00:00,000"
"""


"""
        tmp = ""
        if(self.type == SubTypesEnum.TYPE_MICRODVD and target == SubTypesEnum.TYPE_SUBRIP):
            for i,v in enumerate(self.data.splitlines(), start=1):
                m = re.match(".*\{(\d+)\}\{(\d+)\}(.*)[\r\n]*", v)
                tmp += str(i) + "\r\n" + self.framateToTime(m.group(1), fps) + " --> " + self.framateToTime(m.group(2), fps) + "\r\n" + m.group(3).replace("|", "\r\n") + "\r\n\r\n"
                #print self.framateToTime(m.group(1), fps)
            #print tmp

        self.type = target
        self.data = tmp

"""

