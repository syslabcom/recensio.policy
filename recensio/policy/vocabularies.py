from zope.app.schema.vocabulary import IVocabularyFactory
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.app.component.hooks import getSite
from constants import USER_LANGUAGES

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
            for lang in USER_LANGUAGES]


        return SimpleVocabulary(terms)

AvailableUserLanguagesFactory = AvailableUserLanguages()