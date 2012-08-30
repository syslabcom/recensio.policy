from Products.CMFCore.utils import getToolByName
from transaction import commit
from plone.app.controlpanel.skins import ISkinsSchema
from recensio.contenttypes.eventhandlers import review_pdf_updated_eventhandler
from recensio.contenttypes.interfaces.review import IReview


def v7to8(portal_setup):
    catalog = getToolByName(portal_setup, 'portal_catalog')
    for count, brain in enumerate(catalog(
        object_provides=IReview.__identifier__)):
        try:
            obj = brain.getObject()
            try:
                if hasattr(obj, 'pagePictures') and len(obj.pagePictures):
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

def v8to9(portal_setup):
    # activate popup forms
    portal = getToolByName(portal_setup, 'portal_url').getPortalObject()
    skins = ISkinsSchema(portal)
    skins.set_use_popups(True)

    # show folder_contents tab on translations
    portal_actions = getToolByName(portal, 'portal_actions')
    folderContents = portal_actions['object']['folderContents']
    folderContents.manage_changeProperties(
        available_expr="python: object.displayContentsTab() "
            "or True in [tr[0].restrictedTraverse('@@plone').isDefaultPageInFolder() "
                       "for tr in object.getTranslations().values()]")
