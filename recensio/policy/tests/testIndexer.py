# -* coding: utf-8 *-
import unittest

from recensio.policy.indexer import get_field_and_ebook_variant
from recensio.policy.indexer import isbn
from recensio.policy.indexer import place
from recensio.policy.indexer import titleOrShortname


class ReviewStubIsbn(object):
    def __init__(self, isbn="", isbn_online=""):
        self.isbn = isbn
        self.isbn_online = isbn_online

    def getIsbn(self):
        return self.isbn

    def getIsbn_online(self):
        return self.isbn_online


class ReviewStubIssn(object):
    def __init__(self, issn="", issn_online=""):
        self.issn = issn
        self.issn_online = issn_online

    def getIssn(self):
        return self.issn

    def getIssn_online(self):
        return self.issn_online


class ReviewStubYear(object):
    def __init__(self, year="", year_online=""):
        self.year = year
        self.year_online = year_online

    def getYearOfPublication(self):
        return self.year

    def getYearOfPublicationOnline(self):
        return self.year_online


class ReviewStubPlace(object):
    def __init__(self, place="", place_online=""):
        self.place = place
        self.place_online = place_online

    def getPlaceOfPublication(self):
        return self.place

    def getPlaceOfPublicationOnline(self):
        return self.place_online


class ReviewStubDates(object):
    def __init__(self, dates=""):
        self.dates = dates

    def getDates(self):
        return self.dates


class ReviewStubTitles(object):
    def __init__(self, title="", subtitle=""):
        self.title = title
        self.subtitle = subtitle

    def Title(self):
        return self.title

    def getSubtitle(self):
        return self.subtitle

    def getField(self, field):
        return None


class TestIndexer(unittest.TestCase):
    def test_isbn_and_isbn_online(self):
        result = isbn(ReviewStubIsbn(isbn="12-34", isbn_online="5-678"))()
        self.assertEqual(result, ["1234", "5678"])

    def test_isbn_only(self):
        result = isbn(ReviewStubIsbn(isbn="12-34"))()
        self.assertEqual(result, ["1234"])

    def test_isbn_online_only(self):
        result = isbn(ReviewStubIsbn(isbn_online="834 5562 88"))()
        self.assertEqual(result, ["834556288"])

    def test_no_isbn_whatsoever(self):
        result = isbn(ReviewStubIsbn())()
        self.assertEqual(result, [])

    def test_issn_and_issn_online(self):
        result = isbn(ReviewStubIssn(issn="12-34", issn_online="5-678"))()
        self.assertEqual(result, ["1234", "5678"])

    def test_issn_only(self):
        result = isbn(ReviewStubIssn(issn="12-34"))()
        self.assertEqual(result, ["1234"])

    def test_issn_online_only(self):
        result = isbn(ReviewStubIssn(issn_online="834 5562 88"))()
        self.assertEqual(result, ["834556288"])

    def test_no_issn_whatsoever(self):
        result = isbn(ReviewStubIssn())()
        self.assertEqual(result, [])

    def test_year_and_year_online(self):
        result = get_field_and_ebook_variant(
            ReviewStubYear(year="2017", year_online="2018"), "getYearOfPublication"
        )
        self.assertEqual(result, ["2017", "2018"])

    def test_year_only(self):
        result = get_field_and_ebook_variant(
            ReviewStubYear(year="2017"), "getYearOfPublication"
        )
        self.assertEqual(result, ["2017"])

    def test_year_online_only(self):
        result = get_field_and_ebook_variant(
            ReviewStubYear(year_online="2017/2018"), "getYearOfPublication"
        )
        self.assertEqual(result, ["2017/2018"])

    def test_no_year_whatsoever(self):
        result = get_field_and_ebook_variant(ReviewStubYear(), "getYearOfPublication")
        self.assertEqual(result, [])

    def test_place_of_publication(self):
        result = place(ReviewStubPlace(place="Düsseldorf"))()
        self.assertEqual(result, ["Düsseldorf"])

    def test_dates(self):
        result = place(ReviewStubDates(dates=[{"place": "Düsseldorf"}]))()
        self.assertEqual(result, ["Düsseldorf"])

    def test_titleOrShorname(self):
        result = titleOrShortname(ReviewStubTitles(title="Führungsstil"))()
        self.assertEqual(result, ["Führungsstil", ""])
