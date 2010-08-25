# -*- coding: utf-8 -*-

import unittest2 as unittest
from doctest import OutputChecker, ELLIPSIS

compare = lambda x, y:OutputChecker().check_output(x, y, ELLIPSIS)

from zope.component import getMultiAdapter
from zope.interface import directlyProvides

from plone.app.testing import TEST_USER_NAME
from plone.app.testing import setRoles

from plone.app.controlpanel.mail import IMailSchema
from Products.CMFCore.utils import getToolByName

from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING
from recensio.theme.interfaces import IRecensioLayer

class TestEmailFormat(unittest.TestCase):
    layer = RECENSIO_INTEGRATION_TESTING

    def testFormat(self):
        expected_mail = u'''Liebe Abonnenten,

wie jeden Monat freuen wir uns, Sie über Neuigkeiten auf recensio.net
informieren zu können.

Angenehmes Stöbern und Entdecken wünscht Ihnen Ihre recensio.net-Redaktion.

Neue Rezensionen ...


Typ: Review Monograph

Test ReviewMonograph No 0 (http://nohost...)



Created on: ...
--------------------------------------------
Test ReviewMonograph No 1 (http://nohost...)



Created on: ...
--------------------------------------------
Test ReviewMonograph No 2 (http://nohost...)



Created on: ...
--------------------------------------------
Test ReviewMonograph No 3 (http://nohost...)



Created on: ...
--------------------------------------------
Test ReviewMonograph No 4 (http://nohost...)



Created on: ...
--------------------------------------------
Test ReviewMonograph No 5 (http://nohost...)



Created on: ...
--------------------------------------------
Test ReviewMonograph No 6 (http://nohost...)



Created on: ...
--------------------------------------------
Test ReviewMonograph No 7 (http://nohost...)



Created on: ...
--------------------------------------------
Test ReviewMonograph No 8 (http://nohost...)



Created on: ...
--------------------------------------------
Test ReviewMonograph No 9 (http://nohost...)



Created on: ...
--------------------------------------------

Typ: Review Journal

Test ReviewJournal No 0 (http://nohost...)



Created on: ...
--------------------------------------------
Test ReviewJournal No 1 (http://nohost...)



Created on: ...
--------------------------------------------
Test ReviewJournal No 2 (http://nohost...)



Created on: ...
--------------------------------------------
Test ReviewJournal No 3 (http://nohost...)



Created on: ...
--------------------------------------------
Test ReviewJournal No 4 (http://nohost...)



Created on: ...
--------------------------------------------
Test ReviewJournal No 5 (http://nohost...)



Created on: ...
--------------------------------------------
Test ReviewJournal No 6 (http://nohost...)



Created on: ...
--------------------------------------------
Test ReviewJournal No 7 (http://nohost...)



Created on: ...
--------------------------------------------
Test ReviewJournal No 8 (http://nohost...)



Created on: ...
--------------------------------------------
Test ReviewJournal No 9 (http://nohost...)



Created on: ...
--------------------------------------------


Neue Präsentationen ...


Typ: Presentation Article Review

Test PresentationArticleReview No 0 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationArticleReview No 1 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationArticleReview No 2 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationArticleReview No 3 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationArticleReview No 4 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationArticleReview No 5 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationArticleReview No 6 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationArticleReview No 7 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationArticleReview No 8 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationArticleReview No 9 (http://nohost...)



Created on: ...
--------------------------------------------

Typ: Presentation Collection

Test PresentationCollection No 0 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationCollection No 1 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationCollection No 2 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationCollection No 3 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationCollection No 4 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationCollection No 5 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationCollection No 6 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationCollection No 7 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationCollection No 8 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationCollection No 9 (http://nohost...)



Created on: ...
--------------------------------------------

Typ: Presentation Online Resource

Test PresentationOnlineResource No 0 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationOnlineResource No 1 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationOnlineResource No 2 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationOnlineResource No 3 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationOnlineResource No 4 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationOnlineResource No 5 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationOnlineResource No 6 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationOnlineResource No 7 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationOnlineResource No 8 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationOnlineResource No 9 (http://nohost...)



Created on: ...
--------------------------------------------

Typ: Presentation Monograph

Test PresentationMonograph No 0 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationMonograph No 1 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationMonograph No 2 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationMonograph No 3 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationMonograph No 4 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationMonograph No 5 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationMonograph No 6 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationMonograph No 7 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationMonograph No 8 (http://nohost...)



Created on: ...
--------------------------------------------
Test PresentationMonograph No 9 (http://nohost...)



Created on: ...
--------------------------------------------


Verfolgen Sie die Diskussion über die meistkommentierten Präsentationen
des vergangenen Monats:



'''
        portal = self.layer['portal']
        feeds = portal['RSS-feeds']
        request = self.layer['request']
        directlyProvides(request, IRecensioLayer)

        setRoles(portal, TEST_USER_NAME, ['Manager'])

        mail_schema = IMailSchema(portal)
        mail_schema.email_from_address = 'fake'
        membership_tool = getToolByName(portal, 'portal_membership')
        user = membership_tool.getAuthenticatedMember()
        user.setProperties({'email': 'fake@syslab.com'})

        view = getMultiAdapter((feeds, request), name='mail_results')

        class MockMailHost(object):
            sentMail = ''
            def send(self, messageText, mto, mfrom, subject, charset):
                self.sentMail = messageText
        view.mailhost = MockMailHost()

        view()
        for lineno, (expected, real) in enumerate(
                                  zip(expected_mail.split('\n'),
                                      view.mailhost.sentMail.split('\n'))):
            self.assertTrue(compare(expected, real), "Error in Line %i:\nExp: '%s'\nGot: '%s'" % (lineno, expected, real))
