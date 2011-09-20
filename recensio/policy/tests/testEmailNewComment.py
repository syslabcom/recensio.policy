# -*- coding: utf-8 -*-
import unittest2 as unittest
from doctest import OutputChecker, ELLIPSIS

compare = lambda x, y:OutputChecker().check_output(x, y, ELLIPSIS)

from zope.component import getMultiAdapter
from zope.interface import directlyProvides, alsoProvides
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.component import createObject

from plone.app.testing import TEST_USER_NAME, TEST_USER_ID
from plone.app.testing import setRoles, login

from plone.app.controlpanel.mail import IMailSchema
from Products.CMFCore.utils import getToolByName

from plone.app.discussion.interfaces import IConversation
from plone.app.discussion.comment import Comment

from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING
from recensio.theme.interfaces import IRecensioLayer

from recensio.policy.browser.email import MailNewComment

from Acquisition import aq_inner

class TestEmailFormat(unittest.TestCase):
    layer = RECENSIO_INTEGRATION_TESTING

    def testFormat(self):
        expected_mail = {'Review Monograph': [u'''From: Recensio.net <fake>
To: Recensio.net <fake>
Bcc: notification.archive@lists.recensio.net
Subject: Benachrichtigung über Kommentareingang

Sehr geehrte/r Tadeusz Kotłowski,

zu Ihrer Schrift
    Tadeusz Kotłowski: Test ReviewMonograph No 0: Dzieje państwa i społeczeństwa 1890–1945, 2008, 978-83-60448-39-7 (rezensiert von Стоичков, Христо)

erschien eine Rezension in der Zeitschrift
Zeitschrift 1, Summer, Issue 2. Diese Rezension wurde auf der Rezensionsplattform recensio.net publiziert.
Jack Commenter hat am ... diese Rezension bzw. Ihre Schrift kommentiert. Sie haben hier die Gelegenheit, den Kommentar zu lesen und ggf. darauf zu reagieren:

http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph...

Für Rückfragen steht Ihnen die recensio.net-Redaktion gern zur Verfügung: Recensio.net <fake>.

Mit freundlichen Grüßen,
Ihr recensio.net-Team''',
                                            u'''From: Recensio.net <fake>
To: hc@example.org
Bcc: notification.archive@lists.recensio.net
Subject: Benachrichtigung über Kommentareingang

Sehr geehrte/r Hugh Commenter,

Sie haben die Schrift bzw. die Internetressource
    Tadeusz Kotłowski: Test ReviewMonograph No 0: Dzieje państwa i społeczeństwa 1890–1945, 2008, 978-83-60448-39-7 (rezensiert von Стоичков, Христо) in Zeitschrift 1, Summer, Issue 2

auf recensio.net kommentiert. Jack Commenter hat am ... einen weiteren Kommentar abgegeben. Sie haben hier die Gelegenheit, diesen zu lesen und ggf. darauf zu reagieren:

http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph...

Für Rückfragen steht Ihnen die recensio.net-Redaktion gern zur Verfügung: Recensio.net <fake>.

Mit freundlichen Grüßen,
Ihr recensio.net-Team'''],
                         'Presentation Article Review': [u'''From: Recensio.net <fake>
To: hc@example.org
Bcc: notification.archive@lists.recensio.net
Subject: Benachrichtigung über Kommentareingang

Sehr geehrte/r Hugh Commenter,

Sie haben die Schrift bzw. die Internetressource
    Tadeusz Kotłowski: Test PresentationArticleReview No 0: Dzieje państwa i społeczeństwa 1890–1945, 2008,  (präsentiert von Стоичков, Христо)

auf recensio.net kommentiert. Jack Commenter hat am ... einen weiteren Kommentar abgegeben. Sie haben hier die Gelegenheit, diesen zu lesen und ggf. darauf zu reagieren:

http://nohost/plone/Members/fake_member/PresentationArticleReview...

Für Rückfragen steht Ihnen die recensio.net-Redaktion gern zur Verfügung: Recensio.net <fake>.

Mit freundlichen Grüßen,
Ihr recensio.net-Team''']}

        portal = self.layer['portal']
        reviews = [portal['sample-reviews']['newspapera']['summer']['issue-2'].objectValues()[0], 
            portal.Members['fake_member'].objectValues()[0]]

        request = self.layer['request']
        directlyProvides(request, IRecensioLayer)

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        alsoProvides(request, IDefaultBrowserLayer)

        membership_tool = getToolByName(portal, 'portal_membership')
        membership_tool.addMember('commenter', '12345', [], [], properties={'email': 'jc@example.org', 'preferred_language': 'de'})
        membership_tool.addMember('commenter2', '12345', [], [], properties={'email': 'hc@example.org', 'preferred_language': 'de'})

        for review in reviews:
            conversation = IConversation(aq_inner(review))
            comment = createObject('plone.Comment')
            comment.author_username = 'commenter'
            comment.author_name = 'Jack Commenter'
            comment.author_email = 'jc@example.org'
            comment.text = 'Comment Text!'
            conversation.addComment(comment)
            comment2 = createObject('plone.Comment')
            comment2.author_username = 'commenter2'
            comment2.author_name = 'Hugh Commenter'
            comment2.author_email = 'hc@example.org'
            comment2.text = 'Second Comment Text!'
            conversation.addComment(comment2)

            mail_schema = IMailSchema(portal)
            mail_schema.email_from_address = 'fake'

            comment2 = conversation.items()[0][1]
            view = getMultiAdapter((comment2, request), name='notify_author_new_comment')
            class MockMailHost(object):
                sentMail = []
                def send(self, messageText, mto, mfrom, subject, charset):
                    self.sentMail.append(messageText)
            view.mailhost = MockMailHost()
            #view.ts = getToolByName(portal, 'translation_service')

            view()
            self.assertEquals(len(view.mailhost.sentMail), len(expected_mail[review.portal_type]))
            for i in range(len(view.mailhost.sentMail)):
                for lineno, (expected, real) in enumerate(
                                          zip(expected_mail[review.portal_type][i].split('\n'),
                                              view.mailhost.sentMail[i].split('\n'))):
                    self.assertTrue(compare(expected, real), ("Error in Line %i:\nExp:\n%s\nGot:\n%s" % (lineno, '<<<\n'.join(expected_mail[review.portal_type][i].split('\n')[max(0, lineno-2):lineno+3]), '<<<\n'.join(view.mailhost.sentMail[i].split('\n')[max(0, lineno-2):lineno+3]))).encode('ascii', 'ignore'))
