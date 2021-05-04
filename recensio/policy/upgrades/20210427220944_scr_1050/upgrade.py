from ftw.upgrade import UpgradeStep
from plone import api
from plone.app.portlets.utils import assignment_mapping_from_key
from plone.portlets.constants import CONTEXT_CATEGORY


class Scr1050(UpgradeStep):
    """scr-1050.
    """

    def __call__(self):
        self.install_upgrade_profile()
        portal = api.portal.get()
        obj = portal.get("rezensionen")
        if obj:
            path = "/".join(obj.getPhysicalPath())
            left_portlet_assignment_mapping = assignment_mapping_from_key(
                obj, "plone.leftcolumn", CONTEXT_CATEGORY, path
            )
            for key in ["secondarynavportlets", "secondarynavportlet"]:
                if key in left_portlet_assignment_mapping:
                    del left_portlet_assignment_mapping[key]
