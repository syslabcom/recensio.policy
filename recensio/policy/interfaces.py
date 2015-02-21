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
                                description = _(u'description_mailsettings_mail_template', default=u'The container for the complete template, Variable expansion will be applied. Provide the following slots: a b c'),
                                default = u"""(English version see below)

**Liebe Abonnenten,**


wie jeden Monat freuen wir uns, Sie über Neuigkeiten auf recensio.net informieren zu können.

Angenehmes Stöbern und Entdecken wünscht Ihnen


*Ihre recensio.net-Redaktion.*


-----------------------
Neue Präsentationen ...
-----------------------

%(new_presentations)s

------------------------
Neue Rezensionsteile ...
------------------------

%(new_review_sections)s

--------------------
Neue Rezensionen ...
--------------------

%(new_reviews)s

-------------------------------------
Verfolgen Sie die Diskussion über ...
-------------------------------------

... die meistkommentierten Präsentationen des vergangenen Monats:
-----------------------------------------------------------------

%(new_discussions)s


*********************************************


**Dear subscribers,**


It’s time again for your monthly digest of news from recensio.net.

We hope you will enjoy browsing our platform and discovering its content.


*Your recensio.net editorial team*


---------------------
New presentations ...
---------------------

%(new_presentations)s

---------------
New reviews ...
---------------

%(new_reviews)s

----------------------------
Follow the discussion on ...
----------------------------

... the presentations most commented on over the course of the past months:
---------------------------------------------------------------------------
%(new_discussions)s
""")
    subject = schema.TextLine(title = _('Subject'),
                              description=_(u'description_mailsettings_subject', default=u"The subject of the e-mail. Thats what the user sees first when receiving the mail"),
                              default = _(u"""Recensio Newsletter"""))
    mail_format = schema.ASCIILine(title=_('Date Format'),
                                   description=_(u'description_mailsettings_date_format', default=u'strftime compatible date format specification, see http://docs.python.org/library/time.html#time.strftime'),
                                   default = "%d.%m.%Y")
    standard_result_template = schema.Text(title = _('Review template'),
                                           default = u"""%(Title)s (%(getURL)s)

%(Description)s

Erstellt am: / Created on: %(created)s
""")
    # This template will be used for IATTopics, that implement the
    # IDiscussionCollections Interface.
    comment_result_template = schema.Text(title = _('Review template for Discussion based searches'),
                                          default = u"""%(Title)s (%(getURL)s)

%(Description)s

Zuletzt kommentiert am: / Last discussed on: %(last_comment_date)s
""")

    separator = schema.Text(title=_(u'Separator'),
                            description=_(u'The separator will be used to separate sections of the email '\
                                'from each other.'),
                            default=u"""*********************************************

""")
    archive_folder = schema.TextLine(title = _('Archive Folder'),
                              description=_(u'description_mailsettings_archive_folder', default=u"The path of the folder where newsletter mails will be saved after they have been sent. Will be created when needed if it does not exist."),
                              default = u"""/recensio/newsletter/archiv""")

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

    xml_export_server = schema.TextLine(
        title=_(u'label_xml_export_server',
                default=u'Server name for Chronicon export'),
        description=_(u'description_xml_export_server',
                      default=u'Enter the server name that should be used for '
                      'exporting XML metadata to Chronicon over SFTP.'),
        required=False,
        default=u'',
    )

    xml_export_username = schema.TextLine(
        title=_(u'label_xml_export_username',
                default=u'User name for Chronicon export'),
        description=_(u'description_xml_export_username',
                      default=u'Enter the user name that should be used for '
                      'exporting XML metadata to Chronicon over SFTP.'),
        required=False,
        default=u'',
    )

    xml_export_password = schema.TextLine(
        title=_(u'label_xml_export_password',
                default=u'Password for Chronicon export'),
        description=_(u'description_xml_export_password',
                      default=u'Enter the password that belongs to the above '
                      'SFTP user name.'),
        required=False,
        default=u'',
    )

    doi_registration_url = schema.TextLine(
        title=_(u'label_doi_registration_url',
                default=u'URL for DOI registration'),
        description=_(u'description_doi_registration_url',
                      default=u'Endpoint URL for registration of DOIs'),
        required=False,
        default=u'http://www.da-ra.de/dara/study/importXML?registration=true',
    )

    doi_registration_username = schema.TextLine(
        title=_(u'label_doi_registration_username',
                default=u'User name for DOI registration'),
        description=_(u'description_doi_registration_username',
                      default=u'User name to use as login for registration of '
                      'DOIs'),
        required=False,
        default=u'',
    )

    doi_registration_password = schema.TextLine(
        title=_(u'label_doi_registration_password',
                default=u'Password for DOI registration'),
        description=_(u'description_doi_registration_password',
                      default=u'Password that belongs to the above user name '
                      'for registration of DOIs'),
        required=False,
        default=u'',
    )


class IRecensioView(Interface):

    def getSupportedLanguages():
        """ Get the languages defines in the recensio-setting which our
        content types support."""


class IDigitoolView(Interface):
    """ Supports exporting XML to digitool """


class IRecensioExporter(Interface):
    """ Interface for bulk exporting review data"""

    def needs_to_run():
        """ True if the exporter needs to be run at the time of the call,
            False if the exporter thinks it has nothing to do right now, e.g. a
            recent export is still stored """

    def add_review():
        """ Accepts a review that is to be exported in the current run. """

    def export():
        """ Finishes the current export run. This should store the exported
        data in a way appropriate for the export. """
