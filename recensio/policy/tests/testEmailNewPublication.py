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
        expected_mail = u'''Liebe Redaktion,
Die folgende Mail wurde generiert zur Benachrichtigung von %(reviewed_author)s. Bitte prüfen Sie sie und leiten sie ggf. weiter an

...

**********

Dear Mr %(reviewed_author)s,

Recently a text on the topic Test ReviewMonograph No 0 Dzieje pa\u0144stwa i spo\u0142ecze\u0144stwa 1890\u20131945 was published.
Its author \u0425\u0440\u0438\u0441\u0442\u043e \u0421\u0442\u043e\u0438\u0447\u043a\u043e\u0432 has presented the text on the review platform recensio.net and states that he/she has dealt with your research.

Here you can take a look at the presentation and comment on the presented statements. You will only need to register first (fast and free of charge) with your name and e-mail-address. This is necessary to prevent any misuse of the comment function and to maintain the platform’s scholarly claim.

For any further information/questions please feel free to contact the recensio.net editorial team:
 <fake>.

Yours sincerely
The recensio.net editorial team

recensio.net is a joint project of the Bavarian State Library (BSB) Munich, the German Historical Institute Paris (DHIP) and the Institute for European History (IEG) Mainz – funded by the German Research Foundation (DFG). Further information http://nohost/plone/konzept'''
        expected_mail_de = u'''Sehr geehrter Herr Tadeusz Kot\u0142owski,

vor Kurzem ist eine Schrift zum Thema Test ReviewMonograph No 0 Dzieje pa\u0144stwa i spo\u0142ecze\u0144stwa 1890\u20131945 erschienen. Der Autor \u0425\u0440\u0438\u0441\u0442\u043e \u0421\u0442\u043e\u0438\u0447\u043a\u043e\u0432 hat diese Schrift auf der Rezensionsplattform recensio.net pr\xe4sentiert und gibt an, sich mit Ihren Forschungen auseinandergesetzt zu haben.

Sie k\xf6nnen die Pr\xe4sentation hier einsehen und haben zugleich die Gelegenheit, die pr\xe4sentierten Thesen zu kommentieren. Daf\xfcr ist eine kurze, kostenlose Registrierung mit Namen und E-Mail-Adresse notwendig, die lediglich dazu dient, Missbrauch der Kommentarfunktion zu verhindern und den wissenschaftlichen Anspruch der Plattform zu wahren.

F\xfcr R\xfcckfragen steht Ihnen die recensio.net-Redaktion gern zur Verf\xfcgung:  <fake>.

Mit freundlichen Gr\xfc\xdfen,
Ihr recensio.net-Team

recensio.net ist ein DFG-gef\xf6rdertes Angebot der Bayerischen Staatsbibliothek, des Deutschen Historischen Instituts Paris und des Instituts f\xfcr Europ\xe4ische Geschichte Mainz. Weitere Informationen finden Sie unter http://nohost/plone/konzept'''
        portal = self.layer['portal']
        review = portal['sample-reviews']['newspapera'].summer['issue-2'].objectValues()[0]
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

        view = getMultiAdapter((review, request), name='mail_new_presentation')

        class MockMailHost(object):
            sentMail = ''
            def send(self, messageText, mto, mfrom, subject, charset):
                self.sentMail = messageText
        view.mailhost = MockMailHost()

        view()
        for lineno, (expected, real) in enumerate(
                                  zip(expected_mail.split('\n'),
                                      view.mailhost.sentMail.split('\n'))):
            self.assertTrue(compare(expected, real), ("Error in Line %i:\nExp:\n%s\nGot:\n%s" % (lineno, '\n'.join(expected_mail.split('\n')[max(0, lineno-2):lineno+3]), '\n'.join(view.mailhost.sentMail.split('\n')[max(0, lineno-2):lineno+3]))).encode('ascii', 'ignore'))
