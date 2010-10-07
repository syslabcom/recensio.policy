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
from Acquisition import aq_parent

log = logging.getLogger()

_ = recensioMessageFactory

class ValidationError(Exception):
    pass

class MailCollection(BrowserView):

    def __init__(self, request, context):
        super(BrowserView, self).__init__(request, context)
        self.mailhost = getToolByName(self.context, 'MailHost')
        self.ts = getToolByName(self.context, 'translation_service')

    def getNewReviews(self):
        magazines = {}
        for result in self.context.new_reviews.queryCatalog():
            obj = result.getObject()
            mag_title = obj.get_publication_title().decode('utf-8')
            if not magazines.has_key(mag_title):
                magazines[mag_title] = []
            magazines[mag_title].append(obj)
        retval = u''
        mag_keys = magazines.keys()
        mag_keys.sort()
        for mag_title in mag_keys:
            mag_results = magazines[mag_title]
            retval += mag_title
            for i, result in enumerate(mag_results):
                if i < 3:
                    msg = '\n\n    %s (%s)\n\n    %s\n\n' % (result.Title(), \
                                             result.absolute_url(),\
                                             '-' * 40)
                    retval += msg
                if i == 3:
                    msg = "    " + self.ts.translate(_('more_results_here'), context=self.context) % \
                        self.context.new_reviews.absolute_url() + "\n\n"
                    retval += msg
                    break
        return retval

    def getComments(self):
        retval = ''
        for result in self.context.new_discussions.queryCatalog():
            retval += '\n%s (%s %s)\n(%s)\n' % (result.Title, \
                result.total_comments, \
                result.total_comments != '1' and self.ts.translate(_('comments'), context=self.context) or self.ts.translate(_('comment'), context=self.context), \
                result.getURL())
        return retval

    def getNewPresentations(self):
        key_monographs = self.ts.translate(_('presentations_of_monographs'), context=self.context)
        key_articles = self.ts.translate(_('presentations_of_articles'), context=self.context)
        key_onlineres = self.ts.translate(_('presentations_of_online_resources'), context=self.context)
        
        presentations = {key_monographs : [],
                         key_articles : [],
                         key_onlineres : []}

        formatted_result = lambda x: u'\n\n        %s (%s)\n\n        %s' % \
            (x.Title, x.getURL(), '-' * 36)

        for result in self.context.new_presentations.queryCatalog():
            if result.portal_type == 'Presentation Article Review':
                presentations[key_articles]\
                    .append(formatted_result(result))
            elif result.portal_type == 'Presentation Collection':
                presentations[key_articles]\
                    .append(formatted_result(result))
            elif result.portal_type == 'Presentation Monograph':
                presentations[key_monographs]\
                    .append(formatted_result(result))
            elif result.portal_type == 'Presentation Online Resource':
                presentations[key_onlineres]\
                    .append(formatted_result(result))
            else:
                assert False, "Unknown new content type, fix me"
        presentation_keys = presentations.keys()
        presentation_keys.sort()
        for key in presentation_keys:
            if len(presentations[key]) > 3:
                presentations[key][3] = "\n\n    " + self.ts.translate(_('more_results_here'), context=self.context) % self.context.new_presentations.absolute_url() + "\n\n"
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
                messages.addStatusMessage(self.ts.translate(_('mail_sending_prepared'), context=self.context) % mail_to, type="info")
        return self.request.response.redirect(self.context.absolute_url())

class MailNewComment(BrowserView):
    def __init__(self, request, context):
        super(BrowserView, self).__init__(request, context)
        self.mailhost = getToolByName(self.context, 'MailHost')
        self.ts = getToolByName(self.context, 'translation_service')

    def __call__(self):
        root = getToolByName(self.context, 'portal_url').getPortalObject()
        mail_info = IMailSchema(root)
        mail_from = '%s <%s>' % (mail_info.email_from_name, mail_info.email_from_address)

        comment = self.context
        conversation = aq_parent(comment)
        review = aq_parent(conversation)

        authors = getattr(review, 'authors', [{'firstname' : '',\
                                               'lastname' : 'unknown'}])
        args = {}
        args['url'] = review.absolute_url()
        args['author'] = u' '.join([x.decode('utf-8') for x in [review.reviewAuthorFirstname, review.reviewAuthorLastname]])
        args['date'] = review.created().strftime('%d.%m.%Y')
        args['title'] = review.Title()
        args['commenter'] = comment.author_name
        args['commentdate'] = comment.creation_date.strftime('%d.%m.%Y')
        args['mail_from'] = mail_from

        subject = self.ts.translate(_('mail_new_comment_subject'), context=self.context)
        mail_to = self.findRecipient()
        msg_template = self.ts.translate(_('mail_new_comment_body'), context=self.context)
        self.sendMail(msg_template % args, mail_from, mail_to, subject)

    def sendMail(self, msg, mail_from, mail_to, subject):
        if mail_to:
            self.mailhost.send(messageText=msg, mto=mail_to,
                               mfrom=mail_from,
                               subject=subject, charset='utf-8')
        else:
            messages = IStatusMessage(self.request)
            messages.addStatusMessage(self.ts.translate(_('mail_no_recipients'), context=self.context), type="warning")

    def findRecipient(self):
        membership_tool = getToolByName(self.context, 'portal_membership')
        owner = membership_tool.getMemberById(self.context.__parent__.__parent__.Creator()).getUser()
        return owner.getProperty('email')


class MailNewPublication(BrowserView):
    def __init__(self, request, context):
        super(BrowserView, self).__init__(request, context)
        self.mailhost = getToolByName(self.context, 'MailHost')

    def __call__(self):
        root = getToolByName(self.context, 'portal_url').getPortalObject()
        ts = getToolByName(self.context, 'translation_service')
        mail_info = IMailSchema(root)
        mail_from = '%s <%s>' % (mail_info.email_from_name, mail_info.email_from_address)
        authors = list(getattr(self.context, 'authors', [{'firstname' : '',\
                                                     'lastname' : 'unknown'}]))
        referenceAuthors = getattr(self.context, 'referenceAuthors', [])
        authors.extend(referenceAuthors)

        for author in authors:
            args = {}
            fuckup = [author['firstname'], author['lastname']]
            fuckup = [x.decode('utf-8') for x in fuckup]
            args['reviewed_author'] = u' '.join(fuckup)
            if author.has_key('email'):
                args['mail_to'] = author['email']
            else:
                args['mail_to'] = ts.translate(_('no_mail_address_available'), context=self.context)
            args['title'] = self.context.title.decode('utf-8')
            args['subtitle'] = getattr(self.context, 'subtitle', '').decode('utf-8')
            args['review_author'] = u' '.join([x.decode('utf-8') for x in [self.context.reviewAuthorFirstname, self.context.reviewAuthorLastname]])
            args['mail_from'] = mail_from.decode('utf-8')
            args['concept_url'] = root.konzept.absolute_url()
            subject = ts.translate(_('mail_new_publication_subject'), context=self.context) % args['title']
            msg_template = ts.translate(_('mail_new_publication_body'), context=self.context)
            self.sendMail(msg_template % args, mail_from, subject)

    def sendMail(self, msg, mail_from, subject):
        self.mailhost.send(messageText=msg, mto=mail_from,
                           mfrom=mail_from,
                           subject=subject, charset='utf-8')

class MailUncommented(BrowserView):
    def __init__(self, request, context):
        super(BrowserView, self).__init__(request, context)
        self.mailhost = getToolByName(self.context, 'MailHost')
        self.ts = getToolByName(self.context, 'translation_service')


    def __call__(self):
        count = 0
        for result in self.context.discussion_three_months_old.queryCatalog():
            if result.total_comments == '0':
                count += 1
                self.sendMail(result)
        return "Sent %i mails" % count

    def sendMail(self, result):
        msg = self.formatMessage(result)
        mail_to = self.findRecipient(result)
        mail_from = self.findSender()
        subject = self.ts.translate(_('mail_uncommented_subject'), context=self.context)
        self.mailhost.send(messageText=msg, mto=mail_to,
                           mfrom=mail_from,
                           subject=subject, charset='utf-8')

    def formatMessage(self, result):
        title = result.Title
        owner_name = result.Creator
        url = result.getURL()
        date = result.created.strftime('%d.%m.%Y')
        msg_template = self.ts.translate(_('mail_uncommented_body'), context=self.context)

        return msg_template % {'name' : owner_name,
                                    'url' : url,
                                    'title' : title,
                                    'date' : date,
                                    'mail_from' : self.findSender() }

    def findRecipient(self, result):
        membership_tool = getToolByName(self.context, 'portal_membership')
        owner = membership_tool.getMemberById(result.Creator).getUser()
        return owner.getProperty('email')

    def findSender(self):
        root = getToolByName(self.context, 'portal_url').getPortalObject()
        membership_tool = getToolByName(self.context, 'portal_membership')
        mail_info = IMailSchema(root)
        mail_from = '%s <%s>' % (mail_info.email_from_name, mail_info.email_from_address)
        return mail_from

class NewsletterSettingsEditForm(controlpanel.RegistryEditForm):

    schema = INewsletterSettings
    label = _('Newsletter settings')
    description = _('This is a technical configuration panel for newsletter settings.\nThe templates can access any object of a catalog result, but dates have been preformatted.')

class NewsletterSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = NewsletterSettingsEditForm

