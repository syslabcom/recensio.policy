# -*- coding: utf-8 -*-

import unittest2 as unittest
from doctest import OutputChecker, ELLIPSIS

compare = lambda x, y:OutputChecker().check_output(x, y, ELLIPSIS)

from zope.component import getMultiAdapter
from zope.interface import alsoProvides

from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import setRoles

from plone.app.controlpanel.mail import IMailSchema
from Products.CMFCore.utils import getToolByName

from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING
from recensio.theme.interfaces import IRecensioLayer

class TestExcelImport(unittest.TestCase):
    layer = RECENSIO_INTEGRATION_TESTING

    def testFormat(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        setRoles(portal, TEST_USER_NAME, ['Manager'])
        request = self.layer['request']
        reviews = portal["sample-reviews"]
        reviews.invokeFactory('Publication', id='pub', title='pub')
        publication = reviews.pub
        publication.invokeFactory('Volume', id='vol', title='vol')
        vol = publication.vol
        vol.invokeFactory('Issue', id='issue', title='issue')
        issue = vol.issue
        pt = getToolByName(portal, 'portal_types')
        issueType = pt.getTypeInfo(issue)
        # We are lazy here, allowing an issue to contain all documents
        issueType.filter_content_types = False

        alsoProvides(request, IRecensioLayer)
        request['ACTUAL_URL'] = 'test'
        class FakeFile(file):
            filename = 'fake'
        request.form['pdf'] = FakeFile(
            '../../src/recensio.imports/samples/demo1.pdf')
        request.form['xls'] = FakeFile(
            '../../src/recensio.imports/samples/initial.xls')
        view = getMultiAdapter((issue, request), name='magazine_import')
        html = view()
        self.assertFalse('portalMessage error' in html)

        found = 0
        for obj in issue.objectValues():
            if obj.title == 'Titel der Rezension 2009':
                self.assertEquals('123456', obj.isbn)
                self.assertEquals('2009', obj.yearOfPublication)
                self.assertEquals('Rez. Vorname', obj.reviewAuthorFirstname)
                self.assertEquals('Rez. Nachname', obj.reviewAuthorLastname)
                self.assertEquals(({u'lastname': u'Autor Nachname', u'firstname': u'Autor Vorname'},), obj.authors)
                self.assertEquals('http://www.1.de', obj.uri)
                self.assertEquals(('en',), obj.languageReview)
                self.assertEquals(('de',), obj.languageReviewedText)
                self.assertEquals('Zitierschema', obj.customCitation)
                found += 1
            if obj.title == 'Titel Rezension 2010':
                self.assertEquals('124656', obj.issn)
                self.assertEquals('2010', obj.yearOfPublication)
                self.assertEquals('Rez. Vorname', obj.reviewAuthorFirstname)
                self.assertEquals('Rez. Nachname', obj.reviewAuthorLastname)
                self.assertEquals(3, obj.pageStart)
                self.assertEquals(5, obj.pageEnd)
                self.assertEquals('http://www.1.de', obj.uri)
                self.assertEquals(('az',), obj.languageReview)
                self.assertEquals(('cs',), obj.languageReviewedText)
                self.assertEquals('Zitierschema', obj.customCitation)
                found += 1

        self.assertEquals(2, found)
