# *-* coding: utf-8 *-*

'''
Created on 13-12-2012

@author: miziak
'''

import urllib, urllib2, base64, md5, StringIO, sys
from xml.dom import minidom

class NapiProjekt(object):
    def __init__(self, file):
        self.info = {}
        self.name = file
        self.url = "http://napiprojekt.pl/api/api-napiprojekt3.php"
        
        sum = md5.new()
        sum.update(open(file, 'rb').read(10485760))
        self.md5hash = sum.hexdigest()
		
    def downloadSubtitles(self, eng = False):
        values = {
            "mode":"1",
            #"client":"NapiTux",
            "client":"NapiProjektPython",
            "client_ver":"0.1",
            "downloaded_subtitles_id":self.md5hash,
            "downloaded_subtitles_txt":"1",
            "downloaded_subtitles_lang":"PL"
        }
        
        if(eng):
            values["downloaded_subtitles_lang"] = "ENG"
        
        data = urllib.urlencode(values)
        #req = urllib2.Request(self.url, data)
        try:
            #response = urllib2.urlopen(req)
			response = urllib.urlopen(self.url, data)
        except urllib2.URLError, e:
            sys.stderr.write(e.message)
            return False

        try:
            DOMTree = minidom.parseString(response.read())
            cNodes = DOMTree.childNodes
            if(cNodes[0].getElementsByTagName("status") != []):
                open(self.name[:self.name.rfind(".")] + ".txt", "w").write(base64.b64decode(cNodes[0].getElementsByTagName("subtitles")[0].getElementsByTagName("content")[0].childNodes[0].data))
                return True
        except Exception, e:
            return False
        
        return False
    
    def getMoreInfo(self):
        values = {
            "mode":"32770",
            #"client":"NapiTux",
            "client":"NapiProjektPython",
            "client_ver":"0.1",
            "downloaded_cover_id":self.md5hash,
            "VideoFileInfoID":self.md5hash
        }
        
        data = urllib.urlencode(values)
        #req = urllib2.Request(self.url, data)
        try:
            #response = urllib2.urlopen(req)
			response = urllib.urlopen(self.url, data)
        except urllib2.URLError, e:
            sys.stderr.write(e.message)
            return False

        try:
            #print response.read()
            DOMTree = minidom.parseString(response.read())
            cNodes = DOMTree.childNodes[0].getElementsByTagName("movie")
            
            if(cNodes[0].getElementsByTagName("status") != []):
                self.info["title"] = cNodes[0].getElementsByTagName("title")[0].childNodes[0].data
                self.info["year"] = cNodes[0].getElementsByTagName("year")[0].childNodes[0].data
                self.info["country"] = cNodes[0].getElementsByTagName("country")[0].getElementsByTagName("pl")[0].childNodes[0].data
                if(cNodes[0].getElementsByTagName("genre")[0].getElementsByTagName("pl")[0].childNodes != []):
                    self.info["genre"] = cNodes[0].getElementsByTagName("genre")[0].getElementsByTagName("pl")[0].childNodes[0].data
                else:
                    self.info["genre"] = "Niepodany!"
                
                self.info["filmweb"] = cNodes[0].getElementsByTagName("direct_links")[0].getElementsByTagName("filmweb_pl")[0].childNodes[0].data
                self.info["cover"] = StringIO.StringIO(base64.b64decode(cNodes[0].getElementsByTagName("cover")[0].childNodes[0].data))
                
                cNodes = DOMTree.childNodes[0].getElementsByTagName("file_info")
                
                self.info["size"] = cNodes[0].getElementsByTagName("rozmiar_pliku_z_jednostka")[0].childNodes[0].data
                self.info["duration"] = cNodes[0].getElementsByTagName("czas_trwania_sformatowany")[0].childNodes[0].data
                self.info["resolution"] = cNodes[0].getElementsByTagName("rozdz_X")[0].childNodes[0].data + "x" + cNodes[0].getElementsByTagName("rozdz_Y")[0].childNodes[0].data
                self.info["fps"] = cNodes[0].getElementsByTagName("fps")[0].childNodes[0].data
        except Exception, e:
			sys.stderr.write(e.message)
			return False

