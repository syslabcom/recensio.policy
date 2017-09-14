import unittest
from recensio.policy.indexer import get_field_and_ebook_variant
from recensio.policy.indexer import isbn


class ReviewStubIsbn(object):

    def __init__(self, isbn='', isbn_online=''):
        self.isbn = isbn
        self.isbn_online = isbn_online

    def getIsbn(self):
        return self.isbn

    def getIsbn_online(self):
        return self.isbn_online


class ReviewStubIssn(object):

    def __init__(self, issn='', issn_online=''):
        self.issn = issn
        self.issn_online = issn_online

    def getIssn(self):
        return self.issn

    def getIssn_online(self):
        return self.issn_online


class ReviewStubYear(object):

    def __init__(self, year='', year_online=''):
        self.year = year
        self.year_online = year_online

    def getYearOfPublication(self):
        return self.year

    def getYearOfPublicationOnline(self):
        return self.year_online


class TestIndexer(unittest.TestCase):

    def test_isbn_and_isbn_online(self):
        result = isbn(ReviewStubIsbn(isbn='12-34', isbn_online='5-678'))()
        self.assertEqual(result, ['1234', '5678'])

    def test_isbn_only(self):
        result = isbn(ReviewStubIsbn(isbn='12-34'))()
        self.assertEqual(result, ['1234'])

    def test_isbn_online_only(self):
        result = isbn(ReviewStubIsbn(isbn_online='834 5562 88'))()
        self.assertEqual(result, ['834556288'])

    def test_no_isbn_whatsoever(self):
        result = isbn(ReviewStubIsbn())()
        self.assertEqual(result, [])

    def test_issn_and_issn_online(self):
        result = isbn(ReviewStubIssn(issn='12-34', issn_online='5-678'))()
        self.assertEqual(result, ['1234', '5678'])

    def test_issn_only(self):
        result = isbn(ReviewStubIssn(issn='12-34'))()
        self.assertEqual(result, ['1234'])

    def test_issn_online_only(self):
        result = isbn(ReviewStubIssn(issn_online='834 5562 88'))()
        self.assertEqual(result, ['834556288'])

    def test_no_issn_whatsoever(self):
        result = isbn(ReviewStubIssn())()
        self.assertEqual(result, [])

    def test_year_and_year_online(self):
        result = get_field_and_ebook_variant(
            ReviewStubYear(year='2017', year_online='2018'),
            'getYearOfPublication')
        self.assertEqual(result, ['2017', '2018'])

    def test_year_only(self):
        result = get_field_and_ebook_variant(
            ReviewStubYear(year='2017'),
            'getYearOfPublication')
        self.assertEqual(result, ['2017'])

    def test_year_online_only(self):
        result = get_field_and_ebook_variant(
            ReviewStubYear(year_online='2017/2018'),
            'getYearOfPublication')
        self.assertEqual(result, ['2017/2018'])

    def test_no_year_whatsoever(self):
        result = get_field_and_ebook_variant(
            ReviewStubYear(),
            'getYearOfPublication')
        self.assertEqual(result, [])
