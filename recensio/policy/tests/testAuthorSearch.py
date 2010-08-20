# -*- coding: utf-8 -*-

import unittest2 as unittest
from doctest import OutputChecker, ELLIPSIS

from zope.component import getMultiAdapter
from zope.interface import directlyProvides

from plone.app.testing import TEST_USER_NAME
from plone.app.testing import setRoles

from plone.app.controlpanel.mail import IMailSchema
from Products.CMFCore.utils import getToolByName

from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING
from recensio.theme.interfaces import IRecensioLayer

class TestAuthorSearch(unittest.TestCase):
    layer = RECENSIO_INTEGRATION_TESTING

    def testAllAuthors(self):
        portal = self.layer['portal']
        request = self.layer['request']
        view = getMultiAdapter((portal, request), name='authorsearch')
        expected = (u' \u0421\u0442\u043e\u0438\u0447\u043a\u043e\u0432', u'Dr. rer nat \u0425\u0440\u0438\u0441\u0442\u043e \u0421\u0442\u043e\u0438\u0447\u043a\u043e\u0432', u'Fran\xe7ois Lam\xe8re', u'F\xfcrchtegott Huberm\xfcller', u'Harald Schmidt', u'Tadeusz Kot\u0142owski')
        view()

        got = view.authors
        self.assertEquals(expected, got)

    def testLimitedAuthors(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request.set('authors', 'Schmidt')
        view = getMultiAdapter((portal, request), name='authorsearch')
        expected = [u'Harald Schmidt']
        view()

        got = view.authors
        self.assertEquals(expected, got)
