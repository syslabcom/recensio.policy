import random

from zope.interface import implements
from zope.viewlet.interfaces import IViewlet

from Products.CMFCore.utils import getToolByName

from recensio.policy.utility import getSelectedQuery

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

    @property
    def drill_down_views(self):
        vocabulary = getToolByName(self.context, 'portal_vocabularies')
        if not hasattr(self.context, 'themen-epochen-regionen'):
            return []
        getUrl = lambda x: '?'.join([\
            getattr(self.context, 'themen-epochen-regionen').absolute_url(), \
            getSelectedQuery({'ddcTime' : [vocabulary['epoch_values'][x].getTermKey()]})])
        views = [{'title' : 'Alte Geschichte', 'url' : getUrl('old history')}
                ,{'title' : 'Mittelalter', 'url' : getUrl('middle_age')}
                ,{'title' : 'Neuzeit bis 1900', 'url' : getUrl('modern_age_until_1900')}
                ,{'title' : '20. Jahrhundert', 'url' : getUrl('20_century')}
                ,{'title' : '21. Jahrhundert', 'url' : getUrl('21_century')}]
        return views
