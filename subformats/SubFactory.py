# -*- coding: utf-8 -*-

from SubRip import *

class SubFactory(object):
    """docstring for SubFactory"""
    @staticmethod
    def convert(data, info=None, fps=None, totype=SubTypesEnum.TYPE_MICRODVD):
        """docstring for convert"""
        if(totype == SubTypesEnum.TYPE_SUBRIP):
            sub = SubRip(data, info, fps)
            sub.save()
