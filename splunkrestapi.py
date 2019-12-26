from myvariables import SplunkVariables
import logging
import urllib
import httplib2
from xml.dom import minidom
import base64

class SplunkAPISearch:
    def __init__(self):
        self.SplunkBaseURL = SplunkVariables.SplunkURL
        self.SplunkLookupURL = SplunkVariables.SplunkLookupURL
        self.SplunkSearchURL = SplunkVariables.SplunkSearchURL
        self.apiuser = SplunkVariables.SplunkAPIUser
        self.apipass = SplunkVariables.SplunkAPIpass
        self.searchQuery = []
        self.ServerContent = ""
        self.sessionKey = ""
        self.AuthenticateToSplunk()
    
    def DoSearchOnSplunk(self,SplunkSearch):
        try:
            self.searchQuery = SplunkSearch
        except:
            logging.error("No SearchQuery to search for in DoSearchOnSplunk function")
            exit(1)
        if self.searchQuery == []:
            logging.error("Empty search query in DoSearchOnSplunk function")
            exit(1)
        try:
            for search in self.searchQuery:
                # Remove leading and trailing whitespace from the search
                search = search.strip()
                if not (search.startswith('search') or search.startswith("|")):
                    search = 'search ' + search
                # Do the Search
                try:
                    httplib2.Http(disable_ssl_certificate_validation=True).request(self.SplunkBaseURL + self.SplunkSearchURL,'POST',headers={'Authorization': 'Splunk %s' % self.sessionKey},body=urllib.parse.urlencode({'search': search}))[1]
                except:
                    logging.error("error in http request to search on Splunk")
                    exit(1)                
        except:
            logging.error("Cant do search on Splunk: "+search)
            exit(1)
    
    def AuthenticateToSplunk(self):
        try:
            temp = base64.b64decode(self.apipass)
            temp = str(temp,"utf-8")
            self.ServerContent = httplib2.Http(disable_ssl_certificate_validation=True).request(self.SplunkBaseURL + '/services/auth/login',
    'POST', headers={}, body=urllib.parse.urlencode({'username':self.apiuser, 'password':temp}))[1]
        except:
            logging.error("Cannot authenticate with SplunkCloud")
            exit(1)
        try:
            self.sessionKey = minidom.parseString(self.ServerContent).getElementsByTagName('sessionKey')[0].childNodes[0].nodeValue
        except:
            logging.error("Cannot get session key for Splunk")
            exit(1)

class SplunkLookupActions:
    def __init__(self):
        self.LookupFilesInString = []
        self.CSVFiles = []
        self.header = ""
        self.headerRegex = ""
        self.headerTable = ""
        self.content = ""
        self.SplunkSearch = []
    
    def CreateSplunkSearchToPushLookupFile(self,LookupFileName):
        self.SplunkSearch.append("| stats count as field1 | eval field1=\""+self.content+"\" | eval field1=split(field1,\";\") | mvexpand field1 | rex field=field1 \""+self.headerRegex+"\" | table "+self.headerTable+" | outputlookup \""+LookupFileName+"\"")

    def ModifyHeadersToRequiredVariables(self):
        for oneheader in self.header:
            try:
                if self.headerRegex == "":
                    self.headerRegex = "(?<"+oneheader+">.*)"
                else:
                    self.headerRegex = self.headerRegex+",(?<"+oneheader+">.*)"
            except:
                logging.error("Error creating Regex from header")
                exit(1)
            try:
                if self.headerTable == "":
                    self.headerTable = oneheader
                else:
                    self.headerTable = self.headerTable+","+oneheader
            except:
                logging.error("Error creating table string from header variable")
                exit(1)
            


    def pushCSVStringToLookup(self,CSVFiles,LookupFilesInString):
        self.CSVFiles = CSVFiles
        self.LookupFilesInString = LookupFilesInString
        for file in self.CSVFiles:
            self.header = ""
            self.headerRegex = ""
            self.headerTable = ""
            self.content = ""
            try:
                self.header = self.LookupFilesInString[self.CSVFiles.index(file)][0]
                self.content = self.LookupFilesInString[self.CSVFiles.index(file)][1]
            except:
                logging.error("Issue with creating header and content variables from the following file: "+file)
                logging.error("Header: "+self.header)
                logging.error("Content: "+self.content)
                exit(1)
            try:
                self.ModifyHeadersToRequiredVariables()
            except:
                logging.error("Error creating Variables from headers")
                logging.error("Header: "+self.header)
                logging.error("Content: "+self.content)
                exit(1)
            try:
                self.CreateSplunkSearchToPushLookupFile(file)
            except:
                logging.error("Error creating Splunk Search to push lookup file")
            
        
    