# *-* coding: utf-8 *-*

'''
Created on 02-02-2013

@author: miziak
'''

import sys, os

def getDir(local = False):
    if(sys.platform == "win32" or local):
        path = os.path.realpath(__file__)
        path = path[:path.rfind("/" if sys.platform != "win32" else "\\")]
        if(".exe" in path):
            path = path[:path.rfind("/" if sys.platform != "win32" else "\\")]

        return path
    else:
        return os.path.expanduser("~") + "/.napitux"
    
def completePath(path):
    last = path[len(path)-1]
    if(last != "/" or last != "\\"):
        path += "/" if sys.platform != "win32" else "\\"
    
    return path