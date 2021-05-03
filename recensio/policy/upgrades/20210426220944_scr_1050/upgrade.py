from ftw.upgrade import UpgradeStep
from logging import getLogger
from plone import api

log = getLogger(__name__)


class SCR1050(UpgradeStep):
    """Register new index "hide_from_listing" and reindex objects."""

    def __call__(self):
        self.install_upgrade_profile()

        catalog = api.portal.get_tool("portal_catalog")
        for brain in catalog(portal_type=["Volume"]):
            try:
                obj = brain.getObject()
            except Exception as e:
                log.exception(e)
                continue
            if not obj:
                log.warn("Could not get object {}".format(brain.getPath()))
                continue
            try:
                obj.reindexObject()
            except Exception as e:
                log.exception(e)
                continue
