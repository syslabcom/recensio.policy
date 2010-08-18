from Products.Five.browser import BrowserView
import urllib

class OAI(BrowserView):
    def __call__(self, identifier):
        return urllib.urlopen('http://www.nature.com/oai/request?verb=GetRecord&metadataPrefix=oai_dc&identifier=' + identifier).read()
