import urllib

import BeautifulSoup

from persistent.dict import PersistentDict
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.event import ObjectEditedEvent
from zope.event import notify

from recensio.policy.importOAI import perspektivia_parser

class Import(BrowserView):
    def __init__(self, context, request):
        super(Import, self).__init__(context, request)
        self.mag = self.context.rezensionen.zeitschriften['francia-recensio']
        self.plone_utils = getToolByName(context, 'plone_utils')

        self.pv = getToolByName(context, 'portal_vocabularies')

    def __call__(self):
        import pkg_resources
        filename = pkg_resources.resource_filename(__name__, '../tests/perspektivia.xml')
        data = perspektivia_parser.parse(file(filename).read())
        # The order is IMPORTANT!
        self._handleBooks(data['books'])
        self._handleReviews(data['reviews'])

    def _handleReviews(self, reviews):
        for review in reviews:
            self._runAssertions(review)
            helper, review = self._renameKeysOfReview(review)
            review = self._addReviewKeys(review)
            self._importReview(review, helper)

    def _handleBooks(self, books):
        for book in books:
            self._runAssertions(book)
            helper, book = self._renameKeysOfBook(book)
            book = self._addBookKeys(book)
            self._importBook(book, helper)

    def _runAssertions(self, obj):
        assert obj['format'] == 'application/html'
        assert obj['rights'] in ['by-nc-ne-3.0-de, perspectivia.net', '']
        assert obj['type'] in ('Book', 'Review')

    def _renameKeysOfReview(self, review):
        helper = {}
        helper['review_date'] = review['date']
        helper['review_id'] = review['id']
        helper['book_id'] = review['relation']
        authors = review.pop('creator')
        for author in authors:
            review['reviewAuthorFirstname'] = author['firstname'].encode('utf8')
            review['reviewAuthorLastname'] = author['lastname'].encode('utf8')
            break
        review['canonical_uri'] = review.pop('identifier')
        review['id'] = self.plone_utils.normalizeString(review['title']).encode('utf8')
        for unused_key in ['date', 'format', 'publisher', 'rights', 'source','id', 'title']:
            review.pop(unused_key)
        return helper, review

    def _renameKeysOfBook(self, book):
        helper = {}
        def stringify(things):
            for thing in things:
                for key in thing.keys():
                    thing[key] = thing[key].encode('utf8')
                yield thing
        book['authors'] = list(stringify(book.pop('creator')))
        for unused_key in ['date', 'format', 'relation', 'rights', 'source', \
            'subject', 'type']:
            book.pop(unused_key)
        book['isbn'] = book.pop('identifier')
        publisher = book.pop('publisher')
        placeOfPublication = None
        if publisher.count(',') == 1:
            publisher, placeOfPublication = publisher.split(',')
        book['publisher'] = publisher.strip()
        if placeOfPublication:
            book['placeOfPublication'] = placeOfPublication
        book['id'] = self.plone_utils.normalizeString(book['title']).encode('utf8')
        return {}, book

    def _addReviewKeys(self, review):
        html = urllib.urlopen(review['canonical_uri']).read()
        soup = BeautifulSoup.BeautifulSoup(html)
        for x in  ['Subject', 'Time', 'Place']:
            review['ddc' + x] = []
        found = []
        for subject in review['subject']:
            original_subject = subject
            if subject.startswith('t'):
                subject = subject[1:]
            if subject in self.pv.topic_values.keys():
                review['ddcSubject'].append(subject)
                found.append(original_subject)
            if subject in self.pv.epoch_values.keys():
                review['ddcTime'].append(subject)
                found.append(original_subject)
            if subject in self.pv.region_values.keys():
                review['ddcPlace'].append(subject)
                found.append(original_subject)
        for subject in found:
            subject.remove(subject)
        review['review'] = ''.join([x.prettify().decode('utf8') for x in \
                    soup.findAll('p', {'class' : 'western'})])
        return review

    def _addBookKeys(self, book):
        book['review'] = "No review has been added yet"
        return book

    def _importReview(self, review, helper):
        review_ob = self.mag.incomplete_books.pop(helper['book_id'])
        for key, value in review.items() + helper.items():
            setattr(review_ob, key, value)
        notify(ObjectEditedEvent(review_ob))

    def _importBook(self, book, helper):
        if '1' not in self.mag:
            self.mag.invokeFactory(type_name="Volume", id='1')
        volume = self.mag['1']
        if '1' not in volume:
            volume.invokeFactory(type_name='Issue', id='1')
        issue = volume['1']
        if book['id'] in issue:
            return
        else:
            issue.invokeFactory(type_name = 'Review Monograph', id = book['id'])
        import pdb;pdb.set_trace()
        book_ob = issue[book['id']]
        if not hasattr(self.mag, 'incomplete books'):
            self.mag.incomplete_books = PersistentDict()
        self.mag.incomplete_books[book['isbn']] = book_ob
        for key, value in book.items():
            setattr(book_ob, key, value)

        return book
