# -*- coding: utf-8 -*-
from AccessControl.Permission import Permission
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility, queryUtility
from zope.interface import directlyProvides
from plone.contentratings.interfaces import IRatingCategoryAssignment
from logging import getLogger
from Products.ATVocabularyManager.utils.vocabs import createSimpleVocabs,\
    createHierarchicalVocabs
import transaction
import constants
import os
from zExceptions import BadRequest
from plone.registry.interfaces import IRegistry
from plone.app.controlpanel.security import SecurityControlPanelAdapter
from recensio.policy.interfaces import IDiscussionCollections, INewsletterSource
from recensio.policy.interfaces import IRecensioSettings
from plone.portlets.interfaces import IPortletManager, ILocalPortletAssignmentManager
from plone.portlets.constants import CONTEXT_CATEGORY
from plone.app.portlets.utils import assignment_mapping_from_key
from plone.portlet.static import static
from Products.Archetypes.interfaces.base import IBaseFolder


from collective.solr.interfaces import ISolrConnectionConfig

log = getLogger('recensio.policy.setuphandlers.py')

mdfile = os.path.join(os.path.dirname(__file__), 'profiles', 'default',
    'metadata.xml')

imported_content = ['ansprechpartner', 'autoren', 'benutzerrichtlinien', 'copyright',
        'konzept', 'mitmachen-bei-recensio.net', 'themen-epochen-regionen',
        'zeitschriften', 'zitierhinweise', 'images']

portlet_hp_text = u"""<h2>Auf recensio.net …</h2>
<p>… publizieren Zeitschriftenredaktionen, die bislang im Druck veröffentlichen,
ihre Rezensionsteile online als Pre- oder Post-Prints (»Rezensionen«)</p>
<p>… präsentieren Autoren die Kernthesen ihrer Monographien und Aufsätze (»Präsentationen«).
Nutzerkommentare lassen »lebendige Rezensionen« entstehen.</p>"""

def guard(func):
    def wrapper(self):
        if self.readDataFile('recensio.policy_marker.txt') is None:
            return
        return func(self)
    return wrapper

@guard
def importVocabularies(self):
    site = self.getSite()
    pvm = getToolByName(site, 'portal_vocabularies')
    vocabs = {}
    for vocab_name, vocabulary in constants.vocabularies.items():
        if not hasattr(pvm, vocab_name):
            createSimpleVocabs(pvm, {vocab_name : vocabulary.items()})
    createHierarchicalVocabs(pvm, constants.hierarchical_vocabularies)

@guard
def addLanguages(self):
    site = self.getSite()
    # site languages
    plt = getToolByName(site, 'portal_languages')
    for l in constants.interface_languages:
        plt.addSupportedLanguage(l)
    plt.display_flags = 1
    # content languages
    registry = queryUtility(IRegistry)
    settings = registry.forInterface(IRecensioSettings)
    langs = "\n".join(constants.languages)
    setattr(settings, 'available_content_languages', langs)
    transaction.savepoint(optimistic=True)

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
    manager.facets = [u'portal_type', u'ddcPlace', 'ddcTime', 'ddcSubject']
    manager.required = []

@guard
def setPermissions(self):
    def setPermission(context, perm_name, roles):
        perm = filter(lambda x: perm_name == x[0],
                      context.ac_inherited_permissions(all=True))[0]
        name, value = perm[:2]
        permission = Permission(name, value, context)
        permission.setRoles(roles)

    user_folder = self.getSite().Members
    user_folder.manage_setLocalRoles('Reviewers', ['Reader'])
    setPermission(self.getSite(), 'Content Ratings: User Rate', ('Authenticated', ))

@guard
def configureContentRatings(context):
    portal = context.getSite()
    utility = getUtility(IRatingCategoryAssignment)
    portal_types = ['Review Journal', 'Review Monograph',\
                    'Presentation Online Resource',\
                    'Presentation Article Review',\
                    'Presentation Collection',\
                    'Presentation Monograph']
    categories_to_set = [utility._avalable_categories.by_token[''].value]
    for type in portal_types:
        utility.assign_categories(type, categories_to_set)

@guard
def setUpCollections(context):
    portal = context.getSite()
    wftool = getToolByName(portal, 'portal_workflow')
    def getOrAdd(context, type, name, publish = True):
        if name not in context.objectIds():
            context.invokeFactory(type, name)
            new_object = context[name]
            new_object.setLanguage('')
            if publish:
                wftool.doActionFor(new_object, 'publish')
        return context[name]

    def configureCollection(collection, types, location):
        try:
            criterion = collection.addCriterion(field='created', \
                criterion_type='ATFriendlyDateCriteria')
            criterion.setValue(31)
            criterion.setOperation('less')
            criterion.setDateRange('-')
        except BadRequest:
            pass
        try:
            criterion = collection.addCriterion(field='Type', \
                criterion_type='ATPortalTypeCriterion')
            criterion.setValue(types)
        except BadRequest:
            pass
        try:
            criterion = collection.addCriterion(field='Language', \
                criterion_type='ATSimpleStringCriterion')
            criterion.setValue('all')
        except BadRequest:
            pass
        try:
            criterion = collection.addCriterion(field='modified', \
                criterion_type='ATSortCriterion')
        except BadRequest:
            pass

    classic_reviews = (u'Review Monograph', u'Review Journal')
    self_reviews = (u'Presentation Collection', u'Presentation Article Review', u'Presentation Online Resource', u'Presentation Monograph')

    feeds = getOrAdd(portal, 'Folder', 'RSS-feeds')
    feeds.setTitle(u'RSS feeds')
    feeds.reindexObject()
    directlyProvides(feeds, INewsletterSource)
    new_reviews = getOrAdd(feeds, 'Topic', 'new_reviews')
    new_reviews.setTitle(u'Neue Rezensionen')
    new_reviews.reindexObject()
    configureCollection(new_reviews, classic_reviews, '/')
    new_self_reviews = getOrAdd(feeds, 'Topic', 'new_presentations')
    new_self_reviews.setTitle(u'Neue Präsentationen')
    new_self_reviews.reindexObject()
    configureCollection(new_self_reviews, self_reviews, '/')
    new_discussions = getOrAdd(feeds, 'Topic', 'new_discussions')
    new_discussions.setTitle(u'Neue Diskussionen')
    new_discussions.reindexObject()
    directlyProvides(new_discussions, IDiscussionCollections)
    try:
        criterion = new_discussions.addCriterion(field='last_comment_date',\
            criterion_type='ATFriendlyDateCriteria')
        criterion.setValue(31)
        criterion.setOperation('less')
        criterion.setDateRange('-')
    except BadRequest:
        pass

    internal_views = getOrAdd(portal, 'Folder', 'internal views', \
        publish = False)
    internal_views.setExcludeFromNav('True')
    digitool_export = getOrAdd(internal_views, 'Topic', 'Digitool Export')
    configureCollection(digitool_export, tuple(set(classic_reviews + self_reviews) - set((u'Presentation Online Resource',))), '/')
    criterion = digitool_export.getCriterion('created_ATFriendlyDateCriteria')
    criterion.setValue(1)

@guard
def addWorkflowScripts(context):
    site = context.getSite()
    pwt = getToolByName(site, 'portal_workflow')
    spw = getattr(pwt, 'simple_publication_workflow')
    spw_scripts = spw.scripts
    id = 'handle_change'
    if not getattr(spw_scripts, id, None):
        spw_scripts.manage_addProduct['PythonScripts'].manage_addPythonScript(
            id=id)
    body = """
rwh = context.restrictedTraverse('@@recensio_workflow_helper')
rwh.handleTransition(info)
"""
    params = "info"
    script = getattr(spw_scripts, id)
    script.ZPythonScript_edit(params, body)

    submit = getattr(spw.transitions, 'submit')
    submit.after_script_name = id
    publish = getattr(spw.transitions, 'publish')
    publish.after_script_name = id

@guard
def addCatalogIndexes(context):
    site = context.getSite()
    cat = getToolByName(site, 'portal_catalog')

    class extra(object):
        def __init__(self, field_name, lexicon_id, index_type, doc_attr=''):
            self.field_name = field_name
            self.lexicon_id = lexicon_id
            self.index_type = index_type
            self.doc_attr = doc_attr

    def addIndex(name, type, **kw):
        if not name in cat.indexes():
            log.debug('adding %s %s, kw=%s' %(type, name, kw))
            cat.addIndex(name, type, **kw)
        elif not filter(lambda x: x.getId() == name, cat.getIndexObjects())[0].meta_type == type:
            cat.delIndex(name)
            log.debug('adding %s %s, kw=%s' %(type, name, kw))
            cat.addIndex(name, type, **kw)
    
    def addColumn(name):
        if not name in cat.schema():
            log.debug('adding metadata %s' % name)
            cat.addColumn(name)

    addIndex('languageReviewedText', 'KeywordIndex')
    addIndex('languageReview', 'KeywordIndex')
    addIndex('ddcPlace', 'FieldIndex')
    addIndex('ddcTime', 'FieldIndex')
    addIndex('ddcSubject', 'FieldIndex')
    addIndex('authors', 'KeywordIndex', extra={'indexed_attrs': ['getAllAuthorData']})
    addIndex('authorsFulltext', 'ZCTextIndex', extra=extra(field_name='getAllAuthorDataFulltext',
        doc_attr='getAllAuthorDataFulltext', lexicon_id='plone_lexicon', index_type='Okapi BM25 Rank'))
    addIndex('titleOrShortname', 'ZCTextIndex', extra=extra(field_name='titel,subtitle,shortnameJournal', lexicon_id='plone_lexicon', index_type='Okapi BM25 Rank'))
    addIndex('year', 'FieldIndex', extra={'indexed_attrs': ['yearOfPublication', 'officialYearOfPublication']})
    addIndex('place', 'FieldIndex', extra={'indexed_attrs': ['placeOfPublication']})
    addIndex('publisher', 'FieldIndex')
    addIndex('series', 'FieldIndex')
    addIndex('isbn', 'FieldIndex')

    addColumn('getAuthors')
    addColumn('listAuthors')
    addColumn('getReviewAuthorFirstname')
    addColumn('getReviewAuthorLastname')
    addColumn('getYearOfPublication')
    addColumn('getOfficialYearOfPublication')

@guard
def hideAllFolders(context):
    site = context.getSite()
    for id in ['Members', 'news', 'events', 'imports', 'RSS-feeds', 'images']:
        ob = getattr(site, id, None)
        if ob:
            ob.setExcludeFromNav(True)
            ob.reindexObject()

@guard
def setupHomepage(context):
    site = context.getSite()
    fp = getattr(site, 'front-page', None)
    if not fp:
        log.error('Front page not found')
        return
    id = 'layout'
    if fp.hasProperty(id):
        fp._delProperty(id)
    fp._setProperty(id=id, value='homepage-view', type='string')
    log.debug('Homepage view was set on the front page')

    # set up portlet
    mapping = assignment_mapping_from_key(fp, 'plone.rightcolumn',
        CONTEXT_CATEGORY, '/'.join(fp.getPhysicalPath()))
    id = 'homepage-intro'
    if id not in mapping:
        mapping[id] = static.Assignment(header=u'Intro', text=portlet_hp_text,
            omit_border=True)

@guard
def setViewsOnFolders(context):
    portal = context.getSite()

    autoren = getattr(portal, 'autoren', None)
    if not autoren:
        log.warning('Folder "autoren" not found on portal. Please run recensio.contenttypes.initial_content')
    else:
        fp = getattr(autoren, 'index_html')
        id = 'layout'
        if fp.hasProperty(id):
            fp._delProperty(id)
        fp._setProperty(id=id, value='authorsearch', type='string')

    themen = getattr(portal, 'themen-epochen-regionen', None)
    if not themen:
        log.warning('Folder "themen-epochen-regionen" not found on portal. Please run recensio.contenttypes.initial_content')
    else:
        fp = getattr(themen, 'index_html')
        id = 'layout'
        if fp.hasProperty(id):
            fp._delProperty(id)
        fp._setProperty(id=id, value='browse-topics', type='string')

    rezensionen = getattr(portal, 'rezensionen', None)
    zeitschriften = getattr(rezensionen, 'zeitschriften', None)
    if not zeitschriften:
        log.warning('Folder "zeitschriften" not found on portal. Please run recensio.contenttypes.initial_content')
    else:
        fp = zeitschriften
        id = 'layout'
        if fp.hasProperty(id):
            fp._delProperty(id)
        fp._setProperty(id=id, value='publications-view', type='string')

def doSetLanguage(obj, language):
    obj.setLanguage(language)
    if IBaseFolder.providedBy(obj):
        for item in obj.objectValues():
            doSetLanguage(item, language)

@guard
def makeImportedContentGerman(context):
    portal = context.getSite()
    for id in imported_content:
        ob = getattr(portal, id, None)
        if not ob:
            log.warning('Object %s not found. Please run import step "Recensio initial content"' % id)
            continue
        if id not in ['images']:
            language = 'de'
        else:
            language = ''
        doSetLanguage(ob, language)
        
    portal.setLanguage('de')


def doPublish(obj, pwt):
    try:
        pwt.doActionFor(obj, 'publish')
        obj.reindexObject()
    except:
        log.info('Could not publish %s' % obj.absolute_url())
    if IBaseFolder.providedBy(obj):
        for item in obj.objectValues():
            doPublish(item, pwt)

@guard
def publishImportedContent(context):
    portal = context.getSite()
    pwt = getToolByName(portal, 'portal_workflow')
    for id in imported_content:
        obj = getattr(portal, id, None)
        if not obj:
            log.warning('Object %s not found. Please run import step "Recensio initial content"' % id)
            continue
        doPublish(obj, pwt)
