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

    def unmaintained_testAllAuthors(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request['ACTUAL_URL'] = 'test'
        view = getMultiAdapter((portal, request), name='authorsearch')
        expected = [
#            {'reviews': 0, 'comments': 0, 'presentations': 0,
#             'name': 'Huberm\xc3\xbcller, F\xc3\xbcrchtegott'},
#            {'reviews': 0, 'comments': 0, 'presentations': 0,
#             'name': 'Kot\xc5\x82owski, Tadeusz'},
#            {'reviews': 0, 'comments': 0, 'presentations': 0,
#             'name': 'Lam\xc3\xa8re, Fran\xc3\xa7ois'},
#            {'reviews': 0, 'comments': 0, 'presentations': 0,
#             'name': 'Schmidt, Harald'},
#            {'reviews': 0, 'comments': 0, 'presentations': 0,
#             'name': ('\xd0\xa1\xd1\x82\xd0\xbe\xd0\xb8\xd1\x87\xd0\xba\xd0\xbe'
#                      '\xd0\xb2, ')},
#            {'reviews': 0, 'comments': 0, 'presentations': 0,
#            'name': ('\xd0\xa1\xd1\x82\xd0\xbe\xd0\xb8\xd1\x87\xd0\xba\xd0\xbe'
#                     '\xd0\xb2, \xd0\xa5\xd1\x80\xd0\xb8\xd1\x81\xd1\x82\xd0'
#
#                     '\xbe')}
            ]
        view()

        got = view.authors
        self.assertEquals(expected, got)

    def unmaintained_testLimitedAuthors(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request['ACTUAL_URL'] = 'test'
        request.set('authors', 'Schmidt')
        view = getMultiAdapter((portal, request), name='authorsearch')
        expected = [
#            {'reviews': 0, 'comments': 0, 'presentations': 0,
#             'name': 'Schmidt, Harald'}
        ]
        view()

        got = view.authors
        self.assertEquals(expected, got)
