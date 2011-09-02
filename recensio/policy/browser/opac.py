from zope.app.schema.vocabulary import IVocabularyFactory
from zope.component import getUtility
from zope.i18n import translate
from zope.i18n.locales import locales

from Products.Five.browser import BrowserView

import urllib
import json

from recensio.policy.opacsearch import opac

geo_mapping = {
'xa' : '4',
'ae' : '41',
'fi' : '41.1',
'is' : '41.2',
'sc' : '41.3',
'da' : '41.31',
'no' : '41.32',
'sw' : '41.33',
'bk' : '41.4',
'ee' : '41.41',
'lv' : '41.42',
'lt' : '41.43',
'xw' : '42',
'nl' : '42.1',
'be' : '42.2',
'lx' : '42.3',
'fr' : '42.4',
'de' : '42.5',
'at' : '42.6',
'ch' : '42.7',
'gb' : '42.8',
'ie' : '42.9',
'oe' : '43',
'ru' : '43.1',
'by' : '43.2',
'ua' : '43.3',
'pl' : '43.4',
'cz' : '43.5',
'sk' : '43.6',
'hu' : '43.7',
'ro' : '43.8',
'md' : '43.9',
'am' : '44.6',
'az' : '44.7',
'ge' : '44.8',
'ys' : '44',
'es' : '44.1',
'pt' : '44.2',
'it' : '44.3',
'xm' : '44.4',
'zy' : '44.5',
'yb' : '44.6',
'al' : '44.61',
'ba' : '44.62',
'bg' : '44.63',
'gr' : '44.64',
'hr' : '44.65',
'mk' : '44.66',
'sp' : '44.67',
'si' : '44.68',
'tr' : '44.69',
'xb' : '5',
'xf' : '51',
'xj' : '52',
'ya' : '54',
'xg' : '56',
'xs' : '57',
'za' : '58',
'yo' : '59',
'xc' : '6',
'xh' : '61',
'xi' : '62',
'xk' : '63',
'xl' : '64',
'xn' : '65',
'yw' : '66',
'af' : '67',
'as' : '68',
'xd' : '7',
'na' : '71',
'us' : '71.1',
'ca' : '71.2',
'ma' : '72',
'sa' : '73',
'xe' : '9',
'xq' : '09',
'vg' : '3',
'aa' : '32',
'bz' : '34',
'ac' : '31',
'ag' : '38',
'pe' : '35',
'ap' : '33',
'rr' : '37',
}

epoch_mapping = {
'10' : 't1:0901',
'12' : 't1:09012',
'13' : 't1:09013',
'14' : 't1:09014',
'15' : 't1:09015',
'20' : 't1:0902',
'21' : 't1:09021',
'22' : 't1:09022',
'23' : 't1:09023',
'24' : 't1:09024',
'30' : 't1:0903',
'31' : 't1:09031',
'32' : 't1:09032',
'33' : 't1:09033',
'34' : 't1:09034',
'40' : 't1:0904',
'91' : 't1:09040',
'41' : 't1:09041',
'42' : 't1:09042',
'43' : 't1:09043',
'44' : 't1:09044',
'95' : 't1:090441',
'45' : 't1:09045',
'46' : 't1:09046',
'47' : 't1:09047',
'48' : 't1:09048',
'49' : 't1:09049',
'50' : 't1:0905',
'51' : 't1:09051',
}

topic_mapping = {
'ag' : '630.9',
'ak' : '780.0534',
'a1' : '060',
'a2' : '290',
'a4' : '490',
'te' : '600',
'a5' : '720',
'ap' : '781.43',
'an' : '781.4',
'bi' : '020',
'er' : '370',
'eg' : '370.9',
'gb' : '920',
'bl' : '788',
'ed' : '780.149',
'vl' : '930',
'el' : '786.7',
'fg' : '791.409',
'gf' : '781.5',
'km' : '781.7',
'he' : '910',
'ip' : '780.77',
'ge' : '900',
'ng' : '509',
'gp' : '150.9',
'ph' : '070.9',
'gg' : '305.309',
'gl' : '880',
'' : '292',
'gs' : '480',
'gh' : '902',
'dg' : '304.609',
'hg' : '911',
'hh' : '902.8',
'hf' : '902.85',
'fi' : '791',
'ig' : '001.09',
'im' : '784',
'in' : '784.19',
'ja' : '781.65',
'gj' : '909.04924',
'rg' : '200.9',
'cg' : '306.09',
'cg' : '306.09',
'ku' : '700',
'kg' : '700.9',
'aa' : '630',
'll' : '870',
'ls' : '470',
'li' : '800',
'a9' : '890',
'lh' : '800.09',
'a8' : '750',
'ma' : '780.051',
'mc' : '786.6',
'pu' : '070',
'me' : '610',
'mh' : '610.9',
'mi' : '355',
'mg' : '355.009',
'mu' : '780',
'mu' : '780',
'op' : '780.079',
'tz' : '793.3',
'ks' : '780.07',
'lt' : '780.08',
'mz' : '780.061',
'jm' : '780.034',
'gf' : '781.5',
'mf' : '372.87',
'mk' : '780.17',
'ed' : '780.149',
'vo' : '781.6',
'gm' : '780.9',
'gm' : '780.9',
'ik' : '704.9',
'lg' : '780.14',
'mp' : '780.7',
'py' : '781.11',
'sz' : '306.484.2',
'mt' : '781',
'bu' : '780.033',
'mw' : '780.72',
'nb' : '780.2',
'na' : '500',
'no' : '780.148',
'pi' : '100',
'a6' : '730',
'po' : '320',
'pg' : '320.9',
'pm' : '781.66',
'ps' : '150',
'ju' : '340',
'jg' : '340.09',
're' : '200',
'a3' : '292',
'pc' : '786.8',
'og' : '307.09',
'sg' : '300.9',
'so' : '300',
'fu' : '796',
'fh' : '796.09',
'sp' : '400',
'sh' : '417.7',
'si' : '787',
'sm' : '780.1',
'ti' : '786',
'tg' : '609',
'ta' : '792',
'th' : '792.09',
'gt' : '901',
'vw' : '350',
'vg' : '351.09',
'vm' : '782',
'et' : '390',
'xq' : '909',
'wi' : '330',
'wg' : '330.09',
'cu' : '001',
'a7' : '740',
}

class OPAC(BrowserView):
    def __call__(self, identifier):
        data = opac.getMetadataForISBN(identifier)
        for i in range(len(data)):
            data[i]['language'] = \
                self._convertLanguageToLangCode(data[i]['language'])
            self._convertKeywords(data[i])
        return json.dumps(data)

    def _convertLanguageToLangCode(self, language):
        if not language:
            return ""
        locale = locales.getLocale('de')
        lang_in_german = locale.displayNames.languages

        if not hasattr(self, '_converter'):
            self._converter = {}
            util = getUtility(IVocabularyFactory,
                u"recensio.policy.vocabularies.available_content_languages")
            vocab = util(self.context)
            for key, title in [(x.value, lang_in_german[x.value]) for x in vocab]:
                self._converter[title] = \
                    key
        retval = []
        for key, value in self._converter.items():
            if key.lower() in language.lower():
                return value

    def _convertKeywords(self, data):
        data['ddcPlace'] = []
        data['ddcTime'] = []
        data['ddcSubject'] = []
        for keyword in data.get('ddc', None) or []:
            prefix = keyword[:1]
            suffix = keyword[2:]
            if prefix == 'G':
                translated = geo_mapping.get(suffix, None)
                if translated:
                    data['ddcPlace'].append(translated)
            if prefix == 'Z':
                translated = epoch_mapping.get(suffix, None)
                if translated:
                    data['ddcTime'].append(translated)
            if prefix == 'S':
                translated = topic_mapping.get(suffix, None)
                if translated:
                    data['ddcSubject'].append(translated)

        data.pop('ddc')
