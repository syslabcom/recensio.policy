# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.interface import implements
from zope.component import getUtility
from zope.app.schema.vocabulary import IVocabularyFactory
from Products.Archetypes.utils import DisplayList

from recensio.policy.interfaces import IRecensioView


class RecensioView(BrowserView):
    """ Utility browser view
    """
    implements(IRecensioView)

    def getSupportedLanguages(self):
        util = getUtility(IVocabularyFactory,
            u"recensio.policy.vocabularies.available_content_languages")
        vocab = util(self)
        terms = [(x.value, x.title) for x in vocab]
        return DisplayList(terms)