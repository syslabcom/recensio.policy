# -*- coding: utf-8 -*-
"""
Various functional tests
"""
import unittest2 as unittest
from urlparse import urljoin

from plone.testing.z2 import Browser
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles

from recensio.policy.tests.layer import RECENSIO_FUNCTIONAL_TESTING

def raising(self, info):
    import traceback
    traceback.print_tb(info[2])
    print info[1]

from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
SiteErrorLog.raising = raising

class TestMainSiteSections(unittest.TestCase):
    """ Visit all the main sections of the site without getting an
    error
    """
    layer = RECENSIO_FUNCTIONAL_TESTING

    def get_manager_browser(self, portal):
        """The test content is not published, so we need to log in"""
        setRoles(portal, TEST_USER_ID, ['Manager'])
        self.browser = Browser(portal)
        self.browser.handleErrors = False
        self.portal.error_log._ignored_exceptions = ()
        portalURL = portal.absolute_url()
        self.browser.open(portalURL + '/login_form')
        self.browser.getControl(name='__ac_name').value = TEST_USER_NAME
        self.browser.getControl(name='__ac_password').value = TEST_USER_PASSWORD
        self.browser.getControl(name='submit').click()

    def setUp(self):
        self.portal = self.layer["portal"]
        self.site_root = self.portal.absolute_url()+"/"
        self.get_manager_browser(self.portal)

    def is_successful_status(self, path):
        """Open the path, and ensure 200 is returned"""
        self.browser.open(urljoin(self.site_root, path))
        self.assertTrue(self.browser.headers.dict["status"] == "200 Ok",
                        msg="Error when trying to view %s" % self.browser.url
                        )

    def test_reviews(self):
        self.is_successful_status("rezensionen")

    def test_presentations(self):
        self.is_successful_status("praesentationen")

    def test_content_browsing(self):
        self.is_successful_status("themen-epochen-regionen")

    def test_content_browsing_batching(self):
        self.is_successful_status("themen-epochen-regionen-en?b_start:int=10")

    def test_authors(self):
        self.is_successful_status("autoren")

    def test_authors_batching(self):
        self.is_successful_status("autoren?b_start:int=30")

    def test_publication(self):
        self.is_successful_status("sample-reviews/newspapera")
        self.assertTrue("Summer" in self.browser.contents,
                        msg = ("The example Volume is missing from the "
                               "publicationlisting viewlet")
                        )
        self.assertTrue("Issue 2" in self.browser.contents,
                        msg = ("The example Issue is missing from the "
                               "publicationlisting viewlet")
                        )
