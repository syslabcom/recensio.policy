# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.interface import directlyProvides

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

$(new_reviews)s

Neue Präsentationen ...

$(new_presentations)s

Verfolgen Sie die Diskussion über die meistkommentierten Präsentationen
des vergangenen Monats:

$(new_discussions)s
'''
        portal = self.layer['portal']
        feeds = portal['RSS-feeds']
        request = self.layer['request']
        directlyProvides(request, IRecensioLayer)

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
        self.assertEqual(expected_mail, view.mailhost.sentMail)
