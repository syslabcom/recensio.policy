import json

from Products.Five.browser import BrowserView
from zope.component import getUtility
from zope.i18n.locales import locales
from zope.schema.interfaces import IVocabularyFactory

from recensio.policy.sparqlsearch import getMetadata


class OPAC(BrowserView):

    def __call__(self, identifier):
        data = getMetadata(identifier)
        data['language'] = \
            self._convertLanguageToLangCode(data['language'])
        return json.dumps([data])

    def _convertLanguageToLangCode(self, language):
        if not language:
            return ""
        locale = locales.getLocale('en')
        lang_in_german = locale.displayNames.languages

        if not hasattr(self, '_converter'):
            self._converter = {}
            util = getUtility(IVocabularyFactory,
                              u"recensio.policy.vocabularies.available_content_languages")
            vocab = util(self.context)
            for key, title in [(x.value, lang_in_german[x.value])
                               for x in vocab]:
                self._converter[title] = \
                    key
        for key, value in self._converter.items():
            if key.lower() in language.lower():
                return value
