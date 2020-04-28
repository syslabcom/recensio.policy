# -*- coding: utf-8 -*-
from mock import Mock
from zope.interface import alsoProvides
import unittest


class TestNewsletter(unittest.TestCase):
    def unmaintained_test_newsletter(self):
        from recensio.policy.browser.email import MailCollection
        from recensio.policy.interfaces import INewsletterSettings
        from Products.statusmessages.interfaces import IStatusMessage
        from plone.app.controlpanel.mail import IMailSchema

        context = Mock()
        request = Mock()
        mailhost = Mock()
        new_reviews = Mock()
        new_presentations = Mock()
        new_discussions = Mock()
        new_issues = Mock()
        newsletter_settings = Mock()
        newsletter_settings.mail_template = INewsletterSettings["mail_template"].default
        context.new_reviews = new_reviews
        context.new_presentations = new_presentations
        context.new_discussions = new_discussions
        context.new_issues = new_issues
        context.new_reviews.queryCatalog = lambda: self.makeReviews()
        context.new_presentations.queryCatalog = lambda: self.makePresentations()
        context.new_discussions.queryCatalog = lambda: self.makeDiscussions()
        context.new_issues.queryCatalog = lambda: self.makeIssues()
        ts = Mock()

        def translate(a, context=None, mapping=None):
            return a

        ts.translate = translate
        root = Mock()
        alsoProvides(request, IStatusMessage)
        alsoProvides(root, IMailSchema)
        view = MailCollection(context, request)
        view.getNewsletterSettings = lambda: newsletter_settings
        view.mailhost = mailhost
        view.ts = ts
        view.root = root
        view()
        self.assertEquals(1, len(mailhost.method_calls))
        self.assertTrue(len(mailhost.method_calls[0][2]["message"]))

    def makeReviews(self):
        for art_num in range(10):
            cat = Mock()
            review = Mock()
            cat.getObject = lambda: review
            review.get_publication_title = lambda: "Mag Noö: %i" % (art_num / 2)
            review.getDecoratedTitle = (
                lambda: review.get_publication_title().decode("utf-8") + "Decorated!"
            )
            review.absolute_url = lambda: "http://www.example.com/"
            yield cat

    def makePresentations(self):
        content_types = [
            "Presentation Article Review",
            "Presentation Collection",
            "Presentation Monograph",
            "Presentation Online Resource",
        ]
        for art_num in range(10):
            catalog_entry = Mock()
            presentation = Mock()
            presentation.getDecoratedTitle = (
                lambda: u"öDecorated title no: %i" % art_num
            )
            catalog_entry.getObject = lambda: presentation
            catalog_entry.getURL = lambda: "http://www.example.com/"
            catalog_entry.portal_type = content_types[art_num % len(content_types)]
            yield catalog_entry

    def makeDiscussions(self):
        for art_num in range(10):
            catalog_entry = Mock()
            catalog_entry.total_comments = art_num
            catalog_entry.getURL = lambda: "http://www.example.com/"
            discussion_item = Mock()
            catalog_entry.getObject = lambda: discussion_item
            discussion_item.getDecoratedTitle = lambda: u"öDecorated Title %i" % art_num
            yield catalog_entry

    def makeIssues(self):
        magazines = [u"A Magazine", u"Another Magazine", u"A Third Magazine"]
        for art_num in range(10):
            catalog_entry = Mock()
            pub = Mock()
            pub.Title = lambda: magazines[art_num % 3]
            iss = Mock()
            iss.Title = lambda: u"%02d" % (9 ** art_num % 7)
            iss.getParentNode = lambda: pub
            obj = Mock()
            obj.getParentNode = lambda: iss
            catalog_entry.getObject = lambda: obj
            catalog_entry.Title = u"%01d" % art_num
            yield catalog_entry
