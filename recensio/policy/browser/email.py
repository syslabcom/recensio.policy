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

_ = recensioMessageFactory

class ValidationError(Exception):
    pass

class MailCollection(BrowserView):

    def __call__(self):
        self.errors = []
        try:
            mailhost = getToolByName(self.context, 'MailHost')
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
            registry = getUtility(IRegistry)
            settings = registry.forInterface(INewsletterSettings)
            if not settings.mail_format:
                self.errors.append(_('Mailsettings not configured'))
                raise ValidationError()
            msg = settings.prefix
            for topic in self.context.objectValues():
                if not IATTopic.providedBy(topic):
                    continue
                if IDiscussionCollections.providedBy(topic):
                    tmpl = settings.comment_result_template
                else:
                    tmpl = settings.standard_result_template
                by_type = dict()
                for result in topic.queryCatalog():
                    if result.portal_type in by_type:
                        by_type[result.portal_type].append(result)
                    else:
                        by_type[result.portal_type] = [result]
                for portal_type in by_type.keys():
                    msg += "\nTyp: %(portal_type)s\n%(separator)s" % dict(
                        portal_type=portal_type, separator=settings.separator)
                    for result in by_type[portal_type]:
                        values = dict()
                        for key in result.__record_schema__.keys():
                            if hasattr(getattr(result, key), 'strftime'):
                                try:
                                    values[key] = getattr(result, key).strftime(settings.mail_format)
                                except ValueError:
                                    pass
                            else:
                                values[key] = getattr(result, key)
                        values['getURL'] = result.getURL()
                        msg += tmpl % values
            msg += settings.suffix
            if self.errors:
                raise ValidationError
            mailhost.send(messageText=msg, mto=mail_to, mfrom=mail_from,
                subject=settings.subject, charset='utf-8')
        except ValidationError:
            pass
        except Exception, e:
            self.errors.append(str(e.__class__) + ' ' + str(e))
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

