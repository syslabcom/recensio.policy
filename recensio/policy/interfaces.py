# -*- coding: utf-8 -*-

from OFS.interfaces import IFolder
from Products.ATContentTypes.interfaces import IATTopic
from zope.interface import Interface
from zope import schema

from recensio.policy import recensioMessageFactory as _

class INewsletterSource(IFolder):
    """
    Marker interfaces for folders that can have an action for sending
    out Newsletters
    """

class IDiscussionCollections(IATTopic):
    """
    Collections that filter based on ongoing discussions
    """

class INewsletterSettings(Interface):
    """
    Configuration for the Newsletter
    """
    prefix = schema.Text(title = _('Prefix'),
                         description =_("The start of the e-mail"),
                         default = _(u"""Willkommen zum aktuellen Newsletter.
Unten sehen Sie, was sich im letzten Monat getan hat!

"""))
    suffix = schema.Text(title = _('Suffix'),
                         description=_("The end of the e-mail"),
                         default = _(u"""
Mit freundlichen Grüßen,

            Syslab.com"""))
    subject = schema.TextLine(title = _('Subject'),
                              description=_("The subject of the e-mail. Thats what the user sees first when receiving the mail"),
                              default = _(u"""Recensio Newsletter"""))
    mail_format = schema.ASCIILine(title=_('Date Format'),
                                   description=_('strftime compatible date format specification, see http://docs.python.org/library/time.html#time.strftime'),
                                   default = "%d.%m.%Y")
    standard_result_template = schema.Text(title = _('Rezension template'),
                                           default = _(u"""%(Title)s (%(getURL)s)

%(Description)s

Created on: %(created)s
--------------------------------------------
"""))
    # This template will be used for IATTopics, that implement the
    # IDiscussionCollections Interface.
    comment_result_template = schema.Text(title = _('Rezension template for Discussion based searches'),
                                          default = _(u"""%(Title)s (%(getURL)s)

%(Description)s

Last discussed on: %(last_comment_date)s
--------------------------------------------
"""))

    separator = schema.Text(title=_(u'Separator'),
                            description=_(u'The separator will be used to separate sections of the email '\
                                'from each other.'),
                            default=u"""*********************************************

""")

class IWorkflowHelper(Interface):
    
    def handleTransition(wf_variable):
        """ Action that is performed after a workflow change, e.g.
            send a notification e-mail.
        """

class IRecensioSettings(Interface):
    """ Global recensio settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    review_submitted_email = schema.TextLine(
        title=_(u'label_review_submitted_email', default=u'E-mail '
            'address for submitted reviews.'),
        description=_(u'description_review_submitted_email', default=u'Enter '
            'an e-mail address to which notifications will be sent, if a user '
            'submits a review for publication.'),
        required=False,
        default=u'',
        )
