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
            self.name = data
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
        f = open(self.name[:-4] + ".srt", "w")
        f.write(self.data)
        f.close()
