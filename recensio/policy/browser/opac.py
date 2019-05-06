import json

from Products.Five.browser import BrowserView
from plone import api
from zope.component import getUtility
from zope.i18n.locales import locales
from zope.schema.interfaces import IVocabularyFactory

from recensio.policy.srusearch import getMetadata
import logging

log = logging.getLogger(__name__)


class OPAC(BrowserView):

    def __call__(self, identifier):
        metadata = getMetadata(identifier)
        for entry in metadata:
            entry['language'] = \
                self._convertLanguageToLangCode(entry['language'])
        return json.dumps(metadata)

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


class MetadataQuery(OPAC):
    def __call__(self, identifier):
        cat = api.portal.get_tool(name='portal_catalog')
        results = cat(isbn=identifier)
        metadata = []
        for result in results:
            try:
                res = result.getObject()
            except:
                path = result and result.getPath() or 'None'
                log.error('Could not get object: ' + path)
                continue
            metadata.append({
                'title': res.Title(),
                'subtitle': res.getSubtitle(),
                'authors': res.getAuthors(),
                'language': res.getLanguageReviewedText(),
                'isbn': res.getIsbn(),
                # DDC values can vary, not handling now, see #13569-5
                # 'ddcSubject': res.getDdcSubject(),
                # 'ddcTime': res.getDdcTime(),
                # 'ddcPlace': res.getDdcPlace(),
                'location': res.getPlaceOfPublication(),
                'keywords': res.Subject(),
                'publisher': res.getPublisher(),
                'pages': res.getPages(),
                'series': res.getSeries(),
                'seriesVol': res.getSeriesVol(),
                'year': res.getYearOfPublication(),
                'bv': res.getBv(),
                'source': {'title': self.context.Title(),
                           'url': res.absolute_url()},
            })

        for opac_data in getMetadata(identifier):
            opac_data['language'] = self._convertLanguageToLangCode(
                opac_data['language'])
            opac_data['source'] = {
                'title': 'OPAC',
                'url': 'http://lod.b3kat.de/page/isbn/' + identifier}
            metadata.append(opac_data)

        return json.dumps(metadata)
