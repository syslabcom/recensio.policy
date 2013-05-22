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


def v9to10(portal_setup):
    #XXX 909 soll von Sache zu Raum werden
    #
    #
    portal = getToolByName(portal_setup, 'portal_url').getPortalObject()
    cat = getToolByName(portal, 'portal_catalog')
    all_docs = [x.getObject() for x in
                cat(object_provides="recensio.contenttypes.interfaces.review.IReview",
                    b_size=100000) if x]
    changed_docs = []

    documents_containing_909 = [x for x in all_docs if '909' in x.ddcSubject]
    for doc in documents_containing_909:
        doc.ddcSubject = tuple([x for x in doc.ddcSubject if x != '909'])
        changed_docs.append(doc)

    sache_mappings = {
        "920": "929",  # Familiengeschichte, Genealogie (Stammtafeln, Insignien, Heraldik, Sphragistik, Namenkunde)
        "902.8": "907.2",  # Historische Hilfswissenschaften
        "902.85": "902.8",  # Gestrichen
        "001.09 (alt: 109)": "001.09",  # ...
        "700.9": "709",  # Kunstgeschichte
        "800.09": "809",  # Literaturgeschichte
        "320.9": "909",  # Politikgeschichte
        "300.9": "306.09",  # Sozial un Gesellschaftsgeschichte
    }
    for doc in all_docs:
        for old, new in sache_mappings.items():
            if old in doc.ddcSubject:
                new_list = [new] + list(doc.ddcSubject)
                new_list.pop(old)
                doc.ddcSubject = tuple(set(new_list))
                changed_docs.append(doc)

    zeit_mappings = {
        "t1:0901": "0901",
        "t1:09012": "09012",
        "t1:09013": "09013",
        "t1:09014": "09014",
        "t1:09015": "09015",
        "t1:0902": "0902",
        "t1:09021": "09021",
        "t1:09022": "09022",
        "t1:09023": "09023",
        "t1:09024": "09024",
        "t1:0903": "0903",
        "t1:09031": "09031",
        "t1:09032": "09032",
        "t1:09033": "09033",
        "t1:09034": "09034",
        "t1:0904": "0904",
        "t1:09040": ["09041", "09042", "09043", "09044"],
        "t1:09041": "09041",
        "t1:09042": "09042",
        "t1:09043": "09043",
        "t1:09044": "09044",
        "t1:090441": ["09045", "09046", "09047", "09048", "09049"],
        "t1:09045": "09045",
        "t1:09046": "09046",
        "t1:09047": "09047",
        "t1:09048": "09048",
        "t1:09049": "09049",
        "t1:0905": "0905",
        "t1:09051": "090511",
    }

    for doc in all_docs:
        for old, news in zeit_mappings.items():
            if old in doc.ddcTime:
                if not isinstance(news, list):
                    news = [news]
                for new in news:
                    new_list = [new] + list(doc.ddcTime)
                    new_list.pop(old)
                    doc.ddcTime = tuple(set(new_list))
                changed_docs.append(doc)

    for doc in documents_containing_909:
        doc.ddcPlace = tuple(set(doc.ddcPlace + tuple('909')))

    for doc in list(set(changed_docs)):
        doc.reindexObject()
