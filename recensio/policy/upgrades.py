from Products.CMFCore.utils import getToolByName
from transaction import commit

from recensio.contenttypes.eventhandlers import review_pdf_updated_eventhandler
from recensio.contenttypes.interfaces.review import IReview


def v7to8(portal_setup):
    catalog = getToolByName(portal_setup, 'portal_catalog')
    for count, brain in enumerate(catalog(
        object_provides=IReview.__identifier__)):
        try:
            obj = brain.getObject()
            try:
                if hasattr(obj, 'pagePicutes') and len(obj.pagePictures):
                    len(obj.pagePictures[0])
                    continue
                else:
                    continue
            except TypeError:
                pass
            review_pdf_updated_eventhandler(obj, None)
        except AttributeError:
            pass
        if not count % 20:
            commit()
