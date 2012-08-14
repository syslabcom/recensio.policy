from BeautifulSoup import BeautifulSoup
from Products.Archetypes.event import ObjectEditedEvent
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from guess_language import guessLanguage as originalGuessLanguage
from itertools import chain
from zope.event import notify
import datetime
import htmlentitydefs
import re
import urllib
import logging
from transaction import commit

from recensio.policy.importSehepunkte import sehepunkte_parser
from recensio.policy.tools import convertToString

log = logging.getLogger(__name__)

def convert(vocab):
    retval = {}
    if not vocab:
        return retval
    for key, value in vocab.items():
        if isinstance(value, tuple):
            retval[value[0]] = key
            retval.update(convert(value[1]))
        elif isinstance(value, basestring):
            retval[value] = key
    return retval

class Import(BrowserView):
    def __init__(self, context, request):
        super(Import, self).__init__(context, request)
        self.mag = self.context.rezensionen.zeitschriften.sehepunkte
        self.plone_utils = getToolByName(context, 'plone_utils')

        pv = getToolByName(context, 'portal_vocabularies')
        self.topic_values = convert(pv.topic_values._getManager().getVocabularyDict(lang='de'))
        self.epoch_values = convert(pv.epoch_values._getManager().getVocabularyDict(lang='de'))
        self.region_values = convert(pv.region_values._getManager().getVocabularyDict(lang='de'))

    def __call__(self):
        data = []
        before = datetime.datetime.now()
        review_count = 0
        for url in self._getTargetURLs():
            try:
                data.append(sehepunkte_parser.parse(urllib.urlopen(url).read()))
            except IOError:
                pass # The library takes care of logging a failure
        for review in chain(*data):
            try:
                self._addReview(self._convertVocabulary(\
                                 convertToString(\
                                  review)))
                review_count += 1
            except:
                log.exception("Warning, sehepunkte import failed! Exception "
                    "has not been catched, but bubbled. Probably sehepunkte "
                    "is broken now! Please see #4656 for fixes")
                raise

        total = (datetime.datetime.now() - before).seconds / 1.0
        log.info("Sehepunkte finished. Imported %i reviews "
            "in %f seconds. %f reviews/s",
            review_count, total, review_count / total)
        return "Success"

    def _getTargetURLs(self):
        base = 'http://www.sehepunkte.de/export/sehepunkte_%s.xml'
        now = datetime.datetime.now()
        big_month = datetime.timedelta(days=31)
        yield base % (now - big_month).strftime('%Y_%m')
        yield base % (now).strftime('%Y_%m')
        yield base % (now + big_month).strftime('%Y_%m')

    def _addReview(self, review):
        if review['volume'] not in self.mag:
            self.mag.invokeFactory(type_name="Volume", id=review['volume'], title="%s (%s)" % (review['volume'], review['year']))
        volume = self.mag[review['volume']]
        if review['issue'] not in volume:
            volume.invokeFactory(type_name='Issue', id=review['issue'], title=review['issue'])
        issue = volume[review['issue']]
        new_id = self.plone_utils.normalizeString(review['title'])
        if new_id in issue:
            return

        def guessLanguage(text):
            lang = originalGuessLanguage(text)
            if lang == 'UNKNOWN':
                lang = 'de'
            return lang
        review = self._extractAndSanitizeHTML(review)
        languageReview = guessLanguage(review['review'])
        languageReviewedText = guessLanguage(review['title'])
        issue.invokeFactory(type_name='Review Monograph', id = new_id)
        review_ob = issue[new_id]
        review_ob.languageReview = languageReview
        review_ob.languageReviewedText = languageReviewedText
        for key, value in review.items():
            if isinstance(value, str):
                value = superclean(value).encode('utf-8')
            setattr(review_ob, key, value)
        notify(ObjectEditedEvent(review_ob))

    def _convertVocabulary(self, review):
        category = review.pop('category')
        setter = lambda mapper: [x for x in [mapper.get(category, '')] if x]
        review['ddcSubject'] = setter(self.topic_values)
        review['ddcTime'] = setter(self.epoch_values)
        review['ddcPlace'] = setter(self.region_values)
        return review

    def _extractAndSanitizeHTML(self, review):
        html = urllib.urlopen(review['canonical_uri']).read()
        soup = BeautifulSoup(html)
        dirt = soup.findAll('div', {'class' : 'box'})
        for div in dirt:
            if div.find('div', {'class' : 'header'}).text != \
                u'Empfohlene Zitierweise:':
                continue
            review['canonical_uri'] = div.p.a['href']
            review['customCitation'] = div.p.text
        [x.extract() for x in dirt]
        try:
            review['review'] = soup.find('div', id='text_area').prettify()
        except AttributeError:
            try:
                review['review'] = soup.find('body', {'class':'printable'}).prettify()
            except AttributeError:
                review['review'] = soup.prettify()
        return review

def superclean(text):
    def unescape(text):
        def fixup1(m):
            return inner_fixup(m)
        def fixup2(m):
            return inner_fixup(m, True)
        def inner_fixup(m, i_thought_i_can_write_html_by_hand_but_i_cant = False):
            tailcut = -1
            if i_thought_i_can_write_html_by_hand_but_i_cant:
                tailcut = 1000
            text = m.group(0)
            if text[:2] == "&#":
                # character reference
                try:
                    if text[:3] == "&#x":
                        return unichr(int(text[3:tailcut], 16))
                    else:
                        return unichr(int(text[2:tailcut]))
                except ValueError:
                    pass
            else:
                # named entity
                try:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:tailcut]])
                except KeyError:
                    pass
            return text # leave as is
        return re.sub("&#?\d+", fixup2,
                      re.sub("&#?\d+;", fixup1, text))
    return unescape(text.decode('utf-8'))
    
