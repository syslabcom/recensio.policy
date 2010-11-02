# -*- coding: utf-8 -*-

import unittest2 as unittest
from doctest import OutputChecker, ELLIPSIS

from zope.component import getMultiAdapter
from zope.interface import directlyProvides

from plone.app.controlpanel.mail import IMailSchema
from Products.CMFCore.utils import getToolByName

from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING
from recensio.theme.interfaces import IRecensioLayer

class TestAuthorSearch(unittest.TestCase):
    layer = RECENSIO_INTEGRATION_TESTING

    def testAllAuthors(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request['ACTUAL_URL'] = 'test'
        view = getMultiAdapter((portal, request), name='authorsearch')
        expected = (' \xd0\xa1\xd1\x82\xd0\xbe\xd0\xb8\xd1\x87\xd0\xba\xd0\xbe\xd0\xb2', 'Fran\xc3\xa7ois Lam\xc3\xa8re', 'F\xc3\xbcrchtegott Huberm\xc3\xbcller', 'Harald Schmidt', 'Tadeusz Kot\xc5\x82owski', '\xd0\xa5\xd1\x80\xd0\xb8\xd1\x81\xd1\x82\xd0\xbe \xd0\xa1\xd1\x82\xd0\xbe\xd0\xb8\xd1\x87\xd0\xba\xd0\xbe\xd0\xb2')
        view()

        got = view.authors
        self.assertEquals(expected, got)

    def testLimitedAuthors(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request['ACTUAL_URL'] = 'test'
        request.set('authors', 'Schmidt')
        view = getMultiAdapter((portal, request), name='authorsearch')
        expected = ['Harald Schmidt']
        view()

        got = view.authors
        self.assertEquals(expected, got)
