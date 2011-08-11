# -*- coding: utf-8 -*-
"""
Various functional tests


Recensio specific browser views (recensio/policy/scripts/list_browser_views.sh):

| FOR                                                     | NAME                           | Tests  |
|---------------------------------------------------------+--------------------------------+--------|
| all                                                     | authorsearch                   |        |
| all                                                     | browse-topics                  |        |
| all                                                     | create-new-presentation        |        |
| all                                                     | fixer1                         |        |
| all                                                     | manage-my-presentations        |        |
| all                                                     | newsletter-view                |        |
| all                                                     | publications-view              |        |
| all                                                     | recensioview                   |        |
| all                                                     | recensio_workflow_helper       |        |
| ..interfaces.IReview                                    | pageviewer                     |        |
| ..interfaces.IReview                                    | review_view                    |        |
| OFS.interfaces.IFolder                                  | magazine_import                |        |
| plone.app.discussion.interfaces.IComment                | notify_author_new_comment      |        |
| plone.app.layout.navigation.interfaces.INavigationRoot  | personal-information           |        |
| plone.app.layout.navigation.interfaces.INavigationRoot  | register                       |        |
| Products.ATContentTypes.interfaces.document.IATDocument | homepage-view                  |        |
| Products.ATContentTypes.interfaces.topic.IATTopic       | digitool_export                |        |
| Products.CMFCore.interfaces.ISiteRoot                   | xmlrpc_import                  |        |
| Products.CMFPlone.interfaces.IPloneSiteRoot             | newsletter-settings            |        |
| Products.CMFPlone.interfaces.IPloneSiteRoot             | opac                           |        |
| Products.CMFPlone.interfaces.IPloneSiteRoot             | perspektivia-import            |        |
| Products.CMFPlone.interfaces.IPloneSiteRoot             | recensio-import-settings       |        |
| Products.CMFPlone.interfaces.IPloneSiteRoot             | recensio-settings              |        |
| Products.CMFPlone.interfaces.IPloneSiteRoot             | sehepunkte-import              |        |
| Products.CMFPlone.interfaces.IPloneSiteRoot             | sitemap.xml.gz                 |        |
| recensio.contenttypes.interfaces.IReview                | generate-pdf-recension         |        |
| recensio.contenttypes.interfaces.IReviewMonograph       | generate-pdf-recension         |        |
| recensio.contenttypes.interfaces.review.IReview         | cut_pdf                        |        |
| recensio.contenttypes.interfaces.review.IReview         | mail_new_presentation          |        |
| recensio.policy.interfaces.INewsletterSource            | mail_results                   |        |
| recensio.policy.interfaces.INewsletterSource            | mail_uncommented_presentations |        |


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
        # obj = self.portal.unrestrictedTraverse("/plone/%s" %path)
        # print "path:\n\t%s\nview:\n\t%s\n\n" %(
        #     path, getattr(obj, "default_view"))
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

