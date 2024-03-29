# -*- coding: utf-8 -*-
from collective.solr.interfaces import ISolrConnectionConfig
from logging import getLogger
from plone.app.controlpanel.security import SecurityControlPanelAdapter
from Products.Archetypes.interfaces.base import IBaseFolder
from Products.ATVocabularyManager.utils.vocabs import createSimpleVocabs
from Products.CMFCore.utils import getToolByName
from Products.LinguaPlone.utils import linkTranslations
from recensio.policy.interfaces import IDiscussionCollections
from recensio.policy.interfaces import INewsletterSource
from zExceptions import BadRequest
from zope.component import queryUtility
from zope.interface import directlyProvides

import constants
import os


log = getLogger("recensio.policy.setuphandlers.py")

mdfile = os.path.join(os.path.dirname(__file__), "profiles", "default", "metadata.xml")

imported_content = [
    "autoren",
    "ueberuns",
    "themen-epochen-regionen",
    "faq",
    "presse",
    "images",
    "RSS-feeds",
    "beste-kommentare",
    "rezensionen",
    "front-page",
    "praesentationen",
]

PROFILE_ID = "profile-recensio.policy:default"


def guard(func):
    def wrapper(self):
        if self.readDataFile("recensio.policy_marker.txt") is None:
            return
        return func(self)

    return wrapper


def guard_voc(func):
    def wrapper(self):
        if self.readDataFile("recensio.policy_marker_voc.txt") is None:
            return
        return func(self)

    return wrapper


@guard_voc
def importVocabularies(self):
    path_tmpl = "../../../../vocabularies/ddc_%s"
    site = self.getSite()
    pvm = getToolByName(site, "portal_vocabularies")
    for (filenamepart, vocabname) in (
        ("geo.vdex", "region_values"),
        ("geo_bsb.vdex", "region_values_bsb"),
        ("sach.vdex", "topic_values"),
        ("zeit.vdex", "epoch_values"),
    ):
        if vocabname not in pvm:
            file_data = self.readDataFile(path_tmpl % filenamepart)
            if file_data is not None:
                pvm.invokeFactory("VdexFileVocabulary", vocabname)
                pvm[vocabname].importXMLBinding(file_data)
                pvm[vocabname].showLeafsOnly = False
    for vocab_name, vocabulary in constants.vocabularies.items():
        if not hasattr(pvm, vocab_name):
            createSimpleVocabs(pvm, {vocab_name: vocabulary.items()})


@guard
def configureSecurity(self):
    site = self.getSite()
    pcp = SecurityControlPanelAdapter(site)
    pcp.set_enable_self_reg(True)
    pcp.set_enable_user_pwd_choice(False)
    pcp.set_enable_user_folders(True)


@guard
def activateSolr(self):
    manager = queryUtility(ISolrConnectionConfig)
    manager.active = True
    manager.facets = [u"portal_type", u"ddcPlace", "ddcTime", "ddcSubject"]
    manager.required = []


@guard
def activateTestSolr(self):
    manager = queryUtility(ISolrConnectionConfig)
    manager.port = 8984


@guard
def activateDemoSolr(self):
    manager = queryUtility(ISolrConnectionConfig)
    manager.port = 8985


@guard
def setPermissions(self):
    user_folder = self.getSite().Members
    user_folder.manage_setLocalRoles("Reviewers", ["Reader"])


@guard
def testSetUpCollections(context):
    """
    This step was originally used to set up the recensio site.
    This step is not safe to be executed many times, so we just deactivated
    it.
    It is now used for tests!
    """
    portal = context.getSite()
    wftool = getToolByName(portal, "portal_workflow")

    def getOrAdd(context, type, name, publish=True):
        if name not in context.objectIds():
            context.invokeFactory(type, name)
            new_object = context[name]
            new_object.setLanguage("")
            if publish:
                wftool.doActionFor(new_object, "publish")
        return context[name]

    def configureCollection(collection, types, location):
        try:
            criterion = collection.addCriterion(
                field="created", criterion_type="ATFriendlyDateCriteria"
            )
            criterion.setValue(31)
            criterion.setOperation("less")
            criterion.setDateRange("-")
        except BadRequest:
            pass
        try:
            criterion = collection.addCriterion(
                field="portal_type", criterion_type="ATPortalTypeCriterion"
            )
            criterion.setValue(types)
        except BadRequest:
            pass
        try:
            criterion = collection.addCriterion(
                field="Language", criterion_type="ATSimpleStringCriterion"
            )
            criterion.setValue("all")
        except BadRequest:
            pass
        try:
            criterion = collection.addCriterion(
                field="modified", criterion_type="ATSortCriterion"
            )
        except BadRequest:
            pass

    classic_reviews = (u"Review Monograph", u"Review Journal")
    self_reviews = (
        u"Presentation Collection",
        u"Presentation Article Review",
        u"Presentation Online Resource",
        u"Presentation Monograph",
    )

    feeds = getOrAdd(portal, "Folder", "RSS-feeds")
    feeds.setTitle(u"RSS feeds")
    feeds.reindexObject()
    directlyProvides(feeds, INewsletterSource)
    new_reviews = getOrAdd(feeds, "Topic", "new_reviews")
    new_reviews.setTitle(u"Neue Rezensionen")
    new_reviews.reindexObject()
    configureCollection(new_reviews, classic_reviews, "/")
    uncommented = getOrAdd(feeds, "Topic", "discussion_three_months_old")
    uncommented.setTitle(
        "Für Besucher unsichtbar, Presentationen genau 3 Monate alt. Für interne Zwecke gedacht"
    )
    configureCollection(uncommented, self_reviews, "/")
    crit = uncommented["crit__created_ATFriendlyDateCriteria"]
    crit.setValue(90)
    crit.setOperation("within_day")
    new_self_reviews = getOrAdd(feeds, "Topic", "new_presentations")
    new_self_reviews.setTitle(u"Neue Präsentationen")
    new_self_reviews.reindexObject()
    configureCollection(new_self_reviews, self_reviews, "/")
    new_discussions = getOrAdd(feeds, "Topic", "new_discussions")
    new_discussions.setTitle(u"Neue Diskussionen")
    new_discussions.reindexObject()
    directlyProvides(new_discussions, IDiscussionCollections)
    try:
        criterion = new_discussions.addCriterion(
            field="last_comment_date", criterion_type="ATFriendlyDateCriteria"
        )
        criterion.setValue(31)
        criterion.setOperation("less")
        criterion.setDateRange("-")
    except BadRequest:
        pass

    internal_views = getOrAdd(portal, "Folder", "internal views", publish=False)
    internal_views.setExcludeFromNav("True")
    digitool_export = getOrAdd(internal_views, "Topic", "Digitool Export")
    configureCollection(
        digitool_export,
        tuple(
            set(classic_reviews + self_reviews) - set((u"Presentation Online Resource",))
        ),
        "/",
    )
    criterion = digitool_export.getCriterion("created_ATFriendlyDateCriteria")
    criterion.setValue(1)


@guard
def addWorkflowScriptsForComments(context):
    script = """
browser_view = info.object.restrictedTraverse('@@notify_author_new_comment')
browser_view()
"""
    addWorkflowScripts(
        context,
        wf_name="comment_review_workflow",
        script_name="send_notification",
        script_contents=script,
        after_transitions_to_hook_in=["publish"],
    )


def addWorkflowScripts(
    context, wf_name, script_name, script_contents, after_transitions_to_hook_in
):
    portal_workflow_tool = getToolByName(context.getSite(), "portal_workflow")
    workflow = getattr(portal_workflow_tool, wf_name)
    wf_scripts = workflow.scripts
    if not getattr(wf_scripts, script_name, None):
        wf_scripts.manage_addProduct["PythonScripts"].manage_addPythonScript(
            id=script_name
        )
    params = "info"
    script = getattr(wf_scripts, script_name)
    script.ZPythonScript_edit(params, script_contents)

    for transition_id in after_transitions_to_hook_in:
        transition = getattr(workflow.transitions, transition_id)
        transition.after_script_name = script_name


@guard
def addCatalogIndexes(context):
    site = context.getSite()
    cat = getToolByName(site, "portal_catalog")

    class extra(object):
        def __init__(self, field_name, lexicon_id, index_type, doc_attr=""):
            self.field_name = field_name
            self.lexicon_id = lexicon_id
            self.index_type = index_type
            self.doc_attr = doc_attr

    def addIndex(name, type, **kw):
        if not name in cat.indexes():
            log.debug("adding %s %s, kw=%s" % (type, name, kw))
            cat.addIndex(name, type, **kw)
        elif (
            not filter(lambda x: x.getId() == name, cat.getIndexObjects())[0].meta_type
            == type
        ):
            cat.delIndex(name)
            log.debug("adding %s %s, kw=%s" % (type, name, kw))
            cat.addIndex(name, type, **kw)

    def addColumn(name):
        if not name in cat.schema():
            log.debug("adding metadata %s" % name)
            cat.addColumn(name)

    addIndex("languageReviewedText", "KeywordIndex")
    addIndex("languageReview", "KeywordIndex")
    addIndex("ddcPlace", "FieldIndex")
    addIndex("ddcTime", "FieldIndex")
    addIndex("ddcSubject", "FieldIndex")
    addIndex("authors", "KeywordIndex", extra={"indexed_attrs": ["getAllAuthorData"]})
    addIndex(
        "authorsFulltext",
        "ZCTextIndex",
        extra=extra(
            field_name="getAllAuthorDataFulltext",
            doc_attr="getAllAuthorDataFulltext",
            lexicon_id="plone_lexicon",
            index_type="Okapi BM25 Rank",
        ),
    )
    addIndex(
        "titleOrShortname",
        "ZCTextIndex",
        extra=extra(
            field_name="titel,subtitle,shortnameJournal",
            lexicon_id="plone_lexicon",
            index_type="Okapi BM25 Rank",
        ),
    )
    addIndex(
        "year",
        "FieldIndex",
        extra={"indexed_attrs": ["yearOfPublication", "officialYearOfPublication"]},
    )
    addIndex("place", "FieldIndex", extra={"indexed_attrs": ["placeOfPublication"]})
    addIndex(
        "publisher",
        "ZCTextIndex",
        extra=extra(
            field_name="publisher",
            lexicon_id="plone_lexicon",
            index_type="Okapi BM25 Rank",
        ),
    )
    addIndex(
        "series",
        "ZCTextIndex",
        extra=extra(
            field_name="series",
            lexicon_id="plone_lexicon",
            index_type="Okapi BM25 Rank",
        ),
    )
    addIndex("isbn", "FieldIndex")
    addIndex("recensioID", "FieldIndex")

    addColumn("getAuthors")
    addColumn("listAuthors")
    addColumn("getReviewAuthorFirstname")
    addColumn("getReviewAuthorLastname")
    addColumn("getYearOfPublication")
    addColumn("getOfficialYearOfPublication")
    addColumn("punctuated_title_and_subtitle")


@guard
def hideAllFolders(context):
    hideAllFoldersUnguarded(context)


def hideAllFoldersUnguarded(context):
    """Unguarded version, so that it can also be called from
    the recencio.contenttypes example_content profile."""
    site = context.getSite()
    for id in ["Members", "news", "events", "imports", "RSS-feeds", "images"]:
        ob = getattr(site, id, None)
        if ob:
            ob.setExcludeFromNav(True)
            ob.reindexObject()


@guard
def setupHomepage(context):
    site = context.getSite()
    for fp_id in ["front-page", "front-page-en", "front-page-fr"]:
        fp = getattr(site, fp_id, None)
        if not fp:
            log.warning("%s not found" % fp_id)
            continue
        id = "layout"
        if fp.hasProperty(id):
            fp._delProperty(id)
        fp._setProperty(id=id, value="homepage-view", type="string")
        log.debug("Homepage view was set on the front page")


@guard
def setViewsOnFolders(context):
    setViewsOnFoldersUnguarded(context)


def setViewsOnFoldersUnguarded(context):
    """Unguarded version, so that it can also be called from
    the recencio.contenttypes example_content profile."""
    portal = context.getSite()

    for autoren_id in ["autoren", "autoren-en", "autoren-fr"]:
        autoren = getattr(portal, autoren_id, None)
        if not autoren:
            log.warning(
                'Folder "%s" not found on portal. Please run recensio.contenttypes.initial_content'
                % autoren_id
            )
        else:
            fp = getattr(autoren, "index_html")
            id = "layout"
            if fp.hasProperty(id):
                fp._delProperty(id)
            fp._setProperty(id=id, value="authorsearch", type="string")

    for themen_id in [
        "themen-epochen-regionen",
        "themen-epochen-regionen-en",
        "themen-epochen-regionen-fr",
    ]:
        themen = getattr(portal, themen_id, None)
        if not themen:
            log.warning(
                'Folder "%s" not found on portal. Please run recensio.contenttypes.initial_content'
                % themen_id
            )
        else:
            fp = getattr(themen, "index_html")
            id = "layout"
            if fp.hasProperty(id):
                fp._delProperty(id)
            fp._setProperty(id=id, value="browse-topics", type="string")

    rezensionen = getattr(portal, "rezensionen", None)
    if not rezensionen:
        log.warning(
            'Folder "rezensionen " not found on portal. Please run recensio.contenttypes.initial_content'
        )
    else:
        fp = rezensionen
        id = "default_page"
        if fp.hasProperty(id):
            fp._delProperty(id)
        fp._setProperty(id=id, value="zeitschriften", type="string")

    zeitschriften = getattr(rezensionen, "zeitschriften", None)
    if not zeitschriften:
        log.warning(
            'Folder "zeitschriften" not found on portal. Please run recensio.contenttypes.initial_content'
        )
    else:
        fp = zeitschriften
        id = "layout"
        if fp.hasProperty(id):
            fp._delProperty(id)
        fp._setProperty(id=id, value="publications-view", type="string")


def doSetLanguage(obj, language):
    obj.setLanguage(language)
    if IBaseFolder.providedBy(obj):
        for item in obj.objectValues():
            doSetLanguage(item, language)


@guard
def setImportedContentLanguages(context):
    portal = context.getSite()
    for id in imported_content:
        language = "de"
        ob = portal.unrestrictedTraverse(id, None)
        if not ob:
            log.warning(
                'Object %s not found. Please run import step "Recensio'
                ' initial content"' % (id)
            )
            continue
        if id in ["images"]:
            language = ""
            doSetLanguage(ob, language)

        def translate_folder(path, language, path_trans, lang_trans):
            ob = portal.unrestrictedTraverse(path, None)
            ob_trans = portal.unrestrictedTraverse(path_trans, None)
            for item in ob.objectIds():
                subob = ob.unrestrictedTraverse(item, None)
                subob_trans = ob_trans.unrestrictedTraverse(item, None)
                if not subob_trans:
                    log.warning(
                        "Object %s not found. No translation for %s "
                        "will be set" % ("/".join(path_trans + [item]), lang_trans)
                    )
                else:
                    if not subob.hasTranslation(lang_trans):
                        linkTranslations(
                            portal,
                            [
                                [
                                    (path + [item], language),
                                    (path_trans + [item], lang_trans),
                                ]
                            ],
                        )
                        log.debug(
                            "Setting translation for %s (%s): %s (%s)"
                            ""
                            % (path + [item], language, path_trans + [item], lang_trans)
                        )
                    else:
                        log.warning(
                            "%s is already translated into %s!"
                            % ("/".join(path + [item]), lang_trans)
                        )
                    if subob and subob.portal_type == "Folder":
                        translate_folder(
                            path + [item], language, path_trans + [item], lang_trans
                        )

        if language:
            for lang_trans in ["en", "fr"]:
                id_trans = id + "-" + lang_trans
                ob_trans = portal.unrestrictedTraverse(id_trans, None)
                if ob_trans:
                    if not ob.hasTranslation(lang_trans):
                        linkTranslations(
                            portal, [[([id], language), ([id_trans], lang_trans)]]
                        )
                    else:
                        log.warning(
                            "%s is already translated into %s!" % (id, lang_trans)
                        )
                    if ob.portal_type == "Folder":
                        translate_folder([id], language, [id_trans], lang_trans)
                else:
                    log.warning(
                        "Object %s not found. No translation for %s "
                        "will be set" % (id_trans, lang_trans)
                    )
    portal.setLanguage("de")


def doPublish(obj, pwt):
    try:
        pwt.doActionFor(obj, "publish")
        obj.reindexObject()
    except:
        log.info("Could not publish %s" % obj.absolute_url())


@guard
def publishImportedContent(context):
    portal = context.getSite()
    pwt = getToolByName(portal, "portal_workflow")
    for id in imported_content:
        for lang in ["", "-en", "-fr"]:
            obj = getattr(portal, (id + lang), None)
            if not obj:
                log.warning(
                    "Object %s not found. Please run import step "
                    '"Recensio initial content"' % (id + lang)
                )
                continue
            doPublish(obj, pwt)


@guard
def fixPortalTabs(self):
    """Remove index_html from the default portal_actions/portal_tabs"""
    site = self.getSite()
    pat = getToolByName(site, "portal_actions")
    tabs = pat.get("portal_tabs")
    if tabs and "index_html" in tabs.objectIds():
        tabs.manage_delObjects("index_html")
