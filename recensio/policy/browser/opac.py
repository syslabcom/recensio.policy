from Products.Five.browser import BrowserView
import urllib
import json

from recensio.policy.opacsearch import opac

class OPAC(BrowserView):
    def __call__(self, identifier):
        import pdb;pdb.set_trace()
        return json.dumps(opac.getMetadataForISBN(identifier))
