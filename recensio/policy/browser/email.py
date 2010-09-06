# -*- coding: utf-8 -*-

import logging
from plone.app.controlpanel.mail import IMailSchema
from Products.ATContentTypes.interfaces import IATTopic
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from plone.app.registry.browser import controlpanel
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

from recensio.policy import recensioMessageFactory
from recensio.policy.interfaces import INewsletterSettings, IDiscussionCollections

log = logging.getLogger()

_ = recensioMessageFactory

class ValidationError(Exception):
    pass

class MailCollection(BrowserView):

    def __init__(self, request, context):
        super(BrowserView, self).__init__(request, context)
        self.mailhost = getToolByName(self.context, 'MailHost')

    def getNewReviews(self):
        magazines = {}
        import pdb;pdb.set_trace()
        for result in self.context.new_reviews.queryCatalog():
            obj = result.getObject()
            mag_title = obj.get_publication_title()
            if not magazines.has_key(mag_title):
                magazines[mag_title] = []
            magazines[mag_title].append(obj)
        retval = ''
        mag_keys = magazines.keys()
        mag_keys.sort()
        for mag_title in mag_keys:
            mag_results = magazines[mag_title]
            retval += mag_title
            for i, result in enumerate(mag_results):
                if i < 3:
                    msg = u'\n\n    %s (%s)\n\n    %s' % (result.Title(), \
                                             result.absolute_url(),\
                                             '-' * 40)
                    retval += msg
                if i == 3:
                    msg = u'\n\n    Weitere Ergebnisse finden Sie hier:\n    %s\n\n' % \
                        self.context.new_reviews.absolute_url()
                    retval += msg
                    break
        return retval

    def getComments(self):
        pass

    def getNewPresentations(self):
        presentations = {u'Präsentationen von Monographien' : [],
                         u'Präsentationen von Aufsätzen' : [],
                         u'Präsentationen von Internetressourcen' : []}

        formatted_result = lambda x: u'\n\n        %s (%s)\n\n        %s' % \
            (x.Title, x.getURL(), '-' * 36)

        for result in self.context.new_presentations.queryCatalog():
            if result.portal_type == 'Presentation Article Review':
                presentations[u'Präsentationen von Aufsätzen']\
                    .append(formatted_result(result))
            elif result.portal_type == 'Presentation Collection':
                presentations[u'Präsentationen von Aufsätzen']\
                    .append(formatted_result(result))
            elif result.portal_type == 'Presentation Monograph':
                presentations[u'Präsentationen von Monographien']\
                    .append(formatted_result(result))
            elif result.portal_type == 'Presentation Online Resource':
                presentations[u'Präsentationen von Internetressourcen']\
                    .append(formatted_result(result))
            else:
                assert False, "Unknown new content type, fix me"
        presentation_keys = presentations.keys()
        presentation_keys.sort()
        for key in presentation_keys:
            if len(presentations[key]) > 3:
                presentations[key][3] = u'\n\n        Weitere Ergebnisse finden Sie hier:\n        %s\n' % self.context.new_presentations.absolute_url()
                presentations[key] = presentations[key][:4]
        retval = ''
        for key in presentations.keys():
            retval += u'\n    ' + key
            for result in presentations[key]:
                retval += result
        return retval

    def getMailAddresses(self):
        root = getToolByName(self.context, 'portal_url').getPortalObject()
        membership_tool = getToolByName(self.context, 'portal_membership')
        if membership_tool.isAnonymousUser():
            self.errors.append(_('You are not logged in'))
            raise ValidationError()
        user = membership_tool.getAuthenticatedMember()
        mail_info = IMailSchema(root)
        mail_from = '%s <%s>' % (mail_info.email_from_name, mail_info.email_from_address)
        if not mail_info.email_from_address:
            self.errors.append(_('Plone site is not configured'))
            raise ValidationError()
        mail_to = user.getProperty('email')
        if not mail_to:
            self.errors.append(_("You did not provide an e-mail address in your profile"))
            raise ValidationError()
        return mail_from, mail_to


    def __call__(self):
        self.errors = []
        try:
            mail_from, mail_to = self.getMailAddresses()
            registry = getUtility(IRegistry)
            settings = registry.forInterface(INewsletterSettings)
            if not settings.mail_format:
                self.errors.append(_('Mailsettings not configured'))
                raise ValidationError()

            sections = {}
            sections['new_reviews'] = self.getNewReviews()
            sections['new_presentations'] = self.getNewPresentations()
            sections['new_discussions'] = self.getComments()
            msg = settings.mail_template % sections

            if self.errors:
                raise ValidationError
            else:
                self.mailhost.send(messageText=msg, mto=mail_to,
                                   mfrom=mail_from,
                                   subject=settings.subject, charset='utf-8')
        except ValidationError:
            pass
#        except Exception, e:
#            log.exception(e)
#            self.errors.append(str(e.__class__) + ' ' + str(e))
        finally:
            messages = IStatusMessage(self.request)
            if self.errors:
                for error in self.errors:
                    messages.addStatusMessage(error, type='error')
            else:
                messages.addStatusMessage(u"Mail sending will be prepared. Mail will be sent to %s" % mail_to, type="info")
        return self.request.response.redirect(self.context.absolute_url())

class NewsletterSettingsEditForm(controlpanel.RegistryEditForm):

    schema = INewsletterSettings
    label = _('Newsletter settings')
    description = _('This is a technical configuration panel for newsletter settings.\nThe templates can access any object of a catalog result, but dates have been preformatted.')

class NewsletterSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = NewsletterSettingsEditForm

