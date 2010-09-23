# -*- coding: utf-8 -*-

import unittest2 as unittest
from doctest import OutputChecker, ELLIPSIS

compare = lambda x, y:OutputChecker().check_output(x, y, ELLIPSIS)

from DateTime import DateTime
from zope.component import getMultiAdapter
from zope.interface import directlyProvides, alsoProvides
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from plone.app.testing import TEST_USER_NAME
from plone.app.testing import setRoles, login

from plone.app.controlpanel.mail import IMailSchema
from Products.CMFCore.utils import getToolByName

from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING
from recensio.theme.interfaces import IRecensioLayer

class TestEmailFormat(unittest.TestCase):
    layer = RECENSIO_INTEGRATION_TESTING

    def testFormat(self):
        expected_mail = u'''Hallo admin,

Bis jetzt hat noch niemand auf Ihre Veröffentlichung geantwortet.
Das ist schade!

Vielleicht möchten Sie sich ihre Rezension mit ein wenig Abstand nochmal
anschauen und sehen, ob Sie was überarbeiten können, um mehr Aufmerksamkeit
der Recensio.net Besucher zu bekommen.

Auf Ihre Rezension kommen Sie übrigens über diesen Link:
http://...

Mit freundlichen Grüßen,

       Ihr Rezensio.net Team
'''
        portal = self.layer['portal']
        feeds = portal['RSS-feeds']
        request = self.layer['request']
        directlyProvides(request, IRecensioLayer)

        setRoles(portal, TEST_USER_NAME, ['Manager'])
        login(portal, TEST_USER_NAME)
        alsoProvides(request, IDefaultBrowserLayer)

        mail_schema = IMailSchema(portal)
        mail_schema.email_from_address = 'fake'
        membership_tool = getToolByName(portal, 'portal_membership')
        user = membership_tool.getMemberById('admin')
        user.setProperties({'email': 'fake@syslab.com'})

        view = getMultiAdapter((feeds, request), name='mail_uncommented_presentations')

        class MockMailHost(object):
            sentMail = ''
            def send(self, messageText, mto, mfrom, subject, charset):
                self.sentMail = messageText
        view.mailhost = MockMailHost()

        presentation = feeds.aq_parent.Members['fake_member'].objectValues()[0]
        criteria = feeds.discussion_three_months_old.crit__created_ATFriendlyDateCriteria
        good_creation_time = DateTime() - criteria.value
        presentation.setCreationDate(good_creation_time)
        getMultiAdapter((presentation, request), name='solr-maintenance').reindex()

        view()
        for lineno, (expected, real) in enumerate(
                                  zip(expected_mail.split('\n'),
                                      view.mailhost.sentMail.split('\n'))):
            self.assertTrue(compare(expected, real), ("Error in Line %i:\nExp:\n%s\nGot:\n%s" % (lineno, '\n'.join(expected_mail.split('\n')[max(0, lineno-2):lineno+3]), '\n'.join(view.mailhost.sentMail.split('\n')[max(0, lineno-2):lineno+3]))).encode('ascii', 'ignore'))
