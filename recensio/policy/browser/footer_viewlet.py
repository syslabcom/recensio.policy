import random

from zope.interface import implements
from zope.viewlet.interfaces import IViewlet

from plone.app.layout.viewlets import ViewletBase

class Footer(ViewletBase):
    implements(IViewlet)

    def getPublications(self):
        portal = self.context.portal_url.getPortalObject()
        rezensionen = getattr(portal, 'rezensionen', None)
        zeitschriften = getattr(rezensionen, 'zeitschriften', None)
        if zeitschriften:
            pubs = [x for x in zeitschriften.objectValues() if \
                x.portal_type=='Publication']
            random.shuffle(pubs)
            return pubs
        else:
            return []
