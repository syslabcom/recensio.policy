# -*- coding: utf-8 -*-

import logging
from plone.app.controlpanel.mail import IMailSchema
from Products.CMFPlone.utils import safe_unicode
from Products.ATContentTypes.interfaces import IATTopic
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from plone.app.registry.browser import controlpanel
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from DateTime import DateTime

from recensio.policy import recensioMessageFactory
from recensio.policy.interfaces import INewsletterSettings, \
    IDiscussionCollections
from recensio.contenttypes.content.review import get_formatted_names
from recensio.contenttypes.interfaces import IParentGetter
from Acquisition import aq_parent

logger = logging.getLogger("recensio.policy.browser.email")

_ = recensioMessageFactory

REVIEW_TYPES = ["Review Monograph", "Review Journal"]

class ValidationError(Exception):
    pass

class MailCollection(BrowserView):

    def __init__(self, request, context):
        super(BrowserView, self).__init__(request, context)
        self.mailhost = getToolByName(self.context, 'MailHost')
        self.ts = getToolByName(self.context, 'translation_service')
        self.root = getToolByName(self.context, 'portal_url').getPortalObject()

    def getNewReviews(self):
        magazines = {}
        for result in self.context.new_reviews.queryCatalog():
            obj = result.getObject()
            mag_title = safe_unicode(obj.get_publication_title())
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
                if i < 9999:
                    title = result.getDecoratedTitle()
                    msg = u'\n%s\n(%s)\n\n' % (title, \
                                             result.absolute_url())
                    retval += msg
                if i == 9999:
                    msg = ('\n'+ self.ts.translate(_('more_results_here'),
                                                   context=self.context) +
                           '\n' + self.context.new_reviews.absolute_url() +
                           '\n\n\n')
                    retval += msg
                    break
        return retval

    def getNewReviewSections(self):
        retval = ''
        for result in self.context.new_issues.queryCatalog():
            volume = result.getObject().getParentNode()
            publication = volume.getParentNode()
            retval += u'%s: %s, %s\n' % (
                safe_unicode(publication.Title()), safe_unicode(volume.Title()),
                safe_unicode(result.Title))
        return retval

    def getComments(self):
        retval = ''
        for result in self.context.new_discussions.queryCatalog():
            label_comments = result.total_comments == 1 \
                and self.ts.translate(_('comment')) \
                or  self.ts.translate(_('comments'), context=self.context)
            line = '%s (%s %s)\n' % (
                result.getObject().getDecoratedTitle(), result.total_comments,
                label_comments)
            line += '\n'
            retval += '%s\n(%s)\n\n' % (line, result.getURL())
        return retval

    def getNewPresentations(self):
        key_monographs = self.ts.translate(
            _('presentations_of_monographs'),
            context=self.context)
        key_articles = self.ts.translate(
            _('presentations_of_articles'),
            context=self.context)
        key_onlineres = self.ts.translate(
            _('presentations_of_online_resources'),
            context=self.context)

        presentations = {key_monographs : [],
                         key_articles : [],
                         key_onlineres : []}

        formatted_result = lambda x: u'\n%s\n%s\n(%s)\n\n' % \
            (x.getObject().getDecoratedTitle(), '\n', x.getURL())

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
                assert False, "Unknown new content type '%s', fix me" % (
                    result.portal_type)
        presentation_keys = presentations.keys()
        presentation_keys.sort()
        for key in presentation_keys:
            if len(presentations[key]) > 9999:
                presentations[key][9999] = (
                    "\n" + self.ts.translate(_('more_results_here'),
                                             context=self.context) +
                    '\n' + self.context.new_presentations.absolute_url() +
                    "\n\n\n")
                presentations[key] = presentations[key][:10000]
        retval = ''
        for key in presentations.keys():
            retval += u'' + key + '\n' + '-' * len(key) + u'\n'
            for result in presentations[key]:
                retval += result
        return retval

    def getMailAddresses(self):
        mail_info = IMailSchema(self.root)
        mail_from = '%s <%s>' % (
            mail_info.email_from_name, mail_info.email_from_address)
        mail_to = '%s <%s>' % (
            mail_info.email_from_name, mail_info.email_from_address)
        if not mail_info.email_from_address:
            self.errors.append(_('Plone site is not configured'))
            raise ValidationError()
        return mail_from, mail_to

    def getNewsletterSettings(self):
        return getUtility(IRegistry).forInterface(INewsletterSettings)

    def __call__(self):
        self.errors = []
        messages = IStatusMessage(self.request)
        mail_to = mail_from = ""
        try:
            mail_from, mail_to = self.getMailAddresses()
            settings = self.getNewsletterSettings()
            if not settings.mail_format:
                msg = _('Mailsettings not configured')
                self.errors.append(msg)
                raise ValidationError(msg)

            sections = {}
            sections['new_review_sections'] = self.getNewReviewSections()
            sections['new_reviews'] = self.getNewReviews()
            sections['new_presentations'] = self.getNewPresentations()
            sections['new_discussions'] = self.getComments()
            msg = settings.mail_template % sections

            if self.errors:
                raise ValidationError("Errors: %s" %self.errors)
            else:
                self.mailhost.send(
                    messageText=msg, mto=mail_to, mfrom=mail_from,
                    subject=settings.subject, charset='utf-8')

            # Copy mail to archive folder
            try:
                arch = self.context.unrestrictedTraverse(
                    settings.archive_folder)
            except (AttributeError, KeyError):
                # try to create archive folder
                folder = getToolByName(
                    self.context, 'portal_url').getPortalObject()
                for sub in settings.archive_folder.split('/')[2:]:
                    if sub in folder.objectIds():
                        folder = folder[sub]
                    else:
                        type = getattr(folder, 'meta_type', None)
                        if not (type == 'ATFolder' or type == 'Plone Site'):
                            messages.addStatusMessage(
                                'Unable to create archive folder %s: '
                                '%s is not a folder!' % (
                                    settings.archive_folder, folder.getId()),
                                type='error')
                            break
                        else:
                            id = folder.invokeFactory('Folder', sub)
                            folder = folder[id]
                            folder.setTitle(sub)
                arch = folder
                messages.addStatusMessage(
                    'Created Newsletter archive folder %s' % (
                        settings.archive_folder),
                    type='info')

            if not getattr(arch, 'meta_type', None) == 'ATFolder':
                messages.addStatusMessage(
                    'Unable to use %s as archive folder: Not a folder!' % (
                        settings.archive_folder),
                    type='error')
                raise ValidationError

            if not arch.getPhysicalPath() == tuple(
                settings.archive_folder.split('/')):
                raise ValidationError("Invalid archive folder path")

            name = 'Newsletter %s' % DateTime().strftime('%d.%m.%Y')
            if name in arch.objectIds():
                messages.addStatusMessage(
                    '%s already exists in archive' % name,
                    type='warning')
            else:
                id = arch.invokeFactory('Document', name)
                new_ob = arch[id]
                new_ob.setTitle(name)
                new_ob.setText(msg)
                new_ob.setContentType('text/restructured')
                messages.addStatusMessage(
                    'Mail archived as %s' % '/'.join(new_ob.getPhysicalPath()),
                    type='info')

        except ValidationError, msg:
            logger.warning("ValidationError: %s"  %msg)
            pass
        finally:
            if self.errors:
                logger.warning("Errors: %s" %self.errors)
                for error in self.errors:
                    messages.addStatusMessage(error, type='error')
            else:
                messages.addStatusMessage(
                    self.ts.translate(
                        _('mail_sending_prepared',
                          default=("Mailversand wird vorbereitet. "
                                   "Mail wird versandt an %(mail_to)s")),
                        context=self.context,
                        mapping={u'mail_to': mail_to}),
                    type="info")
        return self.request.response.redirect(self.context.absolute_url())

class MailNewComment(BrowserView):
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.mailhost = getToolByName(self.context, 'MailHost')
        self.ts = getToolByName(self.context, 'translation_service')
        #self.pl = getToolByName(self.context, 'portal_languages')

    def __call__(self):
        root = getToolByName(self.context, 'portal_url').getPortalObject()
        mail_info = IMailSchema(root)
        mail_from = '%s <%s>' % (
            mail_info.email_from_name, mail_info.email_from_address)

        comment = self.context
        conversation = aq_parent(comment)
        review = aq_parent(conversation)
        pg = IParentGetter(review)


        args = {}
        args['url'] = review.absolute_url()
        args['author'] = get_formatted_names(u' / ', ' ', self.context.getAuthors())
        args['recipient'] = args['author']
        args['date'] = review.created().strftime('%d.%m.%Y')
        args['title'] = review.title + (review.subtitle and ': ' + review.subtitle or '')
        args['year'] = getattr(review, 'yearOfPublication', '')
        args['isbn'] = getattr(review, 'isbn', '')
        args['reviewers'] = '/'.join(review.listReviewAuthors())
        args['journal'] = pg.get_title_from_parent_of_type('Publication')
        args['volume'] = pg.get_title_from_parent_of_type('Volume')
        args['issue'] = pg.get_title_from_parent_of_type('Issue')
        args['commenter'] = comment.author_name
        args['commentdate'] = comment.creation_date.strftime('%d.%m.%Y')
        args['mail_from'] = mail_from

        for key in args:
            args[key] = safe_unicode(args[key])

        # for review types, notify authors of the works (via editorial office)
        if review.portal_type in REVIEW_TYPES:
            authors = getattr(review, 'authors', [])
            args['recipient'] = get_formatted_names(u' / ', ' ', authors)
            mail_to = mail_from
            pref_lang = 'de'
            for author in authors:
                #for pref_lang in self.pl.getAvailableLanguages().keys(): # send one mail for for every language
                subject = self.ts.translate(_('mail_new_comment_subject_review_author',
                                              mapping=args), target_language=pref_lang)
                msg_template = self.ts.translate(_('mail_new_comment_body_review_author',
                                                   mapping=args),
                                                 target_language=pref_lang)
                self.sendMail(msg_template, mail_from, mail_to, subject)
        # for presentation types, notify presentation author
        else:
            args['recipient'] = get_formatted_names(u' / ', ' ', self.context.getReviewAuthors())
            mail_to, pref_lang = self.findRecipient()
            subject = self.ts.translate(_('mail_new_comment_subject_presentation_author',
                                          mapping=args), target_language=pref_lang)
            msg_template = self.ts.translate(_('mail_new_comment_body_presentation_author',
                                               mapping=args),
                                             target_language=pref_lang)
            self.sendMail(msg_template, mail_from, mail_to, subject)

        # Find other comment authors and notify them
        recipients = []
        for item in conversation.items():
            cmt = item[1]
            if not cmt.author_email in map(lambda x: x[0], recipients) \
                                           and (not mail_to or not cmt.author_email in mail_to) \
                                           and not cmt.author_email == comment.author_email:
                rcpt = self.findRecipient(id=cmt.author_username)
                recipients.append(rcpt + (cmt.author_name,))

        for rcpt in recipients:
            mail_to, pref_lang, name = rcpt
            if ' ' in name:
                name = name.split(' ')
                name = {'firstname':name[0], 'lastname':name[1]}
            else:
                name = {'firstname':'', 'lastname':name}
            args['recipient'] = get_formatted_names(u' ',u' ', [name])
            if review.portal_type in REVIEW_TYPES:
                subject = self.ts.translate(_('mail_new_comment_subject_review_commenter',
                                              mapping=args),
                                            target_language=pref_lang)
                msg_template = self.ts.translate(_('mail_new_comment_body_review_commenter',
                                                   mapping=args),
                                                 target_language=pref_lang)
            else:
                subject = self.ts.translate(_('mail_new_comment_subject_presentation_commenter',
                                              mapping=args),
                                            target_language=pref_lang)
                msg_template = self.ts.translate(_('mail_new_comment_body_presentation_commenter',
                                                   mapping=args),
                                                 target_language=pref_lang)
            self.sendMail(msg_template, mail_from, mail_to, subject)

    def sendMail(self, msg, mail_from, mail_to, subject):
        if mail_to:
            self.mailhost.send(messageText=msg, mto=mail_to,
                               mfrom=mail_from,
                               subject=subject, charset='utf-8')
        else:
            mail_to, pref_lang = self.findRecipient()
            messages = IStatusMessage(self.request)
            messages.addStatusMessage(
                self.ts.translate(_('mail_no_recipients'),
                                  target_language=pref_lang),
                type="warning")

    def findRecipient(self, id=None):
        membership_tool = getToolByName(self.context, 'portal_membership')
        owner = membership_tool.getMemberById(
            id or self.context.__parent__.__parent__.Creator()).getUser()
        return (owner.getProperty('email'),
                owner.getProperty('preferred_language', 'en'))


class MailNewPublication(BrowserView):
    def __init__(self, request, context):
        super(BrowserView, self).__init__(request, context)
        self.mailhost = getToolByName(self.context, 'MailHost')
        self.ts = getToolByName(self.context, 'translation_service')
        self.pas = getToolByName(self.context, "acl_users")
        self.membership_tool = getToolByName(self.context, 'portal_membership')

    def __call__(self, skip_addrs=[]):
        root = getToolByName(self.context, 'portal_url').getPortalObject()
        mail_info = IMailSchema(root)
        mail_from = '%s <%s>' % (
            mail_info.email_from_name, mail_info.email_from_address)
        referenceAuthors = getattr(self.context, 'referenceAuthors', [])

        def get_preferred_language(email, default='en'):
            found = self.pas.searchUsers(email=args['mail_to'])
            if found:
                owner = self.membership_tool.getMemberById(
                    found[0]['userid']).getUser()
                return owner.getProperty('preferred_language', default)
            else:
                return default

        for author in referenceAuthors:
            if author.has_key('email') and author['email'] in skip_addrs:
                continue
            args = {}
            fuckup = [author['firstname'], author['lastname']]
            fuckup = [safe_unicode(x) for x in fuckup]
            args['reviewed_author'] = u' '.join(fuckup)
            args['mail_from'] = safe_unicode(mail_from)
            pref_lang = 'en'
            args['title'] = safe_unicode(self.context.title)
            args['subtitle'] = safe_unicode(getattr(
                self.context, 'subtitle', ''))
            args['review_author'] = get_formatted_names(
                u' / ', ' ', self.context.reviewAuthors)
            args['concept_url'] = root.absolute_url() + '/ueberuns/konzept'
            args['context_url'] = self.context.absolute_url()
            if author.has_key('email') and author['email']:
                args['mail_to'] = author['email']
                pref_lang = get_preferred_language(author['email'], pref_lang)
                msg_template = self.ts.translate(
                    _('mail_new_publication_body',
                      mapping=args), target_language=pref_lang)
            else:
                args['mail_to'] = args['mail_from']
                pref_lang = get_preferred_language(args['mail_from'], pref_lang)
                msg_template = (
                    self.ts.translate(
                        _('mail_new_publication_intro',
                          mapping=args),
                        target_language=pref_lang) +
                    self.ts.translate(
                        _('mail_new_publication_body',
                          mapping=args),
                        target_language=pref_lang)
                    )
            subject = self.ts.translate(
                _('mail_new_publication_subject',
                  default=(u"Es wurde eine Rezension von ${title} "
                           u"veröffentlicht"),
                  mapping=args),
                target_language=pref_lang)
            self.sendMail(msg_template, args['mail_to'], mail_from, subject)

    def sendMail(self, msg, mail_to, mail_from, subject):
        self.mailhost.send(messageText=msg, mto=mail_to,
                           mfrom=mail_from,
                           subject=subject, charset='utf-8')

class MailUncommented(BrowserView):
    def __init__(self, request, context):
        super(BrowserView, self).__init__(request, context)
        self.mailhost = getToolByName(self.context, 'MailHost')
        self.mail_body = u"""Sehr geehrte/r Frau/Herr ${name},

Sie haben am ${date} Ihre Schrift
    ${title}

    auf recensio.net präsentiert. Bisher liegen keine Kommentare vor. Sie haben hier die Gelegenheit, Ihre Präsentation zu modifizieren: Sie könnten die Thesenformulierung bearbeiten oder auch die Zahl der aufgeführten Bezugsautoren erweitern. In der Regel werden diese von der recensio.net-Redaktion kontaktiert, was erheblich zur Sichtbarkeit einer Präsentation beiträgt. Wenn noch nicht geschehen, haben Sie zusätzlich die Möglichkeit, Coverbilder und Inhaltsverzeichnisse beizufügen (im Fall von Präsentationen von Monographien).

    Für Rückfragen steht Ihnen die recensio.net-Redaktion gern zur Verfügung: ${mail_from}.

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
        subject = self.ts.translate(
            _('mail_uncommented_subject',
              default=u"Ihre Rezension auf recensio.net"),
            target_language=pref_lang)
        self.mailhost.send(messageText=msg, mto=mail_to,
                           mfrom=mail_from,
                           subject=subject, charset='utf-8')

    def formatMessage(self, result):
        title = result.Title
        owner_name = result.Creator
        mail, pref_lang = self.findRecipient(result)
        url = result.getURL()
        date = result.created.strftime('%d.%m.%Y')
        args = {'name' : owner_name,
                'url' : url,
                'title' : title,
                'date' : date,
                'mail_from' : self.findSender() }
        msg = self.ts.translate(
            _('mail_uncommented_body',
              default=self.mail_body, mapping=args),
            target_language=pref_lang)

        return msg

    def findRecipient(self, result):
        membership_tool = getToolByName(self.context, 'portal_membership')
        owner = membership_tool.getMemberById(result.Creator).getUser()
        return (owner.getProperty('email') or self.findSender(),
                owner.getProperty('preferred_language', 'en'))

    def findSender(self):
        root = getToolByName(self.context, 'portal_url').getPortalObject()
        membership_tool = getToolByName(self.context, 'portal_membership')
        mail_info = IMailSchema(root)
        mail_from = '%s <%s>' % (
            mail_info.email_from_name, mail_info.email_from_address)
        return mail_from

class NewsletterSettingsEditForm(controlpanel.RegistryEditForm):

    schema = INewsletterSettings
    label = _('Newsletter settings')
    description = _('This is a technical configuration panel for newsletter '
                    'settings.\nThe templates can access any object of a '
                    'catalog result, but dates have been preformatted.')

class NewsletterSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = NewsletterSettingsEditForm

