from Products.CMFCore.utils import getToolByName
from logging import getLogger
from Products.ATVocabularyManager.utils.vocabs import createSimpleVocabs
import transaction
import constants
import os
from plone.app.controlpanel.security import SecurityControlPanelAdapter

log = getLogger('esc.policy.setuphandlers.py')

mdfile = os.path.join(os.path.dirname(__file__), 'profiles', 'default',
    'metadata.xml')

def isNotRecensioProfile(self):
    return self.readDataFile('recensio.policy_marker.txt') is None

def importVocabularies(self):
    if isNotRecensioProfile(self):
        return
    site = self.getSite()
    pvm = getToolByName(site, 'portal_vocabularies')
    vocabs = {}
    for vocab_name, vocabulary in constants.vocabularies.items():
        if not hasattr(pvm, vocab_name):
            createSimpleVocabs(pvm, {vocab_name : vocabulary.items()})

def addLanguages(self):
    if isNotRecensioProfile(self):
        return
    site = self.getSite()
    lang = getToolByName(site, 'portal_languages')
    for l in constants.languages:
        lang.addSupportedLanguage(l)
    transaction.savepoint(optimistic=True)

def configureSecurity(self):
    if isNotRecensioProfile(self):
        return
    site = self.getSite()
    pcp = SecurityControlPanelAdapter(site)
    pcp.set_enable_self_reg(True)
    pcp.set_enable_user_pwd_choice(False)
    pcp.set_enable_user_folders(True)
