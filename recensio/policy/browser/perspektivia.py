import urllib

import BeautifulSoup

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

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
        self._handleReviews(data['reviews'])
        self._handleBooks(data['books'])

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
            review['reviewAuthorFirstname'] = author['firstname']
            review['reviewAuthorLastname'] = author['lastname']
            break
        review['canonical_uri'] = review.pop('identifier')
        review['id'] = self.plone_utils.normalizeString(review['title'])
        for unused_key in ['date', 'format', 'publisher', 'rights', 'source']:
            review.pop(unused_key)
        return helper, review

    def _renameKeysOfBook(self, book):
        helper = {}
        book['authors'] = book.pop('creator')
        for unused_key in ['date', 'format', 'relation', 'rights', 'source', \
            'subject', 'type']:
            book.pop(unused_key)
        book['isbn'] = book.pop('identifier')
        return {}, book

    def _addReviewKeys(self, review):
        html = urllib.urlopen(review['canonical_uri']).read()
        soup = BeautifulSoup.BeautifulSoup(html)
        for x in  ['Subject', 'Time', 'Place']:
            review['ddc' + x] = []
        for subject in review['subject']:
            if subject in self.pv.topic_values.keys():
                review['ddcSubject'].append(subject)
            if subject in self.pv.epoch_values.keys():
                review['ddcTime'].append(subject)
            if subject in self.pv.region_values.keys():
                review['ddcPlace'].append(subject)
        review['review'] = ''.join([x.prettify().decode('utf8') for x in \
                    soup.findAll('p', {'class' : 'western'})])
        return review

    def _addBookKeys(self, book):
        return book

    def _importReview(self, review, helper):
        volume_id = helper['review_date'].strftime('%y')
        issue_id = helper['review_date'].strftime('%m')
        if volume_id not in self.mag:
            self.mag.invokeFactory(type_name="Volume", id=volume_id)
        volume = self.mag[volume_id]
        if issue_id not in volume:
            volume.invokeFactory(type_name='Issue', id=issue_id)
        issue = volume[issue_id]
        if review['id'] in issue:
            if issue[review['id']].hasReview:
                return
            review_ob = issue[review['id']]
        else:
            issue.invokeFactory(type_name = 'Review Monograph', id = review['id'])
            review_ob = issue[review['id']]
        for key, value in review.items() + helper.items():
            setattr(review_ob, key, value)
        review_ob.hasReview = True

    def _importBook(self, book, helper):
        return book
