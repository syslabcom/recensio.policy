# -*- coding: utf-8 -*-

from OFS.interfaces import IFolder
from Products.ATContentTypes.interfaces import IATTopic
from zope.interface import Interface
from zope import schema

from recensio.policy import recensioMessageFactory as _

class IOAIUtility(Interface):
    """
    Utility that returns OAIProviders
    """
    def getOAIProvider(self, url):
        """
        Return OAIProvider for the given url provided as a string.
        """

    def getKnownOAIProviders(self):
        """
        Little Helper for testing/debugging.
        Return a list of strings containing urls
        """

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
    mail_template = schema.Text(title = _('Mail Template'), 
                                description = _('The container for the complete template, Variable expansion will be applied. Provide the following slots: a b c'),
                                default = u"""Liebe Abonnenten,

wie jeden Monat freuen wir uns, Sie über Neuigkeiten auf recensio.net
informieren zu können.

Angenehmes Stöbern und Entdecken wünscht Ihnen Ihre recensio.net-Redaktion.

Neue Rezensionen ...

%(new_reviews)s

Neue Präsentationen ...

%(new_presentations)s

Verfolgen Sie die Diskussion über die meistkommentierten Präsentationen
des vergangenen Monats:

%(new_discussions)s
""")
    subject = schema.TextLine(title = _('Subject'),
                              description=_("The subject of the e-mail. Thats what the user sees first when receiving the mail"),
                              default = _(u"""Recensio Newsletter"""))
    mail_format = schema.ASCIILine(title=_('Date Format'),
                                   description=_('strftime compatible date format specification, see http://docs.python.org/library/time.html#time.strftime'),
                                   default = "%d.%m.%Y")
    standard_result_template = schema.Text(title = _('Review template'),
                                           default = _(u"""%(Title)s (%(getURL)s)

%(Description)s

Created on: %(created)s
--------------------------------------------
"""))
    # This template will be used for IATTopics, that implement the
    # IDiscussionCollections Interface.
    comment_result_template = schema.Text(title = _('Review template for Discussion based searches'),
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
            u'address for submitted reviews.'),
        description=_(u'description_review_submitted_email', default=u'Enter '
            u'an e-mail address to which notifications will be sent, if a user '
            u'submits a review for publication.'),
        required=False,
        default=u'',
        )

    available_content_languages = schema.Text(
        title=_(u'label_available_content_languages', default=u'Available '
            u'languages for content in the site.'),
        description=_(u'description_available_content_languages',
             default=u'Enter one language (2 letter code) per line. These '
             u'languages will be used for the fields "Language of '
             u'Presentation" and "Language of reviewed text".'),
        required=False,
        default=u'',
        )