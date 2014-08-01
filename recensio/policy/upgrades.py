from plone.app.controlpanel.skins import ISkinsSchema
from Products.CMFCore.utils import getToolByName
from recensio.contenttypes.eventhandlers import review_pdf_updated_eventhandler
from recensio.contenttypes.interfaces.review import IReview
from transaction import commit
import pkg_resources
from logging import getLogger


log = getLogger(__name__)


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
    """
    Please be careful, conversions have to be done in a specific order.
    """
    portal = getToolByName(portal_setup, 'portal_url').getPortalObject()
    cat = getToolByName(portal, 'portal_catalog')

    pvm = getToolByName(portal, 'portal_vocabularies')
    path_tmpl = '../../vocabularies/ddc_%s'
    for (filenamepart, vocabname) in (('geo.vdex', 'region_values'),
                                      ('sach.vdex', 'topic_values'),
                                      ('zeit.vdex', 'epoch_values')):
        pvm[vocabname].importXMLBinding(pkg_resources.resource_string(
            __name__, path_tmpl % filenamepart))

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
        "400": "417.7",
        "390": None,
        "902": "907.2"
    }

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

    sach_mappings = {
        "43.0": "43",
        "44.68": "44.69",
        "44.69": "44.70",
        "51.0": "51",
        "52.0": "52",
        "54.0": "54",
        "56.0": "56",
        "57.0": "57",
        "58.0": "58",
        "59.0": "59",
        "61.0": "61",
        "62.0": "62",
        "63.0": "63",
        "64.0": "64",
        "65.0": "65",
        "66.0": "66",
        "67.0": "67",
        "68.0": "68",
    }

    for doc in all_docs:
        for old, new in sache_mappings.items():
            if old in doc.ddcSubject:
                if new:
                    new_list = [new] + list(doc.ddcSubject)
                else:
                    new_list = list(doc.ddcSubject)
                new_list.remove(old)
                doc.ddcSubject = tuple(set(new_list))
                changed_docs.append(doc)
        for old, news in zeit_mappings.items():
            if old in doc.ddcTime:
                if not isinstance(news, list):
                    news = [news]
                new_list = list(doc.ddcTime)
                new_list.remove(old)
                for new in news:
                    new_list = new_list + [new]
                doc.ddcTime = tuple(set(new_list))
                changed_docs.append(doc)
        for old, new in sach_mappings.items():
            if old in doc.ddcPlace:
                new_list = [new] + list(doc.ddcPlace)
                new_list.remove(old)
                doc.ddcPlace = tuple(set(new_list))
                changed_docs.append(doc)

    for doc in documents_containing_909:
        doc.ddcPlace = tuple(set(doc.ddcPlace + tuple('909')))

    log.warning("To 10 Migration migrated %i documents",
                len(set(changed_docs)))

    for doc in list(set(changed_docs)):
        doc.reindexObject()


def v10to11(portal_setup):
    portal_setup.runImportStepFromProfile(
        'profile-recensio.policy:default',
        'propertiestool')
