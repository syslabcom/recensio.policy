# -*- coding: utf-8 -*-

import logging

from DateTime import DateTime
from plone.app.controlpanel.mail import IMailSchema
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from recensio.policy import recensioMessageFactory as _
from recensio.policy.interfaces import IRecensioSettings
from recensio.policy.interfaces import IWorkflowHelper
from zope.component import queryUtility
from zope.i18n import translate
from zope.interface import implements

log = logging.getLogger("Recensio Workflow Helper:")

submit_notification_template = """User %(user)s (mailto:%(email)s) has submitted a %(portal_type)s for review.

Please check it out a %(link)s.
"""

# en=u"""Your item "${title}" at ${url} has been approved and is now published.""",


class WorkflowHelper(BrowserView):
    """ Helper for the Recensio workflows
    """

    implements(IWorkflowHelper)

    def handleTransition(self, info):
        membership_tool = getToolByName(self.context, "portal_membership")
        user = membership_tool.getAuthenticatedMember()
        mailhost = getToolByName(self.context, "MailHost")
        root = getToolByName(self.context, "portal_url").getPortalObject()
        mail_info = IMailSchema(root)
        mail_from = "%s <%s>" % (
            mail_info.email_from_name,
            mail_info.email_from_address,
        )
        user_email = user.getProperty("email")

        registry = queryUtility(IRegistry)
        try:
            settings = registry.forInterface(IRecensioSettings)
        except KeyError:
            settings = dict()

        msg = ""

        if info.transition.id == "publish":
            info.object.setEffectiveDate(DateTime())
            info.object.reindexObject()

        if info.transition.id == "submit":
            title = _(u"label_item_submitted", default=u"Content was submitted")
            mail_to = getattr(settings, "review_submitted_email", None) or mail_from
            msg = submit_notification_template % dict(
                user=user.getUserName(),
                portal_type=info.object.portal_type,
                link=info.object.absolute_url(),
                email=user_email,
            )

        elif info.transition.id == "publish" and info.old_state.id == "pending":
            ts = getToolByName(self.context, "translation_service")
            owner = info.object.getOwner()
            mail_to = owner.getProperty("email")
            pref_lang = owner.getProperty("preferred_language", "de")
            title = ts.translate(
                _(u"label_item_published", default=u"Your item has been published"),
                target_language=pref_lang,
            )
            rtool = getToolByName(self.context, "portal_repository")

            info.object.restrictedTraverse("@@mail_new_presentation")()

            publish_notification_template = _(
                "publish_notification_template",
                default=u"""Ihr Artikel "${title}" wurde freigeschaltet und ist nun unter ${url} verfügbar.""",
                mapping=dict(
                    title=info.object.Title().decode("utf-8"),
                    url=info.object.absolute_url(),
                ),
            )
            template = ts.translate(
                publish_notification_template, target_language=pref_lang
            )
            msg = template % dict(
                title=info.object.Title().decode("utf-8"),
                url=info.object.absolute_url(),
            )

        if msg:
            subject = translate(title)
            try:
                log.info(u"I am sending the following msg:\n%s" % msg)
                mailhost.send(
                    messageText=msg,
                    mto=mail_to,
                    mfrom=mail_from,
                    subject=subject,
                    charset="utf-8",
                    immediate=True,
                )
            except Exception, err:
                log.warn(
                    "Not possible to send email notification for "
                    "workflow change on %(url)s. Message:\n%(error)s"
                    % dict(url=info.object.absolute_url(), error=str(err))
                )
