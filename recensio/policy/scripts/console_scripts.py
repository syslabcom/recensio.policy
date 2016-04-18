from plone import api
from recensio.policy.browser.export import MetadataExport
from recensio.policy.browser.email import MailCollection
from recensio.policy.browser.sehepunkte import Import
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


metadata_export = MetadataExportScript()
newsletter = NewsletterScript()
sehepunkte_import = SehepunkteImportScript()
