from plone import api
from recensio.policy.browser.export import MetadataExport
from recensio.policy.browser.email import MailCollection
from recensio.policy.browser.sehepunkte import Import
from recensio.policy.export import register_doi
from slc.zopescript.script import ConsoleScript
import logging

log = logging.getLogger()


class MetadataExportScript(ConsoleScript):
    def run(self):
        me = MetadataExport(self.portal, self.portal.REQUEST)
        me()


class NewsletterScript(ConsoleScript):
    def run(self):
        rss_feeds = self.portal.unrestrictedTraverse('/recensio/RSS-feeds')
        mc = MailCollection(rss_feeds, rss_feeds.REQUEST)
        mc()


class SehepunkteImportScript(ConsoleScript):
    def run(self):
        si = Import(self.portal, self.portal.REQUEST)
        si()


class RegisterAllDOIsScript(ConsoleScript):
    def issues_and_volumes(self):
        pc = api.portal.get_tool('portal_catalog')
        parent_path = dict(query='/'.join(self.portal.getPhysicalPath()))
        results = pc(review_state="published",
                     portal_type=("Issue", "Volume"),
                     path=parent_path)
        for item in results:
            yield item.getObject()

    def reviews(self, issue):
        pc = api.portal.get_tool('portal_catalog')
        parent_path = dict(query='/'.join(issue.getPhysicalPath()),
                           depth=1)
        results = pc(review_state="published",
                     portal_type=("Review Monograph", "Review Journal"),
                     path=parent_path)
        for item in results:
            yield item.getObject()

    def run(self):
        for issue_or_volume in self.issues_and_volumes():
            for review in self.reviews(issue_or_volume):
                if not review.isDoiRegistrationActive():
                    continue
                if api.content.get_state(review) != 'published':
                    continue
                path = '/'.join(review.getPhysicalPath())
                if not review.getEffectiveDate():
                    log.error("No effective date, can not generate XML! " +
                              path)
                    continue
                status, message = register_doi(review)
                print('{0}: {1}, {2}'.format(path, status, message))


metadata_export = MetadataExportScript()
newsletter = NewsletterScript()
sehepunkte_import = SehepunkteImportScript()
register_all_dois = RegisterAllDOIsScript()
