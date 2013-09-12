# -*- coding: utf-8 -*-

import sys, re


class CmdParser(object):
    """Class parsing input cmd options."""
    def __init__(self, name, usage, version):
       self.name = name
       self.usage = usage
       self.version = version
       self.values_dict = {}
       self.options_dict = {}
       self.options_dict[name] = ("h", "help", "exist", "show help", False)

    def addOpt(self, name, flag, exflag, action, help, default):
        """addOpt method add new flag to parser"""
        self.options_dict[name] = (flag, exflag, action, help, default)
        if(default != None):
            self.values_dict[name] = default

    def praseCmd(self):
        """praseCmd method prase input options to output dict"""
        opt = sys.argv[1:]
        
        flag = []
        while(opt):
            it = opt[0]
            if(it[0] == "-" and it[1] != "-" and not flag):
                for c in it[1:]:
                    throw = True
                    for i,v in self.options_dict.iteritems():
                        if(c == v[0]):
                            if(v[2] == "exist"):
                                self.values_dict[i] = True
                                throw = False
                            else:
                                flag.append(i)
                                throw = False

                            break
                        elif(c == "h"):
                            print self.name + " v" + self.version + "\n" + self.usage
                            print "Options:\n"
                            for i in self.options_dict.itervalues():
                                print "\t-" + i[0] + "  --" + i[1] + "\t" + i[3]

                            return
                        
                    if(throw):
                        raise Exception("Unknown option " + it + "!")

                for i in range(0, len(flag)):
                    self.values_dict[flag[i]] = opt[1:][i]

                opt = opt[len(flag)+1:]
                flag = []
            elif(it[0:2] == "--"):
                m = re.match(r"--(.*)=(.*)", it)
                throw = True
                for i,v in self.options_dict.iteritems():
                    if(m.group(1) == v[1]):
                        self.values_dict[i] = m.group(2)
                        opt = opt[1:]
                        throw = False
                        break
                
                if(throw):
                    raise Exception("Unknown option --" + m.group(1) + "!")
            else:
                raise Exception("Unknown option " + it + "!")
