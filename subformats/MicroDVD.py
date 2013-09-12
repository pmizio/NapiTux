# -*- coding: utf-8 -*-

import re
from Subtitles import *

class MicroDVD(Subtitles):
    """docstring for MicroDVD"""
    def __init__(self, data, info = None, fps = None):
        super(MicroDVD, self).__init__(data, info)
        
        print self.type

        if(self.type != SubTypesEnum.TYPE_MICRODVD):
            if(info != None):
                self.convert(float(info["fps"]))
            else:
                self.convert(fps)
    
    def secToFramate(self, sec, fps):
        """docstring for secToFramate"""
        return str(int(sec * fps))

    def convert(self, fps=None):
        """docstring for convert"""
       
        tmp = ""
        if(self.type == SubTypesEnum.TYPE_MPL2):
            for v in self.data.splitlines():
                m = re.match(".*\[(\d+)\]\[(\d+)\](.*)[\r\n]*", v)
                if(m):
                    tmp += "{" + self.secToFramate(int(m.group(1))*0.1, fps) + "}{" + self.secToFramate(int(m.group(2))*0.1, fps) + "}" + m.group(3) + "\r\n"

        self.type = SubTypesEnum.TYPE_MICRODVD
        self.data = tmp
