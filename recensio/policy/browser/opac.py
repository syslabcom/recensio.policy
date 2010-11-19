from zope.app.schema.vocabulary import IVocabularyFactory
from zope.component import getUtility
from zope.i18n import translate

from Products.Five.browser import BrowserView

import urllib
import json

from recensio.policy.opacsearch import opac

class OPAC(BrowserView):
    def __call__(self, identifier):
        data = opac.getMetadataForISBN(identifier)
        for i in range(len(data)):
            data[i]['language'] = \
                self._convertLanguageToLangCode(data[i]['language'])
        return json.dumps(data)

    def _convertLanguageToLangCode(self, language):
        if not hasattr(self, '_converter'):
            self._converter = {}
            util = getUtility(IVocabularyFactory,
                u"recensio.policy.vocabularies.available_content_languages")
            vocab = util(self.context)
            for key, title in [(x.value, x.title) for x in vocab]:
                self._converter[translate(title, target_language='de')] = \
                    key
        return self._converter.get(language, 'unknown')
