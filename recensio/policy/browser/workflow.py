# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.interface import implements
from plone.registry.interfaces import IRegistry
from plone.app.controlpanel.mail import IMailSchema
from zope.component import queryUtility
from zope.i18n import translate
import logging

from recensio.policy.interfaces import IWorkflowHelper, IRecensioSettings
from recensio.policy import recensioMessageFactory as _

log = logging.getLogger('Recensio Workflow Helper:')

submit_notification_template = """User %(user)s (mailto:%(email)s) has submitted a %(portal_type)s for review.

Please check it out a %(link)s.
"""

publish_notification_template = dict(
en=u"""Your item "%(title)s" at %(url)s has been approved and is now published.""",
de=u"""Ihr Artikel "%(title)s" wurde freigeschaltet und ist nun unter %(url)s verfügbar.""",
fr=u"""Ihr Artikel "%(title)s" wurde freigeschaltet und ist nun unter %(url)s verfügbar."""
)

class WorkflowHelper(BrowserView):
    """ Helper for the Recensio workflows
    """
    implements(IWorkflowHelper)

    
    def handleTransition(self, info):
        membership_tool = getToolByName(self.context, 'portal_membership')
        user = membership_tool.getAuthenticatedMember()
        mailhost = getToolByName(self.context, 'MailHost')
        root = getToolByName(self.context, 'portal_url').getPortalObject()
        mail_info = IMailSchema(root)
        mail_from = '%s <%s>' % (mail_info.email_from_name, mail_info.email_from_address)
        user_email = user.getProperty('email')

        registry = queryUtility(IRegistry)
        try:
            settings = registry.forInterface(IRecensioSettings)
        except KeyError:
            settings = dict()
        
        msg = ''
        if info.transition.id == 'submit':
            title = _(u"label_item_submitted", default=u"Content was submitted")
            mail_to = getattr(settings, 'review_submitted_email', None) or mail_from
            msg = submit_notification_template % dict (
                user=user.getUserName(),
                portal_type=info.object.portal_type,
                link=info.object.absolute_url(),
                email=user_email
                )

        elif info.transition.id == 'publish' and info.old_state.id == 'pending':
            owner = info.object.getOwner()
            mail_to = owner.getProperty('email')
            pref_lang = owner.getProperty('preferred_language', 'de')
            title = _(u'label_item_published', default=u'Your item has been published')
            info.object.restrictedTraverse('@@mail_new_presentation')()
            template = publish_notification_template.get(pref_lang, None) or \
                publish_notification_template.get('de')
            msg = template % dict(title=info.object.Title().decode('utf-8'),
                url=info.object.absolute_url())

        if msg:
            subject = translate(title)
            try:
                log.info(u'I am sending the following msg:\n%s' % msg)
                mailhost.send(messageText=msg, mto=mail_to, mfrom=mail_from,
                    subject=subject, charset='utf-8', immediate=True)
            except Exception, err:
                log.warn('Not possible to send email notification for '
                'workflow change on %(url)s. Message:\n%(error)s' % dict(
                    url=info.object.absolute_url(), error=str(err)))


