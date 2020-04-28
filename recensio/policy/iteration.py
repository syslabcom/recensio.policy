from AccessControl import getSecurityManager
from Acquisition import aq_parent, aq_inner
from OFS.Folder import Folder
from plone.app.iterate.policy import CheckinCheckoutPolicyAdapter
from plone.app.iterate import event
from Products.CMFCore import permissions
from zope.event import notify


class CustomCheckingCheckoutPolicyAdapter(CheckinCheckoutPolicyAdapter):
    def cancelCheckout(self):
        baseline = self._getBaseline()
        notify(event.CancelCheckoutEvent(self.context, baseline))
        wc_container = aq_parent(aq_inner(self.context))
        Folder.manage_delObjects(wc_container, [self.context.getId()])
        if getSecurityManager().checkPermission(permissions.View, baseline):
            return baseline
        else:
            return aq_parent(baseline)
