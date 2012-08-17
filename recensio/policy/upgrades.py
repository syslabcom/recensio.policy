from recensio.contenttypes.interfaces.review import IReview
from Products.CMFCore.utils import getToolByName
from recensio.contenttypes.eventhandlers import review_pdf_updated_eventhandler


def v7to8(portal_setup):
    catalog = getToolByName(portal_setup, 'portal_catalog')
    for i in catalog(object_provides=IReview.__identifier__):
        obj = i.getObject()
        review_pdf_updated_eventhandler(obj, None)
