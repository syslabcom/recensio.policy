from zope.schema.interfaces import IVocabularyFactory
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.component.hooks import getSite


class AvailableUserLanguages(object):
    """ Vocabulary that shows all languages that a user might
        chose during registration
    """

    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(self, 'context', getSite())
        language_tool = getToolByName(context, 'portal_languages')

        info = language_tool.getAvailableLanguageInformation()
        terms = [SimpleTerm(lang, lang, info.get(lang).get('native'))
                 for lang in info]
        return SimpleVocabulary(terms)

AvailableUserLanguagesFactory = AvailableUserLanguages()
