from constants import interface_languages
from plone.i18n.locales.interfaces import ILanguageAvailability
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from recensio.policy import recensioMessageFactory as _
from recensio.policy.interfaces import IRecensioSettings
from zope.component import getGlobalSiteManager
from zope.component import queryUtility
from zope.component.hooks import getSite
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class AvailableUserLanguages(object):
    """ Vocabulary that shows all languages that a user might
        chose during registration
    """

    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(self, "context", getSite())
        language_tool = getToolByName(context, "portal_languages")

        info = language_tool.getAvailableLanguageInformation()
        terms = [SimpleTerm(lang, lang, info.get(lang).get("native")) for lang in info]
        return SimpleVocabulary(terms)


AvailableUserLanguagesFactory = AvailableUserLanguages()


class AvailableContentLanguages(object):
    """ Vocabulary that holds the languages defined in the recensio-settings
        and which our content types support.
    """

    implements(IVocabularyFactory)

    def __call__(self, context):
        # get user-defined languages
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IRecensioSettings)
        allowed_langs = getattr(settings, "available_content_languages", "").split("\n")
        # get names for language codes
        gsm = getGlobalSiteManager()
        util = gsm.queryUtility(ILanguageAvailability)
        available_languages = util.getLanguages()
        terms = list()
        for lang in allowed_langs:
            lang = lang.strip()
            if available_languages.get(lang):
                terms.append(
                    SimpleTerm(lang, lang, _(available_languages[lang]["name"]))
                )

        return SimpleVocabulary(terms)


AvailableContentLanguagesFactory = AvailableContentLanguages()
