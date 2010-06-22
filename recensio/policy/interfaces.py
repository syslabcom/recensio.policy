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
    prefix = schema.Text(title = _('Prefix'), description=_("The start of the e-mail"))
    mail_format = schema.ASCIILine(title=_('Date Format'), description=_('strftime compatible date format specification, see http://docs.python.org/library/time.html#time.strftime'))
    standard_result_template = schema.Text(title = _('Rezension template'))
    # This template will be used for IATTopics, that implement the
    # IDiscussionCollections Interface.
    comment_result_template = schema.Text(title = _('Rezension template for Discussion based searches'))

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
