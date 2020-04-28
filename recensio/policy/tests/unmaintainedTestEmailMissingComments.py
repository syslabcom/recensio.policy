# -*- coding: utf-8 -*-

from doctest import ELLIPSIS
from doctest import OutputChecker

import unittest2 as unittest
from DateTime import DateTime
from plone.app.controlpanel.mail import IMailSchema
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from Products.CMFCore.utils import getToolByName
from recensio.policy.interfaces import INewsletterSource
from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING
from recensio.theme.interfaces import IRecensioLayer
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from zope.interface import directlyProvides
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

compare = lambda x, y: OutputChecker().check_output(x, y, ELLIPSIS)






class TestEmailFormat(unittest.TestCase):
    layer = RECENSIO_INTEGRATION_TESTING

    def unmaintained_testFormat(self):
        expected_mail = u"""Dear Mr admins,

On ... you presented your text 
\tTest PresentationArticleReview No 0s
on recensio.net, but so far no comments have been left by other users. Do you want to modify your presentation? You could review the phrasing of your core statements or extend the number of stated reference authors. Usually these will be contacted by the recensio.net editorial staff, which greatly adds to the visibility of a presentation. If you haven’t done this yet, you may also add cover images and indeces (in the case of presentations of monographs).

If you have any further questions or require more information please feel free to contact the recensio.net editorial team:
Recensio.net <fake>.

Yours sincerely
The recensio.net editorial team"""

        portal = self.layer["portal"]
        feeds = portal["RSS-feeds"]
        request = self.layer["request"]
        directlyProvides(request, IRecensioLayer)

        setRoles(portal, TEST_USER_ID, ["Manager"])
        login(portal, TEST_USER_NAME)
        alsoProvides(request, IDefaultBrowserLayer)

        mail_schema = IMailSchema(portal)
        mail_schema.email_from_address = "fake"
        membership_tool = getToolByName(portal, "portal_membership")
        user = membership_tool.getMemberById("admin")
        user.setProperties({"email": "fake@syslab.com"})

        view = getMultiAdapter((feeds, request), name="mail_uncommented_presentations")

        class MockMailHost(object):
            sentMail = ""

            def send(self, messageText, mto, mfrom, subject, charset):
                self.sentMail = messageText

        view.mailhost = MockMailHost()

        presentation = feeds.aq_parent.Members["fake_member"].objectValues()[0]
        criteria = (
            feeds.discussion_three_months_old.crit__created_ATFriendlyDateCriteria
        )
        good_creation_time = DateTime() - criteria.value
        presentation.setCreationDate(good_creation_time)
        getMultiAdapter((presentation, request), name="solr-maintenance").reindex()

        view()
        for lineno, (expected, real) in enumerate(
            zip(expected_mail.split("\n"), view.mailhost.sentMail.split("\n"))
        ):
            self.assertTrue(
                compare(expected, real),
                (
                    "Error in Line %i:\nExp:\n%s\nGot:\n%s"
                    % (
                        lineno,
                        "\n".join(
                            expected_mail.split("\n")[max(0, lineno - 2) : lineno + 3]
                        ),
                        "\n".join(
                            view.mailhost.sentMail.split("\n")[
                                max(0, lineno - 2) : lineno + 3
                            ]
                        ),
                    )
                ).encode("ascii", "ignore"),
            )
