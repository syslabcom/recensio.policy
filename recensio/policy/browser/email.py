from plone.app.controlpanel.mail import IMailSchema
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from plone.app.registry.browser import controlpanel
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

from recensio.policy import recensioMessageFactory
from recensio.policy.interfaces import INewsletterSettings

_ = recensioMessageFactory

result_template = """%(Title)s

%(Description)s

Created on: %(created)s
-------------------------------------------------------------------------------

"""
result_discussions_template = """%(Title)s

%(Description)s

Last discussed on: %(last_comment_date)s
-------------------------------------------------------------------------------

"""

class MailCollection(BrowserView):

    def __call__(self):
        self.errors = []
        mailhost = getToolByName(self.context, 'MailHost')
        root = getToolByName(self.context, 'portal_url').getPortalObject()
        membership_tool = getToolByName(self.context, 'portal_membership')
        if membership_tool.isAnonymousUser():
            self.errors.append(_('You are not logged in'))
        user = membership_tool.getAuthenticatedMember()
        mail_info = IMailSchema(root)
        mail_from = '%s <%s>' % (mail_info.email_from_name, mail_info.email_from_address)
        if not mail_info.email_from_address:
            self.errors.append(_('Plone site is not configured'))
        mail_to = user.getProperty('email') or 'do3ccqrv@googlemail.com'
        if not mail_to:
            self.errors.append(_("You did not provide an e-mail address in your profile"))
        self.mail_to = mail_to
        registry = getUtility(IRegistry)
        settings = registry.forInterface(INewsletterSettings)

        import pdb;pdb.set_trace()
        msg = ""
        for result in self.context.queryCatalog():
            msg += self.tmpl % {'Title' : result.Title,
                                'Description' : result.Description,
                                'created' : result.created.strftime('%d.%m.%Y'),
                                'last_comment_date' : result.last_comment_date and result.last_comment_date.strftime('%d.%m.%Y')}
        if not self.errors:
            mailhost.send(messageText=msg, mto=mail_to, mfrom=mail_from,
                subject=self.context.Title())
        return super(MailCollection, self).__call__()

class NewsletterSettingsEditForm(controlpanel.RegistryEditForm):

    schema = INewsletterSettings
    label = _('Newsletter settings')
    description = _('This is a technical configuration panel for newsletter settings.\nThe templates can access any object of a catalog result, but dates have been preformatted.')

class NewsletterSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = NewsletterSettingsEditForm
