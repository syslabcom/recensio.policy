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
from DateTime import DateTime

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
            retval += mag_title + '\n' + '-' * len(mag_title)
            for i, result in enumerate(mag_results):
                if i < 3:
                    msg = '\n%s\n%s\n(%s)\n\n' % (result.Title(), \
                                             '~' * len(result.Title()),
                                             result.absolute_url())
                    retval += msg
                if i == 3:
                    msg = '\n' + self.ts.translate(_('more_results_here'), context=self.context) + '\n' +\
                        self.context.new_reviews.absolute_url() + '\n\n\n'
                    retval += msg
                    break
        return retval

    def getComments(self):
        retval = ''
        for result in self.context.new_discussions.queryCatalog():
            line = '%s (%s %s)\n' % (result.Title, \
                result.total_comments, \
                result.total_comments != '1' and self.ts.translate(_('comments'), context=self.context) \
                    or self.ts.translate(_('comment')))
            line += '~' * len(line)
            retval += '%s\n(%s)\n\n' % (line, result.getURL())
        return retval

    def getNewPresentations(self):
        key_monographs = self.ts.translate(_('presentations_of_monographs'), context=self.context)
        key_articles = self.ts.translate(_('presentations_of_articles'), context=self.context)
        key_onlineres = self.ts.translate(_('presentations_of_online_resources'), context=self.context)
        
        presentations = {key_monographs : [],
                         key_articles : [],
                         key_onlineres : []}

        formatted_result = lambda x: u'\n%s\n%s\n(%s)\n\n' % \
            (x.Title, '~' * len(x.Title), x.getURL())

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
                presentations[key][3] = "\n" + self.ts.translate(_('more_results_here'), context=self.context) + '\n' + self.context.new_presentations.absolute_url() + "\n\n\n"
                presentations[key] = presentations[key][:4]
        retval = ''
        for key in presentations.keys():
            retval += u'' + key + '\n' + '-' * len(key)
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
        messages = IStatusMessage(self.request)
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

            # Copy mail to archive folder
            try:
                arch = self.context.unrestrictedTraverse(settings.archive_folder)
            except (AttributeError, KeyError):
                # try to create archive folder
                folder = getToolByName(self.context, 'portal_url').getPortalObject()
                for sub in settings.archive_folder.split('/')[2:]:
                    if sub in folder.objectIds():
                        folder = folder[sub]
                    else:
                        type = getattr(folder, 'meta_type', None)
                        if not (type == 'ATFolder' or type == 'Plone Site'):
                            messages.addStatusMessage('Unable to create archive folder %s: %s is not a folder!' % (settings.archive_folder, folder.getId()), type='error')
                            break
                        else:
                            id = folder.invokeFactory('Folder', sub)
                            folder = folder[id]
                            folder.setTitle(sub)
                arch = folder
                messages.addStatusMessage('Created Newsletter archive folder %s' % (settings.archive_folder), type='info')

            if not getattr(arch, 'meta_type', None) == 'ATFolder':
                messages.addStatusMessage('Unable to use %s as archive folder: Not a folder!' % (settings.archive_folder), type='error')
                raise ValidationError

            if not arch.getPhysicalPath() == tuple(settings.archive_folder.split('/')):
                raise ValidationError
                
            name = 'Newsletter %s' % DateTime().strftime('%d.%m.%Y')
            if name in arch.objectIds():
                messages.addStatusMessage('%s already exists in archive' % name, type='warning')
            else:
                id = arch.invokeFactory('Document', name)
                new_ob = arch[id]
                new_ob.setTitle(name)
                new_ob.setText(msg)
                new_ob.setContentType('text/restructured')
                messages.addStatusMessage('Mail archived as %s' % '/'.join(new_ob.getPhysicalPath()), type='info')

        except ValidationError:
            pass
#        except Exception, e:
#            log.exception(e)
#            self.errors.append(str(e.__class__) + ' ' + str(e))
        finally:
            if self.errors:
                for error in self.errors:
                    messages.addStatusMessage(error, type='error')
            else:
                messages.addStatusMessage(self.ts.translate(_('mail_sending_prepared', default="uMailversand wird vorbereitet. Mail wird versandt an %s"), context=self.context) % mail_to, type="info")
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

        mail_to, pref_lang = self.findRecipient()
        subject = self.ts.translate(_('mail_new_comment_subject'), target_language=pref_lang)
        msg_template = self.ts.translate(_('mail_new_comment_body'), target_language=pref_lang)
        self.sendMail(msg_template % args, mail_from, mail_to, subject)

    def sendMail(self, msg, mail_from, mail_to, subject):
        if mail_to:
            self.mailhost.send(messageText=msg, mto=mail_to,
                               mfrom=mail_from,
                               subject=subject, charset='utf-8')
        else:
            messages = IStatusMessage(self.request)
            messages.addStatusMessage(self.ts.translate(_('mail_no_recipients'), target_language=pref_lang), type="warning")

    def findRecipient(self):
        membership_tool = getToolByName(self.context, 'portal_membership')
        owner = membership_tool.getMemberById(self.context.__parent__.__parent__.Creator()).getUser()
        return owner.getProperty('email'), owner.getProperty('preferred_language', 'en')


class MailNewPublication(BrowserView):
    def __init__(self, request, context):
        super(BrowserView, self).__init__(request, context)
        self.mailhost = getToolByName(self.context, 'MailHost')
        self.ts = getToolByName(self.context, 'translation_service')
        self.pas = getToolByName(self.context, "acl_users")
        self.membership_tool = getToolByName(self.context, 'portal_membership')

    def __call__(self):
        root = getToolByName(self.context, 'portal_url').getPortalObject()
        mail_info = IMailSchema(root)
        mail_from = '%s <%s>' % (mail_info.email_from_name, mail_info.email_from_address)
        referenceAuthors = getattr(self.context, 'referenceAuthors', [])

        def get_preferred_language(email, default='en'):
            found = self.pas.searchUsers(email=args['mail_to'])
            if found:
                owner = self.membership_tool.getMemberById(found[0]['userid']).getUser()
                return owner.getProperty('preferred_language', default)
            else:
                return default

        for author in referenceAuthors:
            args = {}
            fuckup = [author['firstname'], author['lastname']]
            fuckup = [x.decode('utf-8') for x in fuckup]
            args['reviewed_author'] = u' '.join(fuckup)
            args['mail_from'] = mail_from.decode('utf-8')
            pref_lang = 'en'
            if author.has_key('email') and author['email']:
                args['mail_to'] = author['email']
                pref_lang = get_preferred_language(author['email'], pref_lang)
                msg_template = self.ts.translate(_('mail_new_publication_body'), target_language=pref_lang)
            else:
                args['mail_to'] = args['mail_from']
                pref_lang = get_preferred_language(args['mail_from'], pref_lang)
                msg_template = self.ts.translate(_('mail_new_publication_intro'), target_language=pref_lang) + self.ts.translate(_('mail_new_publication_body'), target_language=pref_lang)
            args['title'] = self.context.title.decode('utf-8')
            args['subtitle'] = getattr(self.context, 'subtitle', '').decode('utf-8')
            args['review_author'] = u' '.join([x.decode('utf-8') for x in [self.context.reviewAuthorFirstname, self.context.reviewAuthorLastname]])
            args['concept_url'] = root.absolute_url() + '/ueberuns/konzept'
            args['context_url'] = self.context.absolute_url()
            subject = self.ts.translate(_('mail_new_publication_subject', default=u"Es wurde eine Rezension von %s veröffentlicht"), target_language=pref_lang) % args['title']
            self.sendMail(msg_template % args, args['mail_to'], mail_from, subject)

    def sendMail(self, msg, mail_to, mail_from, subject):
        self.mailhost.send(messageText=msg, mto=mail_to,
                           mfrom=mail_from,
                           subject=subject, charset='utf-8')

class MailUncommented(BrowserView):
    def __init__(self, request, context):
        super(BrowserView, self).__init__(request, context)
        self.mailhost = getToolByName(self.context, 'MailHost')
        self.mail_body = u"""Sehr geehrte/r Frau/Herr %(name)s,

Sie haben am %(date)s Ihre Schrift
    %(title)s
    
    auf recensio.net präsentiert. Bisher liegen keine Kommentare vor. Sie 
haben hier die Gelegenheit, Ihre Präsentation zu modifizieren: Sie könnten 
die Thesenformulierung bearbeiten oder auch die Zahl der aufgeführten 
Bezugsautoren erweitern. In der Regel werden diese von der recensio.net-
Redaktion kontaktiert, was erheblich zur Sichtbarkeit einer Präsentation 
beiträgt. Wenn noch nicht geschehen, haben Sie zusätzlich die Möglichkeit, 
Coverbilder und Inhaltsverzeichnisse beizufügen (im Fall von Präsentationen 
von Monographien).
    
    Für Rückfragen steht Ihnen die recensio.net-Redaktion gern zur 
Verfügung: %(mail_from)s.
    
    Mit freundlichen Grüßen,
    Ihr recensio.net-Team"""

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
        mail_to, pref_lang = self.findRecipient(result)
        mail_from = self.findSender()
        subject = self.ts.translate(_('mail_uncommented_subject', default=u"Ihre Rezension auf recensio.net"), target_language=pref_lang)
        self.mailhost.send(messageText=msg, mto=mail_to,
                           mfrom=mail_from,
                           subject=subject, charset='utf-8')

    def formatMessage(self, result):
        title = result.Title
        owner_name = result.Creator
        mail, pref_lang = self.findRecipient(result)
        url = result.getURL()
        date = result.created.strftime('%d.%m.%Y')
        msg_template = self.ts.translate(_('mail_uncommented_body', default=self.mail_body), target_language=pref_lang)

        return msg_template % {'name' : owner_name,
                                    'url' : url,
                                    'title' : title,
                                    'date' : date,
                                    'mail_from' : self.findSender() }

    def findRecipient(self, result):
        membership_tool = getToolByName(self.context, 'portal_membership')
        owner = membership_tool.getMemberById(result.Creator).getUser()
        return owner.getProperty('email') or self.findSender(), owner.getProperty('preferred_language', 'en')

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

