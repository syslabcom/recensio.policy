# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.interface import implements
from zope.component import getUtility
from zope.app.schema.vocabulary import IVocabularyFactory
from Products.Archetypes.utils import DisplayList
from plone.i18n.locales.languages import _languagelist

from recensio.policy.interfaces import IRecensioView
from recensio.contenttypes.content.review import BaseReviewNoMagic


class RecensioView(BrowserView):
    """ Utility browser view
    """
    implements(IRecensioView)

    def getSupportedLanguages(self):
        return BaseReviewNoMagic(self.context).listSupportedLanguages()
