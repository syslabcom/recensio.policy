from plone.app.controlpanel.mail import IMailSchema
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

from recensio.policy.interfaces import IDiscussionCollections
from recensio.policy import recensioMessageFactory

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
    tmpl = result_template
    def __init__(self, context, request):
        if IDiscussionCollections.providedBy(context):
            self.tmpl = result_discussions_template
        else:
            self.tmpl = result_template
        super(MailCollection, self).__init__(context, request)

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
        msg = ""
        for result in self.context.queryCatalog():
            msg += self.tmpl % {'Title' : result.Title,
                                'Description' : result.Description,
                                'created' : result.created.strftime('%d.%m.%Y'),
                                'last_comment_date' : result.last_comment_date and result.last_comment_date.strftime('%d.%m.%Y')}
        if not self.errors:
            mailhost.send(msg, mail_from, mail_to, self.context.Title())
        return super(MailCollection, self).__call__()
