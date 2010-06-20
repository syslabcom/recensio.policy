from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.interface import directlyProvides
from plone.contentratings.interfaces import IRatingCategoryAssignment
from logging import getLogger
from Products.ATVocabularyManager.utils.vocabs import createSimpleVocabs
import transaction
import constants
import os
from zExceptions import BadRequest
from plone.app.controlpanel.security import SecurityControlPanelAdapter
from recensio.policy.interfaces import IDiscussionCollections

log = getLogger('esc.policy.setuphandlers.py')

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
    portal_types = ['Rezension']
    categories_to_set = [utility._avalable_categories.by_token[''].value]
    for type in portal_types:
        utility.assign_categories(type, categories_to_set)

@guard
def setUpCollections(context):
    portal = context.getSite()
    wftool = getToolByName(portal, 'portal_workflow')
    def getOrAdd(context, type, name):
        if name not in context.objectIds():
            context.invokeFactory(type, name)
            new_object = context[name]
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

    feeds = getOrAdd(portal, 'Folder', 'RSS-feeds')
    new_rezensions = getOrAdd(feeds, 'Topic', 'new_rezenions')
    configureCollection(new_rezensions, 'Rezension', '/')
    new_self_rezensions = getOrAdd(feeds, 'Topic', 'new_self_rezensions')
    configureCollection(new_self_rezensions, 'Rezension', '/')
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
