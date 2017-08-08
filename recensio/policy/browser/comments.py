from urllib import quote_plus

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel.mail import IMailSchema

from plone.app.discussion.browser.comments import CommentsViewlet as BaseCommentsViewlet

class CommentsViewlet(BaseCommentsViewlet):
    index = ViewPageTemplateFile('templates/comments.pt')

    @property
    def getMailTarget(self):
        if not hasattr(self, '_mailTarget'):
            root = getToolByName(self.context, 'portal_url').getPortalObject()
            schema = IMailSchema(root)
            self._mailTarget = '%s <%s>' % (schema.email_from_name, schema.email_from_address)
        return self._mailTarget

    @property
    def title(self):
        if not hasattr(self, '_mailTitle'):
            self._mailTitle = 'NOTIFICATION: possible problematic comment at %s#' % self.context.absolute_url()
        return self._mailTitle

    @property
    def escaped_title(self):
        return quote_plus(self.title)

    @property
    def portal_title(self):
        return getToolByName(self.context, 'portal_url').getPortalObject().Title()
