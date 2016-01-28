from Testing.makerequest import makerequest
from plone import api
from recensio.policy.browser.export import MetadataExport
from recensio.policy.browser.email import MailCollection
from recensio.policy.browser.sehepunkte import Import
from zope.component.hooks import setHooks
from zope.component.hooks import setSite
import Zope2
import logging
import sys
import transaction

log = logging.getLogger()


class ConsoleScript(object):
    def __call__(self, config_file, run_as):
        Zope2.Startup.run.configure(config_file)
        self.app = makerequest(Zope2.app())
        setHooks()
        self.portal = self.app.objectValues('Plone Site')[0]
        setSite(self.portal)

        log.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        log.addHandler(handler)

        with api.env.adopt_user(username=run_as):
            self.run()
        transaction.commit()

    def run(self):
        raise NotImplementedError


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
