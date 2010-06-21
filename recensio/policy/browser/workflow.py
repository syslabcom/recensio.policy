from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.interface import implements
from plone.registry.interfaces import IRegistry
from plone.app.controlpanel.mail import IMailSchema
from zope.component import queryUtility
import logging

from recensio.policy.interfaces import IWorkflowHelper, IRecensioSettings
from recensio.policy import recensioMessageFactory as _

log = logging.getLogger('Recensio Workflow Helper:')

submit_notification_template = """User %(user)s (%(email)s) has submitted a 
%(portal_type)s for review.

Please check it out a %(link)s.
"""

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
        user_email = user.getProperty('email') or "NO EMAIL"

        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IRecensioSettings)

        if info.transition.id == 'submit':
            title = "Content submitted"
            mail_to = settings.review_submitted_email or mail_from

            msg = submit_notification_template % dict (
                user=user.getUserName(),
                portal_type=info.object.portal_type,
                link=info.object.absolute_url(),
                email=user_email
                )
            try:
                mailhost.send(msg, mail_from, mail_to, title, immediate=True)
            except Exception, err:
                log.warn('Not possible to send email notification for '
                'workflow change on %(url)s. Message:\n%(error)s' % dict(
                    url=info.object.absolute_url(), error=str(err)))

