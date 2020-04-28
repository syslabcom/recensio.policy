# -*- coding: utf-8 -*-

import unittest2 as unittest
from doctest import OutputChecker, ELLIPSIS
from mock import Mock
from pkg_resources import resource_filename

compare = lambda x, y: OutputChecker().check_output(x, y, ELLIPSIS)

from zope.component import getMultiAdapter
from zope.interface import alsoProvides

from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import setRoles

from plone.app.controlpanel.mail import IMailSchema
from Products.CMFCore.utils import getToolByName

from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING
from recensio.theme.interfaces import IRecensioLayer


class FakeFile(file):
    filename = "fake"


class TestExcelImportUnit(unittest.TestCase):
    def testLanguageValidation(self):
        from recensio.imports.excel_converter import ExcelConverter

        converter = ExcelConverter()
        converter._supported_languages = ("en", "fr")
        self.assertEquals(("en", "fr"), converter.convertLanguages("en, fr"))

    def testLanguageValidationLowerEverything(self):
        from recensio.imports.excel_converter import ExcelConverter

        converter = ExcelConverter()
        converter._supported_languages = ("en", "fr")
        self.assertEquals(("en", "fr"), converter.convertLanguages("en, fr"))

    def testLanguageValidationFunnyDividers(self):
        from recensio.imports.excel_converter import ExcelConverter

        converter = ExcelConverter()
        converter._supported_languages = ("en", "fr")
        for i in (
            "en,fr",
            "fr,en",
            "fr,,en",
            "fr:en",
            "fr;en",
            "fr.en",
            "fr    en",
            "fr\nen",
            "fr\ten",
            "fr\ren",
        ):
            self.assertEquals(
                set(("en", "fr")),
                set(converter.convertLanguages(i)),
                "%s not as expected" % str(i),
            )

    def testLanguageValidationMissingLang(self):
        from recensio.imports.excel_converter import ExcelConverter

        converter = ExcelConverter()
        converter._supported_languages = ("en", "fr")
        self.assertEquals(("en", "fr"), converter.convertLanguages("en, fr, es"))
        self.assertEquals(['The language "${lang}" is unknown'], converter.warnings)


class TestZipImport(unittest.TestCase):
    def unmaintained_testZipImport(self):
        from recensio.imports import browser

        addOneItem = Mock()
        browser.addOneItem = addOneItem
        view = browser.MagazineImport()
        view.zip_extractor = lambda x: (None, [1, 2])
        view.excel_converter = Mock()
        view.excel_converter.convert_zip = lambda x: [
            {"portal_type": [1, 2]},
            {"portal_type": [1, 2]},
        ]
        view.type_getter = lambda a, b: None
        view.context = None
        view.addZIPContent(None)
        self.assertEquals(2, len(view.results))
        xls = FakeFile("../../src/recensio.imports/samples/ziptest.zip")

    def testZipImportMissingDocs(self):
        from recensio.imports import browser

        addOneItem = Mock()
        browser.addOneItem = addOneItem
        view = browser.MagazineImport()
        view.zip_extractor = lambda x: (None, [1, 2])
        view.excel_converter_zip = lambda x: [{"portal_type": [1, 2]}]
        view.type_getter = lambda a, b: None
        view.context = None
        self.assertRaises(browser.FrontendException, view.addZIPContent, None)

    def unmaintained_testZipExtractor(self):
        from recensio.imports.zip_extractor import ZipExtractor

        extractor = ZipExtractor()
        zipfile = file(
            resource_filename(
                __name__, "../../../../recensio.imports/samples" "/ziptest.zip"
            )
        )
        xls, docs = extractor(zipfile)
        docs = [x for x in docs]
        self.assertEquals(2, len(docs))

    def unmaintained_testExcelConverterForZip(self):
        from recensio.imports.excel_converter import ExcelConverter

        converter = ExcelConverter()
        converter._supported_languages = ("de", "en")
        xls = file(
            resource_filename(
                __name__,
                "../../../../recensio.imports/samples" "/recensioupload_DE_zip.xls",
            )
        )
        results = list(converter.convert_zip(xls))
        self.assertEquals(2, len(results))


class testexcelimport(unittest.TestCase):
    layer = RECENSIO_INTEGRATION_TESTING

    def unmaintained_testGermanFormat(self):
        self._testFormat("recensioupload_DE.xls")

    def unmaintained_testEnglishFormat(self):
        self._testFormat("recensioupload_EN.xls")

    def _testFormat(self, filename):
        portal = self.layer["portal"]
        setRoles(portal, TEST_USER_ID, ["Manager"])
        request = self.layer["request"]
        reviews = portal["sample-reviews"]
        reviews.invokeFactory("Publication", id="pub", title="pub")
        publication = reviews.pub
        publication.invokeFactory("Volume", id="vol", title="vol")
        vol = publication.vol
        vol.invokeFactory("Issue", id="issue", title="issue")
        issue = vol.issue
        pt = getToolByName(portal, "portal_types")
        issueType = pt.getTypeInfo(issue)
        # We are lazy here, allowing an issue to contain all documents
        issueType.filter_content_types = False

        alsoProvides(request, IRecensioLayer)
        request["ACTUAL_URL"] = "test"
        request.form["pdf"] = FakeFile("../../src/recensio.imports/samples/demo1.pdf")
        request.form["xls"] = FakeFile(
            "../../src/recensio.imports/samples/%s" % filename
        )
        view = getMultiAdapter((issue, request), name="magazine_import")
        view.excel_converter._supported_languages = ("de", "en")
        html = view()
        self.assertFalse("portalMessage error" in html)

        found = 0
        for obj in issue.objectValues():
            if obj.title == "Titel der Rezension 2009":
                self.assertEquals("123456", obj.isbn)
                self.assertEquals("2009", obj.yearOfPublication)
                self.assertEquals("http://www.1.de", obj.uri)
                self.assertEquals(("en",), obj.languageReview)
                self.assertEquals(("de",), obj.languageReviewedText)
                self.assertEquals(3, obj.pageStartOfReviewInJournal)
                self.assertEquals(4, obj.pageEndOfReviewInJournal)
                self.assertEquals("Zitierschema", obj.customCitation)
                found += 1
            if obj.title == "Titel Rezension 2010":
                self.assertEquals("124656", obj.issn)
                self.assertEquals("2010", obj.yearOfPublication)
                self.assertEquals("Rez. Vorname", obj.reviewAuthors[0]["firstname"])
                self.assertEquals("Rez. Nachname", obj.reviewAuthors[0]["lastname"])
                self.assertEquals(5, obj.pageStartOfReviewInJournal)
                self.assertEquals(6, obj.pageEndOfReviewInJournal)
                self.assertEquals("http://www.1.de", obj.uri)
                self.assertEquals(tuple(), obj.languageReview)
                self.assertEquals(tuple(), obj.languageReviewedText)
                self.assertEquals("Zitierschema", obj.customCitation)
                found += 1

        self.assertEquals(2, found)
