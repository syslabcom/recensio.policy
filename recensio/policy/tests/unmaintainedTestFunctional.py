# -*- coding: utf-8 -*-
"""
Mainly testing recensio browser views, that no error is thrown when
the view is accessed.
"""
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
from recensio.policy.tests.layer import RECENSIO_FUNCTIONAL_TESTING
from urlparse import urljoin

import unittest2 as unittest


def raising(self, info):
    import traceback

    traceback.print_tb(info[2])
    print info[1]


SiteErrorLog.raising = raising


class TestMainSiteSections(unittest.TestCase):
    """Visit all the main sections of the site without getting an
    error
    """

    layer = RECENSIO_FUNCTIONAL_TESTING

    def get_manager_browser(self, portal):
        """The test content is not published, so we need to log in"""
        setRoles(portal, TEST_USER_ID, ["Manager"])
        self.browser = Browser(portal)
        self.browser.handleErrors = False
        self.portal.error_log._ignored_exceptions = ()
        portalURL = portal.absolute_url()
        self.browser.open(portalURL + "/login_form")
        self.browser.getControl(name="__ac_name").value = TEST_USER_NAME
        self.browser.getControl(name="__ac_password").value = TEST_USER_PASSWORD
        self.browser.getControl(name="submit").click()

    def setUp(self):
        self.portal = self.layer["portal"]
        self.site_root = self.portal.absolute_url() + "/"
        self.get_manager_browser(self.portal)

    def is_successful_status(self, path):
        """Open the path, and ensure 200 is returned"""
        self.browser.open(urljoin(self.site_root, path))
        self.assertTrue(
            self.browser.headers.dict["status"] == "200 Ok",
            msg="Error when trying to view %s" % self.browser.url,
        )

    def unmaintained_test_authorsearch_view(self):
        path = "autoren/index_html"
        self.is_successful_status(path)
        obj = self.portal.unrestrictedTraverse(path)
        self.assertEquals(obj.getProperty("layout", ""), "authorsearch")

    def unmaintained_test_browse_topics(self):
        path = "themen-epochen-regionen/index_html"
        self.is_successful_status(path)
        obj = self.portal.unrestrictedTraverse(path)
        self.assertEquals(obj.getProperty("layout", ""), "browse-topics")

    def unmaintained_test_publications_view(self):
        path = "rezensionen/zeitschriften"
        self.is_successful_status(path)
        obj = self.portal.unrestrictedTraverse(path)
        self.assertEquals(obj.layout, "publications-view")

    def unmaintained_test_personal_information_view(self):
        path = "personal-information"
        self.is_successful_status(path)

    def unmaintained_test_personal_information_view(self):
        path = "register"
        self.is_successful_status(path)

    def unmaintained_test_presentations(self):
        self.is_successful_status("praesentationen")

    def unmaintained_test_content_browsing_batching(self):
        self.is_successful_status("themen-epochen-regionen-en?b_start:int=10")

    def unmaintained_test_authors_batching(self):
        self.is_successful_status("autoren?b_start:int=30")

    def unmaintained_test_publication(self):
        self.is_successful_status("sample-reviews/newspapera")
        self.assertTrue(
            "Summer" in self.browser.contents,
            msg=("The example Volume is missing from the " "publicationlisting viewlet"),
        )
        self.assertTrue(
            "Issue 2" in self.browser.contents,
            msg=("The example Issue is missing from the " "publicationlisting viewlet"),
        )

    def unmaintained_test_search_form(self):
        self.is_successful_status("search_form")
