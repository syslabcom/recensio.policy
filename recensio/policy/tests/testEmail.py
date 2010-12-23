# -*- coding: utf-8 -*-

import unittest2 as unittest
from doctest import OutputChecker, ELLIPSIS

compare = lambda x, y:OutputChecker().check_output(x, y, ELLIPSIS)

from zope.component import getMultiAdapter
from zope.interface import directlyProvides

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.app.controlpanel.mail import IMailSchema
from Products.CMFCore.utils import getToolByName

from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING
from recensio.theme.interfaces import IRecensioLayer

class TestEmailFormat(unittest.TestCase):
    layer = RECENSIO_INTEGRATION_TESTING

    def testFormat(self):
        expected_mail = u'''(English version see below)

**Liebe Abonnenten,**


wie jeden Monat freuen wir uns, Sie über Neuigkeiten auf recensio.net informieren zu können.

Angenehmes Stöbern und Entdecken wünscht Ihnen


*Ihre recensio.net-Redaktion.*


--------------------
Neue Rezensionen ...
--------------------

Zeitschrift 1
-------------
Test ReviewMonograph No 0
~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph...)


Test ReviewMonograph No 1
~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph...)


Test ReviewMonograph No 2
~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph...)


Weitere Ergebnisse finden Sie hier:
http://nohost/plone/RSS-feeds/new_reviews


Zeitschrift 2
-------------
test title
~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspaperb/summer/issue-2/ReviewMonograph...)



-----------------------
Neue Präsentationen ...
-----------------------

Präsentationen von Aufsätzen
----------------------------
Test PresentationArticleReview No 0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview...)


Test PresentationArticleReview No 1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview...)


Test PresentationArticleReview No 2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview...)


Weitere Ergebnisse finden Sie hier:
http://nohost/plone/RSS-feeds/new_presentations


Präsentationen von Internetressourcen
-------------------------------------
Test PresentationOnlineResource No 0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource...)


Test PresentationOnlineResource No 1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource...)


Test PresentationOnlineResource No 2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource...)


Weitere Ergebnisse finden Sie hier:
http://nohost/plone/RSS-feeds/new_presentations


Präsentationen von Monographien
-------------------------------
Test PresentationMonograph No 0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph...)


Test PresentationMonograph No 1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph...)


Test PresentationMonograph No 2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph...)


Weitere Ergebnisse finden Sie hier:
http://nohost/plone/RSS-feeds/new_presentations




-------------------------------------
Verfolgen Sie die Diskussion über ...
-------------------------------------

... die meistkommentierten Präsentationen des vergangenen Monats:
-----------------------------------------------------------------

test title (1 Comment)
~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspaperb/summer/issue-2/ReviewMonograph...)




*********************************************


**Dear subscribers,**


It’s time again for your monthly digest of news from recensio.net.

We hope you will enjoy browsing our platform and discovering its content.


*Your recensio.net editorial team*


---------------
New reviews ...
---------------

Zeitschrift 1
-------------
Test ReviewMonograph No 0
~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph...)


Test ReviewMonograph No 1
~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph...)


Test ReviewMonograph No 2
~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspapera/summer/issue-2/ReviewMonograph...)


Weitere Ergebnisse finden Sie hier:
http://nohost/plone/RSS-feeds/new_reviews


Zeitschrift 2
-------------
test title
~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspaperb/summer/issue-2/ReviewMonograph...)



---------------------
New presentations ...
---------------------

Präsentationen von Aufsätzen
----------------------------
Test PresentationArticleReview No 0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview...)


Test PresentationArticleReview No 1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview...)


Test PresentationArticleReview No 2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationArticleReview...)


Weitere Ergebnisse finden Sie hier:
http://nohost/plone/RSS-feeds/new_presentations


Präsentationen von Internetressourcen
-------------------------------------
Test PresentationOnlineResource No 0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource...)


Test PresentationOnlineResource No 1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource...)


Test PresentationOnlineResource No 2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationOnlineResource...)


Weitere Ergebnisse finden Sie hier:
http://nohost/plone/RSS-feeds/new_presentations


Präsentationen von Monographien
-------------------------------
Test PresentationMonograph No 0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph...)


Test PresentationMonograph No 1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph...)


Test PresentationMonograph No 2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/Members/fake_member/PresentationMonograph...)


Weitere Ergebnisse finden Sie hier:
http://nohost/plone/RSS-feeds/new_presentations




----------------------------
Follow the discussion on ...
----------------------------

... the presentations most commented on over the course of the past months:
---------------------------------------------------------------------------
test title (1 Comment)
~~~~~~~~~~~~~~~~~~~~~~~
(http://nohost/plone/sample-reviews/newspaperb/summer/issue-2/ReviewMonograph...)


'''
        portal = self.layer['portal']
        feeds = portal['RSS-feeds']
        request = self.layer['request']
        directlyProvides(request, IRecensioLayer)

        setRoles(portal, TEST_USER_ID, ['Manager'])

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
            self.assertTrue(compare(expected, real), ("Error in Line %i:\nExp:\n%s\nGot:\n%s" % (lineno, '\n'.join(expected_mail.split('\n')[lineno-2:lineno+3]), '\n'.join(view.mailhost.sentMail.split('\n')[lineno-2:lineno+3]))).encode('ascii', 'ignore'))
