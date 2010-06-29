from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.interface import directlyProvides
from plone.contentratings.interfaces import IRatingCategoryAssignment
from logging import getLogger
from Products.ATVocabularyManager.utils.vocabs import createSimpleVocabs,\
    createHierarchicalVocabs
import transaction
import constants
import os
from zExceptions import BadRequest
from plone.app.controlpanel.security import SecurityControlPanelAdapter
from recensio.policy.interfaces import IDiscussionCollections, INewsletterSource

log = getLogger('recensio.policy.setuphandlers.py')

mdfile = os.path.join(os.path.dirname(__file__), 'profiles', 'default',
    'metadata.xml')

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
    lang = getToolByName(site, 'portal_languages')
    for l in constants.languages:
        lang.addSupportedLanguage(l)
    transaction.savepoint(optimistic=True)

@guard
def configureSecurity(self):
    site = self.getSite()
    pcp = SecurityControlPanelAdapter(site)
    pcp.set_enable_self_reg(True)
    pcp.set_enable_user_pwd_choice(False)
    pcp.set_enable_user_folders(True)

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

@guard
def configureContentRatings(context):
    portal = context.getSite()
    utility = getUtility(IRatingCategoryAssignment)
    portal_types = ['Review']
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
            criterion = collection.addCriterion(field='path', \
                criterion_type='ATRelativePathCriterion')
            criterion.setRelativePath('/')
            criterion.setRecurse(True)
        except BadRequest:
            pass

    classic_reviews = (u'Review Monograph', u'Review Journal')
    self_reviews = (u'Presentation Collection', u'Presentation Article Review', u'Presentation Online Resource', u'Presentation Monograph')

    feeds = getOrAdd(portal, 'Folder', 'RSS-feeds')
    directlyProvides(feeds, INewsletterSource)
    new_reviews = getOrAdd(feeds, 'Topic', 'new_rezenions')
    configureCollection(new_reviews, classic_reviews, '/')
    new_self_reviews = getOrAdd(feeds, 'Topic', 'new_self_reviews')
    configureCollection(new_self_reviews, self_reviews, '/')
    new_discussions = getOrAdd(feeds, 'Topic', 'new_discussions')
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
        def __init__(self, field_name, lexicon_id, index_type):
            self.field_name = field_name
            self.lexicon_id = lexicon_id
            self.index_type = index_type

    def addIndex(name, type, **kw):
        if not name in cat.indexes():
            log.debug('adding %s %s, kw=%s' %(type, name, kw))
            cat.addIndex(name, type, **kw)
        elif not filter(lambda x: x.getId() == name, cat.getIndexObjects())[0].meta_type == type:
            cat.delIndex(name)
            log.debug('adding %s %s, kw=%s' %(type, name, kw))
            cat.addIndex(name, type, **kw)

    addIndex('languagePresentation', 'LanguageIndex')
    addIndex('languageReview', 'LanguageIndex')
    addIndex('ddcPlace', 'FieldIndex')
    addIndex('ddcTime', 'FieldIndex')
    addIndex('ddcSubject', 'FieldIndex')
    addIndex('authors', 'KeywordIndex', extra={'indexed_attrs': ['reviewAuthor', 'authors', 'editorCollectedEdition']})
    addIndex('titleOrShortname', 'ZCTextIndex', extra=extra(field_name='titel,subtitle,shortnameJournal', lexicon_id='plone_lexicon', index_type='Okapi BM25 Rank'))
    addIndex('year', 'FieldIndex', extra={'indexed_attrs': ['yearOfPublication', 'officialYearOfPublication']})
    addIndex('place', 'FieldIndex', extra={'indexed_attrs': ['placeOfPublication']})
    addIndex('publisher', 'FieldIndex')
    addIndex('series', 'FieldIndex')
    addIndex('isbn', 'FieldIndex')
